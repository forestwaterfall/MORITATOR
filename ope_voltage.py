from datetime import datetime
#import sel
import orbit
from pyorbital.orbital import Orbital
import ephem
import numpy as  np

def cal_voltage(angle,tle):
    #When the satellite is out of range
    if angle[1] <= -0.5:
        now = datetime.utcnow()
        #Calculate the next time the satellite appears
        hirogari = ephem.readtle(tle[0], tle[1], tle[2])
        fudai = ephem.Observer()
        fudai.lat = '34.545898'
        fudai.lon = '135.503224'
        fudai.date = now
        rise_t, az_rise, max_t, alt_max, set_t, az_set = fudai.next_pass(hirogari)
        return rise_t

        if 165 < angle[0] and angle[0] <= 180:
            angle[0] = angle[0] - 360
            azi_volt = 4.995117   #20210318
        elif 110 < angle[0] and angle[0] <= 160:
            azi_volt = -2 * (10 ** (-5)) * (angle[0] ** 2) + 0.0076 * angle[0] + 4.1908
        elif 100 < angle[0] and angle[0] <= 110:
            azi_volt = 0.0051 * angle[0] + 4.276   #20210318
        elif 0 <= angle[0] and angle[0] <= 100:
            azi_volt = 0.0159 * angle[0] + 3.2073   #20210318
        else:
            azi_volt = 0.0161 * angle[0] - 2.5656

        if angle[1] <= 65:
            ele_volt = 0.0646 * angle[1] + 0.3824
        elif 65 < angle[1] and angle[1] <= 90:
            ele_volt = 0.0006 * (angle[1] ** 2) + 0.1114 * angle[1] -0.0284

        voltage = [azi_volt, ele_volt]
        return voltage

if __name__ == '__main__':
    cal_voltage()
