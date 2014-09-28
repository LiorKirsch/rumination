'''
Created on Mar 16, 2014

@author: noam
'''

from pymaps import Map, PyMap, Icon # import the libraries
import urllib
import os
import pickle
import time
import json
from path3 import path


FOLDERS = ('/Users/noampeled/Dropbox/postDocMoshe/rumination/MasonWordsSite/MasonWordsSite/logs/serverLogs/amt2', 
           '/home/noam/Dropbox/postDocMoshe/rumination/MasonWordsSite/MasonWordsSite/logs/amt1/',
           '/Users/daryarfrank/Dropbox/BarLab/MasonWordsSite/MasonWordsSite/logs/serverLogs')
BASE_DIR = [f for f in FOLDERS if os.path.exists(f)][0]
POINTS_FILE = 'ipsInfo_amt2.pkl'
MAP_FILE = 'map_amt.html'
GOOGLE_KEY = "ABQIAAAAQQRAsOk3uqvy3Hwwo4CclBTrVPfEE8Ms0qPwyRfPn-DOTlpaLBTvTHRCdf2V6KbzW7PZFYLT8wFD0A"      # set your google key

'notasecret'
# https://code.google.com/p/google-api-php-client/wiki/OAuth2
# https://console.developers.google.com/project/104607357812/apiui/credential

def createIcon():
    icon = Icon('icon2')               # create an additional icon
    icon.image = "http://labs.google.com/ridefinder/images/mm_20_blue.png" # for testing only!
    icon.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png" # do not hotlink from your web page!
    return icon

def addPoint(tmap, gmap, lat_coo, long_coo, hover_text=''):
    icon = createIcon()
    point = (lat_coo, long_coo, hover_text, icon.id)
    tmap.setpoint(point)
    gmap.addicon(icon)

def createMap(zoom=3):
    # Create a map - pymaps allows multiple maps in an object
    tmap = Map()
    tmap.zoom = zoom
    return tmap

def createhtml(mapCode):
    """returns a complete html page with a map"""
    
    html = """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
        <title></title>
        %s
        </head>
        
        <body onload="load()" onunload="GUnload()">
        <div id="map" style="width: 1000px; height: 700px"></div>
        </body>
        </html>
        """ % (mapCode)
    return html

def createPointsMap():
    tmap = createMap(zoom=2)
    tmap.center = (1.757537,144.492188)
    gmap = PyMap(key=GOOGLE_KEY, maplist=[tmap])
    with open(POINTS_FILE, 'r') as pointsFile:
        points = pickle.load(pointsFile)
        print('Create a map for {} subject'.format(len(points)))
        for ip,lat,lan,data,uuid in points:
            addPoint(tmap, gmap, lat, lan, getDemographicDetails(uuid)) 
        mapCode = gmap.pymapjs()
        html = createhtml(mapCode)
        with open(MAP_FILE,'wb') as mapFile:
            mapFile.write(html)

def getDemographicDetails(uuid):
    fileName = os.path.join(BASE_DIR, '{}_{}.pkl'.format(uuid,'demographic'))
    text = uuid
    try:
        with open(fileName, 'r') as pklFile:
            log = pickle.load(pklFile)
            text = ', '.join(['{}: {}'.format(key,val) for key,val in sorted(log.iteritems())])
    except:
        print('error with {}'.format(uuid))
    return text

def saveIPsInfo():
    uuids = getuuids()
    uuidsWithIP, points = getuuidWithIP()
    for uuid in uuids-set(uuidsWithIP):
        fileName = os.path.join(BASE_DIR, '{}_{}.pkl'.format(uuid,'ip'))  
        try:
            with open(fileName, 'r') as pklFile:
                log = pickle.load(pklFile)
                ip = log['ip']
                lat,lan, data = getLatLonFromIP(ip)
                if (lat and lan): # Check lat and lan aren't None
                    points.append((ip,lat,lan,data,uuid))
                    print('data saved for {}'.format(uuid))
                time.sleep(1)
        except:
            print ('No ip file for {}'.format(uuid))
            print(path(BASE_DIR).files('{}*.pkl'.format(uuid)))
    
    with open(POINTS_FILE, 'w') as pklFile:
        pickle.dump(points, pklFile)

def getuuidWithIP():
    try:
        with open(POINTS_FILE, 'r') as pointsFile:
            points = pickle.load(pointsFile)
            uuids = set([p[-1] for p in points])
    except:
        uuids, points = [],[]
    return uuids,points

def getuuids():
#     return set(f.name[:5] for f in path(BASE_DIR).files('*.pkl')) 
    return set(f.name[:5] for f in path(BASE_DIR).files('*feedback.pkl')) 


def getLatLonFromIP(ip):
    try:
        resp = urllib.urlopen('http://ipinfo.io/{}/json'.format(ip)).read()
        data = json.loads(resp)
        if (data.get('loc','')!=''):    
            lat,lng = data['loc'].split(',')
            return (lat,lng,data)
    except:
        pass
    
    return None,None,None

if __name__ == '__main__':
#     open('test.htm','wb').write(showhtml())   # generate test file
#     saveIPsInfo()
    createPointsMap()
#     response = urllib.urlopen('http://api.hostip.info/get_json.php?ip=12.215.42.19&position=true').read()
#     print(response)
    print('finish!')
