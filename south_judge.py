import req
import ope_voltage
import orbit
import datetime
import math
import ephem
import numpy as  np
import time

def judgement(tle):
    cnt = 0
    south_t = 0
    flag = 0
    az1 = 0
    az2 = 0
    first_roop = 0

    utctime = datetime.datetime.utcnow()
    angle = orbit.cal_orbit(tle,utctime)
    utctime = datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")

    if angle[1] <= -1:
        now = datetime.datetime.utcnow()
        hirogari = ephem.readtle(tle[0], tle[1], tle[2])
        fudai = ephem.Observer()
        fudai.lat = '34.545898'
        fudai.lon = '135.503224'

        rise_t, az_rise, max_t, alt_max, set_t, az_set = fudai.next_pass(hirogari)

        t = ephem.Date(rise_t)
        ta = ephem.Date(rise_t)
        while ta < set_t:
            az1 = az2       #1つ前のアジマス角度
            tb = ta         #1つ前の時間
            ta = ephem.Date(rise_t + (1 * cnt * ephem.second))  #1秒ごとに時間を増やす

            fudai.date = ta
            hirogari.compute(fudai)
            az2 = hirogari.az * (180/3.1415)

            print(hirogari.az * (180/3.1415))

            if first_roop == 1:
                if az2 < 180 and 180 < az1:  #反時計回りで南を横切る
                    flag = 1
                elif az1 < 180 and 180 < az2: #時計回りで南を横切る
                    flag = 2

                if flag == 1 and (az2 < 165 and 165 < az1): #反時計回りの限界値
                    south_t = tb
                    flag = 3
                elif flag == 2 and (az1 < 186 and 186 < az2): #時計回りの限界値
                    south_t = tb
                    flag = 4

            first_roop = 1
            cnt = cnt + 1

        all_pass = ta - t
        start_time = t
        finish_time = ta

        if flag == 3 or flag == 4:          #南を横切り、かつローテータの限界値も超えるとき
            before_south = south_t - t
            after_south = ta - south_t

            if before_south < after_south:
                start_time = south_t
                finish_time = ta
            elif after_south < before_south:
                start_time = t
                finish_time = south_t

        start_time = ephem.localtime(rise_t)
        return start_time,finish_time

    else:
        now = datetime.datetime.utcnow()
        hirogari = ephem.readtle(tle[0], tle[1], tle[2])
        fudai = ephem.Observer()
        fudai.lat = '34.545898'
        fudai.lon = '135.503224'

        rise_t, az_rise, max_t, alt_max, set_t, az_set = fudai.next_pass(hirogari)
        start_time = ephem.localtime(rise_t)
        return start_time,0
