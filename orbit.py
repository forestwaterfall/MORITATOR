import math
import ephem
import datetime

def cal_orbit(tle,time):
    fudai = ephem.Observer()
    fudai.lat = '34.545898'
    fudai.lon = '135.503224'
    fudai.date = time

    hirogari = ephem.readtle(tle[0],tle[1],tle[2])

    hirogari.compute(fudai)
    az = hirogari.az * (180/3.1415)
    alt = hirogari.alt * (180/3.1415)
    angle = [az,alt]
    return angle

if __name__ == '__main__':
    cal_orbit()
