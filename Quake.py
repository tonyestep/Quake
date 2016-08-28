# ACOS( SIN(LAT1*PI()/180)*SIN(LAT2*PI()/180) + COS(LAT1*PI()/180)*COS(LAT2*PI()/180)*COS(LON2*PI()/180-LON1*PI()/180) ) * 6371
# is distance in KM between two points (lat1, lon1) and (lat2, lon2)

import math

class quake:
    def __init__(self, dep, locat, whn, titl):
        self.depth = dep
        self.loc = locat
        self.when = whn
        self.title = titl

# put the following code in the main module:
#     qk = Quake.quake(depth,loc,upd,title)
#     print(upd,title,loc,depth)
#     quakeList.append(qk)
# for q in quakeList:
#     print(q.title)

#def distanceBetween(thisQuake, thatQuake):
thisQuake = '44,-90'
thatQuake = '40,-110'
thisCoords = thisQuake.split(',')
thatCoords = thatQuake.split(',')
lat1 = float(thisCoords[0])
lon1 = float(thisCoords[1])
lat2 = float(thatCoords[0])
lon2 = float(thatCoords[1])

dist=math.acos(math.sin(lat1*math.pi/180)* math.sin(
    lat2*math.pi/180) + math.cos(lat1*math.pi/180)*math.cos(
    lat2*math.pi/180)*math.cos(lon2*math.pi/180-lon1*math.pi/180)) * 6371

print(dist)
