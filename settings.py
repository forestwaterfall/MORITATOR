import os
import serial.tools.list_ports


def init():
    if not os.path.exists('settings'):
        os.mkdir('settings')
    try:
        f = open('./settings/satellite.txt', 'x')
        sat_list = [ ['ISS', '25544'], ['NEXUS', '43937'], ['GRIFEX', '40379'], ['GRBAlpha', '47959'], ['Others', '33496'] ]
        for sat in sat_list:
            f.write(sat[0] + ',' + sat[1] + '\n')
        f.close()
    except:
        pass

    try:
        f = open('./settings/state.txt', 'x')
        f.write('0,COM0')
        f.close()
    except:
        pass

    try:
        f = open('./settings/background_sat.txt', 'x')
        f.write('')
        f.close()
    except:
        pass

def save_other_id(id):
    f = open('./settings/satellite.txt', 'r')
    lines = f.readlines()[0:-1]
    print(lines)
    f.close()
    f = open('./settings/satellite.txt', 'w')
    lines.append('Others,' + id)
    for line in lines:
        f.write(line)
    f.close()

def load_sat_list():
    f = open('./settings/satellite.txt', 'r')
    sat_list = []
    id_list = []
    lines = f.readlines()
    for line in lines:
        line = line.split('\n')[0]
        sat = line.split(',')
        print(sat)
        sat_list.append(sat[0])
        id_list.append(sat[1])
    f.close()
    return sat_list, id_list

def load_port_list():
    port_list = list(serial.tools.list_ports.comports())
    return port_list

def load_state():
    try:
        f = open('./settings/state.txt', 'r')
        sat_num, port = f.readline().split(',')
        sat_num = int(sat_num)
        print('sat',sat_num)
        f.close()
    except:
        sat_num = 0
        port = ''
    return sat_num, port

def save_state(sat_num, port):
    f = open('./settings/state.txt', 'w')
    f.write(str(sat_num) + ',' + port)
    f.close()

def load_background_sat_list():
    try:
        f = open('./settings/background_sat.txt', 'r')
        lines = f.readlines()
        f.close()
        bg_sat_list = []
        for line in lines:
            try:
                name, id = line.split(',')
                bg_sat_list.append([name, id])
            except:
                pass
    except:
        bg_sat_list = []
    return bg_sat_list
