import wx
import main_class
import settings
import copy
import sys


import req
import orbit
import ope_voltage
import south_judge
from datetime import datetime
import time
import serial
import math
import re
import csv
import ephem
import os


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class moritator_main_class( main_class.main_class ):
    def __init__( self, parent ):
        frame = wx.Frame(None, -1, 'MORITATOR', size=(415,235))
        frame.Centre()
        panel = wx.Panel(frame, wx.ID_ANY)
        frame.Show(True)
        image = wx.Image(resource_path('loading.png'))
        bitmap = image.ConvertToBitmap()
        wx.StaticBitmap(panel, -1, bitmap, pos=(0, 0), size=(400,200))

        settings.init()
        self.satellite_choiceChoices, self.norad_id_list = settings.load_sat_list()
        port_list = list(serial.tools.list_ports.comports())
        self.sat_num, self.port = settings.load_state()
        expected_ports = []
        flag_not_found = False
        for p in port_list:
            try:
                if 'Serial' in p[1] and 'USB' in p[1]:
                    check = serial.Serial(p[0],baudrate=9600,timeout=1)
                    check.close()
                    expected_ports.append(p[0])
            except:
                pass
        self.com_port_choiceChoices = expected_ports
        if len(expected_ports) == 0:
            self.port = 'NOT FOUND'
            self.com_port_choiceChoices = ['NOT FOUND']
            flag_not_found = True
        else:
            if not self.port in expected_ports:
                self.port = expected_ports[0]
        if self.sat_num >= len(self.satellite_choiceChoices):
            self.sat_num = 0
        self.norad_id = self.norad_id_list[self.sat_num]
        self.sat_name = self.satellite_choiceChoices[self.sat_num]
        self.bg_sat_list = settings.load_background_sat_list() #複数衛星追跡機能の設定ファイルを読み込み，対象衛星のリストを取得


        main_class.main_class.__init__( self, parent )
        self.Bind(wx.EVT_IDLE, self.main)
        self.Bind(wx.EVT_MOVE, self.main)
        self.Bind(wx.EVT_MOVE_START, self.main)
        self.Bind(wx.EVT_MOVING, self.main)
        self.Bind(wx.EVT_MOVE_END, self.main)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.main)
        self.Bind(wx.EVT_CLOSE, self.frame_close)
        self.set_satellite_b.Bind(wx.EVT_BUTTON, self.set_satellite)
        self.set_norad_b.Bind(wx.EVT_BUTTON, self.set_norad_id)
        self.set_comport_b.Bind(wx.EVT_BUTTON, self.set_comport)
        self.set_90_b.Bind(wx.EVT_BUTTON, self.manual_rotation_antenna_90)
        self.daisenkai_b.Bind(wx.EVT_BUTTON, self.manual_rotation)
        self.daisenkai_b2.Bind(wx.EVT_BUTTON, self.disable_rotation)
        self.is_multiple_checkbox.Bind(wx.EVT_CHECKBOX, self.change_multiple_mode)
        self.last_runtime = time.time()


        #init parameters
        self.deg90_flag = False
        self.flag_round = False
        self.flag_start_round = False
        self.flag_do_not_round = False
        self.flag_after_pass = True
        self.flag_first_loop = True
        self.flag_init_rotation = True

        self.loop_cnt = 0
        self.azi_M = 0.0
        self.azi_M1 = 0.0
        self.azi_M2 = 0.0
        self.ele_M = 0.0
        self.ele_M1 = 0.0

        self.azi_e = 0.00
        self.azi_e1 = 0.00
        self.azi_e2 = 0.00
        self.ele_e = 0.00
        self.ele_e1 = 0.00
        self.ele_e2 = 0.00

        self.aKp = 0.25
        self.aKi = 0.125
        self.aKd = 0.10
        self.eKp = 0.10
        self.eKi = 0.25
        self.eKd = 0.10

        self.plus_angle = [0] * 10
        self.pluse_angle = [0] * 10
        self.a_cnt = 0
        self.sum_kakudo = 0
        self.sume_kakudo = 0
        self.cal_kakudo = 0
        self.cale_kakudo = 0

        self.cnt = 0
        self.send_flag = 0
        self.next_azi_flag = 0
        self.next_ele_flag = 0

        self.azi_x = []
        self.azi_y = []
        self.ele_x = []
        self.ele_y = []

        self.azi_x.append(0.00)
        self.azi_y.append(0.00)
        self.ele_x.append(0.00)
        self.ele_y.append(0.00)

        self.azi_kakudo = 0.0
        self.ele_kakudo = 0.0
        self.now_azi_cood = 0.0
        self.now_ele_cood = 0.0
        self.before_azi_cood = 0.0
        self.before_ele_cood = 0.0

        self.azi_goal2 = 0.0
        self.azi_goal3 = 0.0

        try:
            self.tle = req.read_TLE(self.norad_id)
            if len(self.tle) < 2:
                self.sat_num = 0
                self.norad_id = self.norad_id_list[self.sat_num]
                self.sat_name = self.satellite_choiceChoices[self.sat_num]
                self.satellite_choice.SetSelection( self.sat_num )
                self.tle = req.read_TLE(self.norad_id)
        except:
            self.sat_num = 0
            self.norad_id = self.norad_id_list[self.sat_num]
            self.sat_name = self.satellite_choiceChoices[self.sat_num]

        if not flag_not_found:
            self.ser1 = serial.Serial(self.port,baudrate=9600,timeout=1)

        self.start_time,self.finish_time = south_judge.judgement(self.tle)

        self.csv_strtime = str(self.start_time)
        self.csv_time = self.csv_strtime.split()
        print(self.csv_time)
        self.csv_ttime = self.csv_time[1].split(':')
        self.csv_tttime = self.csv_ttime[2].split('.')
        print(self.csv_time)

        csv_date = '-'.join(self.csv_time[0].split('/'))

        #csvfile open
        if not os.path.exists('./../moritator_log'):
            os.makedirs('./../moritator_log')
        f = open('./../moritator_log/' + csv_date + '_' + str(self.csv_ttime[0]) + str(self.csv_ttime[1]) + str(self.csv_tttime[0]) +'.csv', 'w')
        self.writer = csv.writer(f, lineterminator = '\n')
        self.writer.writerow([self.tle[0]])
        self.writer.writerow([self.tle[1]])
        self.writer.writerow([self.tle[2]])
        self.writer.writerow(['', 'ローテータ', ' ', '衛星', ' '])
        self.writer.writerow(['JST', 'アジマス', 'エレベーション',  'アジマス', 'エレベーション'])
        settings.save_state(self.sat_num, self.port)
        frame.Show(False)

    def set_satellite(self, event):
        self.init_rotation()
        self.deg90_flag == False
        self.sat_num = self.satellite_choice.GetSelection()
        self.sat_name = self.satellite_choiceChoices[self.sat_num]
        self.norad_id = self.norad_id_list[self.satellite_choice.GetSelection()]
        self.norad_id_input.SetValue(self.norad_id)
        self.tle = req.read_TLE(self.norad_id)
        self.tracking_satellite.SetLabel(self.sat_name)
        settings.save_state(self.sat_num, self.port)
        if event != None:
            self.is_multiple_checkbox.SetValue(False)

    def set_comport(self, event):
        self.port = self.com_port_choiceChoices[self.com_port_choice.GetSelection()]
        settings.save_state(self.sat_num, self.port)
        self.ser1 = serial.Serial(self.port,baudrate=9600,timeout=1)
        settings.save_state(self.sat_num, self.port)

    def set_norad_id(self, event):
        self.init_rotation()
        self.deg90_flag = False
        self.norad_id = self.norad_id_input.GetValue()
        self.tle = req.read_TLE(self.norad_id)
        norad_list = copy.deepcopy(self.norad_id_list)
        norad_list[-1] = ''
        if self.norad_id in norad_list:
            self.sat_num = self.norad_id_list.index(self.norad_id)
            self.sat_name = self.satellite_choiceChoices[self.sat_num]
            self.satellite_choice.SetSelection(self.sat_num)
        else:
            self.sat_num = len(self.satellite_choiceChoices) - 1
            self.sat_name = self.tle[0]
            self.norad_id_list[-1] = self.norad_id
        self.satellite_choice.SetSelection( self.sat_num )
        self.tracking_satellite.SetLabel('     '+self.sat_name)
        for i in range(100):
            print(self.sat_name)
        if len(self.sat_name) > 10:
            font_size = int(900/len(self.sat_name))
            self.tracking_satellite.SetFont( wx.Font( font_size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        else:
            self.tracking_satellite.SetFont( wx.Font( 48, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        settings.save_state(self.sat_num, self.port)
        settings.save_other_id(self.norad_id)
        if event != None:
            self.is_multiple_checkbox.SetValue(False)

    def manual_rotation_antenna_90(self, event):
        if self.deg90_flag == False:
            self.deg90_flag = True
            self.tracking.SetLabel( u"")
            self.tracking_satellite.SetLabel('SET 90 MODE')
            self.sat_ele.SetLabel('')
            self.sat_azi.SetLabel('')
            self.next_rise.SetLabel('')
            self.next_set.SetLabel('')
            self.aos_time.SetLabel('')
            self.los_time.SetLabel('')
            self.set_90_b.SetLabel('CANCEL')
        else:
            self.deg90_flag = False
            self.tracking.SetLabel( u"\n               Now Tracking ")
            self.tracking_satellite.SetLabel(self.sat_name)
            self.set_90_b.SetLabel('SET 90 & QUIT')

    def set_next_sat(self):
        if self.is_multiple_checkbox.GetValue() and self.flag_after_pass:
            self.flag_after_pass = False
            sat_list = copy.copy(self.bg_sat_list)
            for i in range(len(sat_list)):
                name = sat_list[i][0]
                id = sat_list[i][1]
                if len(id) > 5:
                    id = id[:5]
                tle = req.read_TLE(id)
                sat = ephem.readtle(tle[0], tle[1], tle[2])
                fudai = ephem.Observer()
                fudai.lat = '34.545898'
                fudai.lon = '135.503224'
                rise_t, az_rise, max_t, alt_max, set_t, az_set = fudai.next_pass(sat)
                sat_list[i] = [rise_t, name, id]
            sat_list.sort()
            next_id = sat_list[0][2]
            self.norad_id_input.SetValue(next_id)
            self.set_norad_id(None)
        else:
            pass

    def change_multiple_mode(self, event):
        if self.is_multiple_checkbox.GetValue():
            self.flag_after_pass = True
            self.set_next_sat()
        else:
            self.set_norad_id(None)


    def main(self, event):
        try:
            times = 1
            event.RequestMore(True)
        except:
            times = 3
            pass
        if time.time() - self.last_runtime > 0.25*times:
            self.last_runtime = time.time()
            try:
                if self.deg90_flag:
                    self.set_antenna_90()
                else:
                    self.operate_antenna()
                    if self.sat_num == len(self.satellite_choiceChoices) - 1:
                        self.sat_name = self.tle[0]
                        if self.sat_name[:2] == '0 ':
                            self.sat_name == self.sat_name[2:]
                    self.tracking_satellite.SetLabel(self.sat_name)
                    if len(self.sat_name) > 10:
                        font_size = int(900/len(self.sat_name))
                        self.tracking_satellite.SetFont( wx.Font( font_size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
                    else:
                        self.tracking_satellite.SetFont( wx.Font( 48, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
                    self.tracking.SetLabel( u"\n                   Now Tracking ")
                    utctime = datetime.utcnow()
                    self.angle = orbit.cal_orbit(self.tle,utctime)
                    self.sat_ele.SetLabel('%0.2f'%self.angle[1])
                    self.sat_azi.SetLabel('%0.2f'%self.angle[0])
            except:
                self.tracking_satellite.SetLabel('ERROR')
                self.tracking.SetLabel('')

    def set_antenna_90(self):
        set_deg = 90
        self.ele_goal = set_deg
        self.init_rotation()
        if set_deg - self.ele_kakudo < 1 and set_deg -self.ele_kakudo > -1:
            self.frame_close(wx.EVT_CLOSE)
        self.output_voltage_to_wait()

    def manual_rotation(self, event):
        self.send_flag = 0
        if self.flag_round:
            self.flag_start_round = not self.flag_start_round
        else:
            self.flag_start_round = False
        if self.flag_start_round:
            self.now_daisenkai_text.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
            self.now_daisenkai_text.SetLabel('Manual Rotation ENABLED')
            self.writer.writerow([str(datetime.now()), 'Manual Rotation ENABLED'])
            self.daisenkai_b.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
            self.daisenkai_b2.SetLabel('DISABLE')
            self.daisenkai_b2.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
            self.flag_do_not_round = False
        else:
            self.now_daisenkai_text.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
            self.now_daisenkai_text.SetLabel('AUTO ROTATION (default)')
            self.writer.writerow([str(datetime.now()), 'Manual Rotation DISABLED'])
            self.daisenkai_b.SetLabel('MANUAL')
            self.daisenkai_b.SetForegroundColour( wx.Colour( 0, 0, 0 ) )

    def disable_rotation(self, event):
        if self.flag_round:
            self.flag_do_not_round = not self.flag_do_not_round
        else:
            self.flag_do_not_round = False
        if self.flag_do_not_round:
            self.now_daisenkai_text.SetForegroundColour( wx.Colour( 0, 0, 255 ) )
            self.now_daisenkai_text.SetLabel('Rotation DISABLED')
            self.writer.writerow([str(datetime.now()), 'Rotation DISABLED'])
            self.daisenkai_b2.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
            self.daisenkai_b.SetLabel('MANUAL')
            self.daisenkai_b.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
            self.flag_start_round = False
        else:
            self.now_daisenkai_text.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
            self.now_daisenkai_text.SetLabel('AUTO ROTATION (default)')
            self.daisenkai_b2.SetLabel('DISABLE')
            self.daisenkai_b2.SetForegroundColour( wx.Colour( 0, 0, 0 ) )

    def init_rotation(self):
        self.now_daisenkai_text.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
        self.now_daisenkai_text.SetLabel('AUTO ROTATION (default)')
        self.daisenkai_b2.SetLabel('DISABLE')
        self.daisenkai_b2.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
        self.daisenkai_b.SetLabel('MANUAL')
        self.daisenkai_b.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
        self.flag_round = False
        self.flag_start_round = False
        self.flag_do_not_round = False
        self.flag_init_rotation = True
        self.send_flag = 0

    def judge_round(self):
        self.flag_first_loop = False
        self.flag_round = False
        hirogari = ephem.readtle(self.tle[0], self.tle[1], self.tle[2])
        fudai = ephem.Observer()
        fudai.lat = '34.545898'
        fudai.lon = '135.503224'
        rise_t, az_rise, max_t, alt_max, set_t, az_set = fudai.next_pass(hirogari)
        az_rise = int(orbit.cal_orbit(self.tle, rise_t)[0])
        az_set = int(orbit.cal_orbit(self.tle, set_t)[0])
        az_max = int(orbit.cal_orbit(self.tle,max_t)[0])

        parameter = az_rise
        distance = 0
        while(parameter != az_max):
            parameter += 1
            distance += 1
            if parameter >= 360:
                parameter -= 360
        if distance <= 180:
            self.flag_clockwise = True
        else:
            self.flag_clockwise = False
        parameter = az_rise
        while(parameter != az_set):
            if self.flag_clockwise:
                parameter += 1
            else:
                parameter -= 1
            if parameter >= 360:
                parameter -= 360
            elif parameter < 0:
                parameter += 360
            if parameter > 160 and parameter < 165:
                self.flag_round = True
                break
        if self.flag_round:
            self.daisenkai_yesno_text.SetLabel('YES')
            self.daisenkai_yesno_text.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
        else:
            self.daisenkai_yesno_text.SetLabel('NO')
            self.daisenkai_yesno_text.SetForegroundColour( wx.Colour( 0, 0, 0 ) )

        return self.flag_round

    def operate_antenna(self):
        utctime = datetime.utcnow()
        self.angle = orbit.cal_orbit(self.tle,utctime)
        self.sat_ele.SetLabel('%0.2f'%self.angle[1])
        self.sat_azi.SetLabel('%0.2f'%self.angle[0])

        hirogari = ephem.readtle(self.tle[0], self.tle[1], self.tle[2])
        fudai = ephem.Observer()
        fudai.lat = '34.545898'
        fudai.lon = '135.503224'

        self.rise_t, self.az_rise, max_t, alt_max, self.set_t, self.az_set = fudai.next_pass(hirogari)
        rise_t_jst = ephem.localtime(self.rise_t)
        set_t_jst = ephem.localtime(self.set_t)
        print(self.rise_t)
        if self.angle[1] <= -1:
            if self.flag_init_rotation == False:
                self.init_rotation()
            self.set_next_sat()
            self.judge_round()
            print(type(self.rise_t))
            aos_t = str(rise_t_jst).split()
            los_t = str(set_t_jst).split()
            self.aos_time.SetLabel(aos_t[0] + '\n' + aos_t[1][0:8])
            self.los_time.SetLabel(los_t[0] + '\n' + los_t[1][0:8])
            self.next_angle = orbit.cal_orbit(self.tle,self.rise_t)
            self.next_set_angle = orbit.cal_orbit(self.tle, self.set_t)
            self.next_rise.SetLabel('%0.2f'%self.next_angle[0])
            self.next_set.SetLabel('%0.2f'%self.next_set_angle[0])
            self.set_angle_to_wait()
            self.output_voltage_to_wait()
        else:
            self.flag_init_rotation = False
            self.flag_after_pass = True
            if self.flag_first_loop:
                self.judge_round()
            self.set_angle_to_sat()
            print('1')
            self.output_voltage_to_sat()
            print('2')

    def set_angle_to_wait(self):
        next_time = ope_voltage.cal_voltage(self.angle,self.tle)
        self.next_angle = orbit.cal_orbit(self.tle,next_time)
        next_voltage = ope_voltage.cal_voltage(self.next_angle,self.tle)

        if self.next_angle[0] > 165:
            self.azi_goal = self.next_angle[0] - 360
        else:
            if self.next_angle[0] >160:
                self.next_angle[0] = 160
            self.azi_goal = self.next_angle[0]
        self.ele_goal = self.next_angle[1]
        if self.flag_round and self.flag_start_round:
            if self.flag_clockwise:
                self.azi_goal = -195
            else:
                self.azi_goal = 160

    def set_angle_to_sat(self):
        if self.flag_clockwise:
            if self.angle[0] >= 165:
                self.flag_start_round = False
                self.flag_round = False
                self.now_daisenkai_text.SetLabel('ROTATION FINISHED')
                self.daisenkai_b.SetLabel('MANUAL')
                self.daisenkai_b2.SetLabel('DISABLE')
        else:
            if self.angle[0] <= 160:
                self.flag_start_round = False
                self.flag_round = False
                self.now_daisenkai_text.SetLabel('ROTATION FINISHED')
                self.daisenkai_b.SetLabel('MANUAL')
                self.daisenkai_b2.SetLabel('DISABLE')

        if self.angle[0] > 165:
            self.azi_goal = self.angle[0] - 360
        else:
            if self.angle[0] >160:
                self.angle[0] = 160
            self.azi_goal = self.angle[0]
        self.ele_goal = self.angle[1]


        if self.flag_round:
            if self.flag_start_round:
                if self.flag_clockwise:
                    self.azi_goal = -195
                else:
                    self.azi_goal = 160
            elif self.flag_do_not_round:
                if self.flag_clockwise:
                    if self.angle[0] >= 160:
                        self.azi_goal = 160
                else:
                    if self.angle[0] <= 165:
                        self.azi_goal = -195


    def output_voltage_to_wait(self):
        send_flag = 0
        voltage = ope_voltage.cal_voltage(self.angle,self.tle)
        r=self.ser1.readline()
        if len(r) != 0:
            regex = re.compile('\d+')
            match = regex.findall(str(r))
            self.before_azi_cood = self.now_azi_cood
            self.before_ele_cood = self.now_ele_cood
            self.now_azi_cood = float(match[0]) + float(match[1]) / (pow(10,len(match[1])))
            self.now_ele_cood = float(match[2]) + float(match[3]) / (pow(10,len(match[3])))
            print('azi:' + str(self.now_azi_cood) + ' ele:' + str(self.now_ele_cood))

        #yes pid
        if self.now_azi_cood >= 0.0616 and self.now_azi_cood <= 4.781323:           #20210319
            self.azi_kakudo = 62.267 * self.now_azi_cood - 199.21
        elif self.now_azi_cood > 4.781323 and self.now_azi_cood <= 4.8318:           #20210319
            self.azi_kakudo = 197.87 * self.now_azi_cood - 846.1
        elif self.now_azi_cood > 4.8318 and self.now_azi_cood <= 4.995117:          #20210319
            self.azi_kakudo = 489.64 * self.now_azi_cood*self.now_azi_cood - 4501.8 * self.now_azi_cood + 10430
        else:
            self.now_azi_cood = self.before_azi_cood

        if self.now_ele_cood >= 0.0 and self.now_ele_cood < 4.5583:               #20210313
            self.ele_kakudo = 15.484 * self.now_ele_cood - 5.9071
        elif self.now_ele_cood >= 4.5583 and self.now_ele_cood <= 5.0:
            self.ele_kakudo = 164.45 * self.now_ele_cood*self.now_ele_cood - 1502.1 * self.now_ele_cood + 3495.2
        else:
            self.now_ele_cood = self.before_ele_cood

        if self.azi_kakudo < 0:
            label_azi = self.azi_kakudo + 360
        else:
            label_azi = self.azi_kakudo
        self.antenna_azi.SetLabel('%0.2f'%label_azi)
        self.antenna_ele.SetLabel('%0.2f'%self.ele_kakudo)

        #azimath
        self.azi_M2 = self.azi_M1
        self.azi_M1 = self.azi_M
        self.azi_e2 = self.azi_e1
        self.azi_e1 = self.azi_e
        self.azi_e = (self.azi_goal + 0) - self.azi_kakudo
        if self.azi_e < 10 and self.azi_e > -10:
            self.azi_M = self.aKp * (self.azi_e-self.azi_e1) + self.aKi * self.azi_e + self.aKd * ((self.azi_e-self.azi_e1) - (self.azi_e1-self.azi_e2))
            self.azi_pwm = round(self.azi_M,1)
            if self.azi_pwm >= 5:
                self.azi_pwm = 0.49
            elif self.azi_pwm <= -5:
                self.azi_pwm = -0.49
            else:
                self.azi_pwm = self.azi_pwm / 10
        elif self.azi_e >= 8:
            self.azi_pwm = 0.49
        elif self.azi_e <= -8:
            self.azi_pwm = -0.49

        if self.azi_e < 4 and self.azi_e > -4:
            self.next_azi_flag = 1
        else:
            self.next_azi_flag = 0

        #elevation
        self.ele_M1 = self.ele_M
        self.ele_e2 = self.ele_e1
        self.ele_e1 = self.ele_e
        self.ele_e = (self.ele_goal + 0) - self.ele_kakudo
        self.ele_M = self.eKp * (self.ele_e-self.ele_e1) + self.eKi * self.ele_e + self.eKd * ((self.ele_e-self.ele_e1) - (self.ele_e1-self.ele_e2))

        if self.ele_e >= 1:
            self.ele_pwm = 0.99
        elif self.ele_e >= 0 and self.ele_e < 1:
            self.ele_pwm = 0.5
        elif self.ele_e >= -1 and self.ele_e < 0:
            self.ele_pwm = 0.5
        elif self.ele_e < -1:
            self.ele_pwm = -0.99

        if self.ele_e < 1 and self.ele_e > -1:
            self.next_ele_flag = 1
        else:
            self.next_ele_flag = 0

        if self.next_azi_flag == 1 and self.next_ele_flag == 1:
            self.azi_pwm = 1.01
            self.ele_pwm = 1.01

        azi_send_data = math.floor(self.azi_pwm * 100)
        ele_send_data = math.floor(self.ele_pwm * 100)
        hoge1 = azi_send_data.to_bytes(1,'little',signed=True)
        hoge2 = ele_send_data.to_bytes(1,'little',signed=True)

        if self.send_flag == 0:
            if self.cnt == 0:
                self.ser1.write(hoge1)
                self.cnt = 1

            elif self.cnt == 1:
                self.ser1.write(hoge2)
                self.cnt = 0

        if self.next_azi_flag == 1 and self.next_ele_flag == 1:
            self.send_flag = 1

    def output_voltage_to_sat(self):
        self.send_flag = 0
        voltage = ope_voltage.cal_voltage(self.angle,self.tle)
        r=self.ser1.readline()
        if len(r) != 0:
            regex = re.compile('\d+')
            match = regex.findall(str(r))
            self.before_azi_cood = self.now_azi_cood
            self.before_ele_cood = self.now_ele_cood
            self.now_azi_cood = float(match[0]) + float(match[1]) / (pow(10,len(match[1])))
            self.now_ele_cood = float(match[2]) + float(match[3]) / (pow(10,len(match[3])))
        #-195 <= self.azi_kakudo <= 165
        if self.now_azi_cood >= 0.0616 and self.now_azi_cood <= 4.781323:           #20210319
            self.azi_kakudo = 62.267 * self.now_azi_cood - 199.21
        elif self.now_azi_cood > 4.781323 and self.now_azi_cood <= 4.8318:           #20210319
            self.azi_kakudo = 197.87 * self.now_azi_cood - 846.1
        elif self.now_azi_cood > 4.8318 and self.now_azi_cood <= 4.995117:          #20210319
            self.azi_kakudo = 489.64 * self.now_azi_cood*self.now_azi_cood - 4501.8 * self.now_azi_cood + 10430
        else:
            self.now_azi_cood = self.before_azi_cood

        self.plus_angle[self.a_cnt] = self.azi_kakudo

        if self.loop_cnt >= 3:
            for t in range(0,3):
                self.sum_kakudo = self.sum_kakudo + self.plus_angle[t]
            self.cal_kakudo = self.sum_kakudo / 3
            self.sum_kakudo = 0
        else:
            self.cal_kakudo = self.plus_angle[self.a_cnt]


        if self.loop_cnt >= 3:
            for t in range(0,3):
                self.sume_kakudo = self.sume_kakudo + self.pluse_angle[t]
            self.cale_kakudo = self.sume_kakudo / 3
            self.sume_kakudo = 0
        else:
            self.cale_kakudo = self.pluse_angle[self.a_cnt]

        self.a_cnt = self.a_cnt + 1
        if self.a_cnt >= 3:
            self.a_cnt = 0

            if self.now_ele_cood >= 0.0 and self.now_ele_cood < 4.5583:               #20210313
                self.ele_kakudo = 15.484 * self.now_ele_cood - 5.9071
            elif self.now_ele_cood >= 4.5583 and self.now_ele_cood <= 5.0:
                self.ele_kakudo = 164.45 * self.now_ele_cood*self.now_ele_cood - 1502.1 * self.now_ele_cood + 3495.2
            else:
                self.now_ele_cood = self.before_ele_cood

        if self.azi_kakudo < 0:
            label_azi = self.azi_kakudo + 360
        else:
            label_azi = self.azi_kakudo
        self.antenna_azi.SetLabel('%0.2f'%label_azi)
        self.antenna_ele.SetLabel('%0.2f'%self.ele_kakudo)

        #pid
        self.azi_M2 = self.azi_M1
        self.azi_M1 = self.azi_M
        self.azi_e2 = self.azi_e1
        self.azi_e1 = self.azi_e
        self.azi_e = (self.azi_goal - 2) - self.cal_kakudo
        if self.ele_goal >= 50 and (self.azi_goal3 - self.azi_goal2) < 0:      #cw
            if self.ele_goal <= 55:
                self.azi_e = (self.azi_goal + (self.ele_goal-50-2)) - self.cal_kakudo
            else:
                self.azi_e = (self.azi_goal + 5) - self.cal_kakudo
        elif self.ele_goal >= 50 and (self.azi_goal3 - self.azi_goal2) > 0:    #ccw
            if self.ele_goal <= 55:
                self.azi_e = (self.azi_goal - (self.ele_goal-50-2)) - self.cal_kakudo
            else:
                self.azi_e = (self.azi_goal - 5) - self.cal_kakudo
        self.azi_ee = self.azi_goal - self.azi_kakudo
        if self.azi_e < 10 and self.azi_e > -10:
            self.azi_M = self.aKp * (self.azi_e-self.azi_e1) + self.aKi * self.azi_e + self.aKd * ((self.azi_e-self.azi_e1) - (self.azi_e1-self.azi_e2))
            self.azi_pwm = round(self.azi_M,1)
            if self.azi_pwm >= 5:
                self.azi_pwm = 0.49
            elif self.azi_pwm <= -5:
                self.azi_pwm = -0.49
            else:
                self.azi_pwm = self.azi_pwm / 10

        if self.azi_e >= 5:
            self.azi_pwm = 0.49
        elif self.azi_e <= -5:
            self.azi_pwm = -0.49
        self.azi_y.append(self.azi_e)
        self.azi_x.append(self.loop_cnt)

        #to do max speed
        self.azi_goal3 = self.azi_goal2
        self.azi_goal2 = self.azi_goal
        if self.loop_cnt > 1:
            if self.azi_goal - self.azi_goal3 > 1.5:
                self.azi_pwm = 0.49
            elif self.azi_goal - self.azi_goal3 < -1.5:
                self.azi_pwm = -0.49

        self.ele_M1 = self.ele_M
        self.ele_e2 = self.ele_e1
        self.ele_e1 = self.ele_e
        self.ele_e = (self.ele_goal - 3) - self.ele_kakudo
        self.ele_M = self.eKp * (self.ele_e-self.ele_e1) + self.eKi * self.ele_e + self.eKd * ((self.ele_e-self.ele_e1) - (self.ele_e1-self.ele_e2))

        self.ele_y.append(self.ele_e)
        self.ele_x.append(self.loop_cnt)

        self.ele_pwm = round(self.ele_M,1)
        if self.ele_pwm >= 0:
            self.ele_pwm = self.ele_pwm + 5
        elif self.ele_pwm < 0:
            self.ele_pwm = self.ele_pwm - 5

        if self.ele_pwm >= 10:
            self.ele_pwm = 0.99
        elif self.ele_pwm <= -10:
            self.ele_pwm = -0.99
        else:
            self.ele_pwm = self.ele_pwm / 10

        if self.ele_e >= 1:
            self.ele_pwm = 0.99
        elif self.ele_e >= 0 and self.ele_e < 1:
            self.ele_pwm = 0.5
        elif self.ele_e >= -1 and self.ele_e < 0:
            self.ele_pwm = 0.5
        elif self.ele_e < -1:
            self.ele_pwm = -0.99

        self.writer.writerow([str(datetime.now()), self.cal_kakudo, self.ele_kakudo, self.azi_goal, self.ele_goal])
        azi_send_data = math.floor(self.azi_pwm * 100)
        ele_send_data = math.floor(self.ele_pwm * 100)
        hoge1 = azi_send_data.to_bytes(1,'little',signed=True)
        hoge2 = ele_send_data.to_bytes(1,'little',signed=True)
        if self.cnt == 0:
            self.ser1.write(hoge1)
            self.cnt = 1
        elif self.cnt == 1:
            self.ser1.write(hoge2)
            self.cnt = 0

        self.loop_cnt = self.loop_cnt + 1


    def rotator(self):
        self.norad_id_input.SetValue(self.norad_id_list[self.satellite_choice.GetSelection()])
        self.tracking_satellite.SetLabel(self.satellite_choiceChoices[self.satellite_choice.GetSelection()])

    def frame_close(self, event):
        try:
            stop_data = math.floor(1.01 * 100)
            hoge1 = stop_data.to_bytes(1,'little',signed=True)
            self.ser1.write(hoge1)
            self.Destroy()
        except:
            pass
        sys.exit()
