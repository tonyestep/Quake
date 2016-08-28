import xmltodict
import urllib.request
import sqlite3
import math
import re

def distanceBetween(thisQuake, thatQuake):
    # thisQuake = '44,-90'
    # thatQuake = '40,-110'
    thisCoords = thisQuake.split(' ')
    thatCoords = thatQuake.split(' ')
    lat1 = float(thisCoords[0])
    lon1 = float(thisCoords[1])
    lat2 = float(thatCoords[0])
    lon2 = float(thatCoords[1])

    dist = math.acos(math.sin(lat1 * math.pi / 180) * math.sin(
        lat2 * math.pi / 180) + math.cos(lat1 * math.pi / 180) * math.cos(
        lat2 * math.pi / 180) * math.cos(lon2 * math.pi / 180 - lon1 * math.pi / 180)) * 6371
    return ("{0:8.1f}".format(dist))

myLoc = ('38.63 -90.2', 'St. Louis')


url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.atom'
html = urllib.request.urlopen(url).read()
#html = open('c:/users/tony/documents/pythoncourse/usgs2.txt').read()
# conn = sqlite3.connect('quake.sqlite3')
# cur = conn.cursor()
# cur.execute('CREATE TABLE IF NOT EXISTS Quakes (title TEXT, upd TEXT, loc TEXT, depth TEXT)')

quake = xmltodict.parse(html)

dat = quake['feed']['entry']    # XMLtoDict is the only parser that correctly gets the tree struct
count = 0
quakeList = []
while count < 25:              #     len(dat):
    q = (dat[count])
    count = count+1
    # items = ['updated','title','georss:point','georss:elev']
    # for it in items:
    #     print (q[it], end = " ")
    # print()
    upd = q['updated']
    title = q['title']      # parse into Magnitude and description
    loc = q['georss:point']
    depth = q['georss:elev']
    dist = distanceBetween(loc, myLoc[0])
    mag = re.findall('^M ([0-9.]+)', title)
    descr = re.findall(mag[0]+'\s+-\s(.*)', title)
    print ('Mag',mag[0]," ", descr[0],':', loc,',', dist,'km. from', myLoc[1], 'depth = ', depth)

#     cur.execute('INSERT INTO Quakes (title, upd, loc, depth) VALUES(?,?,?,?)',(title, upd, loc, depth))
#
# print('Quakes:')
# cur.execute('SELECT * FROM Quakes')
# for row in cur:
#     print (row)
# cur.close()


