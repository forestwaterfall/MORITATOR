import requests
import math
import ephem
import datetime
import sys
#iss 25544
#nexus 43937                 437.075
#himawari 41836
#QUEZZAL-1 45598
#QARMAN 45263
#AZTECHSAT-1 45261
#JALSAT 1 44419
#AIST 2D 41465
#SRMSAT 37841
#UGUISU 44331
#DUCHIFAT-3  44854
#SEEDS 32791                437.485
#STEP CUBE LAB 43138　
#AAUSAT-4  41460
#SPRoUT    39770            437.525
#NANOSAT   40024            145.865
#JAS 2(FO-29)               435.795
#XW-2C     40906            145.770/145.790
#BIRD-PH(MAYA-1)  43590     145.825/437.375
#ZHUHAI-1 01(CAS 4A)  42761  145.855
#DIWATA 2B(PO-101)   43678   145.900

def read_TLE(cat_id):
    try:
        r = requests.post("https://celestrak.org/satcat/tle.php?CATNR="+str(cat_id))
        tle = r.text.split("\r\n")[:3]
        if tle[1][0] != '1':
            raise ValueError("TLE EMPTY")
    except:
        f = open('./settings/HIROGARI_TLE.txt','r')
        tle = f.readlines()
        f.close()
    if str(cat_id) == '47930' and backup_flag:
        f = open('./settings/HIROGARI_TLE.txt','w')
        f.write(''.join(tle))
        f.close()
    return tle
