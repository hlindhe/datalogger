#!/usr/bin/python2

from gps import *
import serial
import time
from pprint import pprint
import string
import json
import os

import socket
import threading
import SocketServer

logpath='/run/user/1000/datalogger.txt'
running = True
ser = serial.Serial('/dev/ttyUSB0',115200)
gps = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

currentstatus = dict()

class MyUDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
#        print "{} wrote:".format(self.client_address[0])
        data = self.request[0].strip()
#        print data
        if data=="":
            data=" ".join(currentstatus.keys())
        else:
            if currentstatus.has_key(data):
                data = json.dumps(currentstatus[data])
            else:
                data = "{}"
        socket = self.request[1]
#        print "{} got:".format(self.client_address[0])
#        print data        
        socket.sendto(data, self.client_address)

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass

def processgps():
    update=gps.next()
    if update['class']=='TPV':
        processgpstpv(update)
    if update['class']=='SKY':
        processgpssky(update)

def processserial():
    #print "getting serial"
    sl = string.rstrip(ser.readline())
#    print sl
#    pprint(vars(gps.fix))
    sv = string.split(sl,":")
#    print len(sv)
    if len(sv)==2:
        if sv[0] == 'BMP':
            process_bmp(sv[1])
        if sv[0] == 'MPU':
            process_mpu(sv[1])
        if sv[0] == 'MPL':
            process_mpl(sv[1])
    if len(sv)>2:
        if sv[0] == 'WIFI':
            process_wifi(string.join(sv[1:999],":"))
#    print str(gps.fix.latitude) + "," + str(gps.fix.longitude) +","+ sl
#    pprint(vars(gps.fix))


def processgpstpv(g):
    if g['mode'] != 3:
        return
    # eh, do nothing
#    pprint(g)

def processgpssky(g):
    return
#    pprint(gps.satellites)

def process_wifi(data):
    dv=string.split(data,"|")
    wv = dict()
    i=0
    pts=time.time()
    for s in range(len(dv)/5):
        kv = dict()        
        kv['ssid']=dv[s*5]
        kv['rssi']=int(dv[s*5+1])
        kv['bssid']=dv[s*5+2]
        kv['channel']=dv[s*5+3]
        kv['encryption']=dv[s*5+4]
        kv['sensor']='esp8266wifi'
        do_log(kv)
        kv['pitimestamp']=pts
        wv[i]=kv
        i=i+1
    currentstatus['wifi']=wv
    
    
def process_bmp(data):
    kv = dict()
    # ['26', '100730', '50']
    dv=string.split(data,",")
    if len(dv)==3:
        kv['temperature']=float(dv[0])
        kv['pressure']=float(dv[1])
        kv['altitude']=float(dv[2])
        kv['sensor']='bmp180'
        do_log(kv)

def process_mpl(data):
    kv = dict()
    # ['39.25', '26.19']
    dv=string.split(data,",")
    if len(dv) == 2:
        kv['altitude']=float(dv[0])
        kv['temperature']=float(dv[1])
        kv['sensor']='mpl3115a2'
        do_log(kv)

def process_mpu(data):
    kv=dict()
    #['0.87', '-1.70', '11.45', ' -0.05', '0.02', '0.02', ' 30.92']
    dv=string.split(data,",")
    if len(dv)==7:
        kv['accelerometerx']=float(dv[0])
        kv['accelerometery']=float(dv[1])
        kv['accelerometerz']=float(dv[2])
        kv['gyroscopex']=dv[3]
        kv['gyroscopey']=dv[4]
        kv['gyroscopez']=dv[5]
        kv['temperature']=dv[6]
        kv['sensor']='mpu6050'
    # pprint(dv)
        currentstatus[kv['sensor']]=kv
#    do_log(kv)


def do_log(kv):
    kv['gpsutc']=gps.utc
    kv['gpsreceived']=gps.received
    kv['pitimestamp']=time.time()
    kv['gpslatitude']=gps.fix.latitude
    kv['gpslongitude']=gps.fix.longitude
    kv['gpsaltitude']=gps.fix.altitude
    currentstatus[kv['sensor']]=kv
    f=open(logpath,'a')
    f.write(json.dumps(kv))
    f.write("\n")
    f.flush()
    os.fsync(f.fileno())
    f.close
    
#    print "%f" % time.time()
#    pprint(vars(gps.fix))
#    pprint(kv)

try:
    print "Application started!"
    server = ThreadedUDPServer(("localhost",18600), MyUDPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    while running:
        # kolla om gps har data
        gw=gps.waiting()
        #print "gw:" + str(gw)
        if gw == True:
            processgps()
        # kolla om serial har data
        sw=ser.in_waiting
        #print "sw:" + str(sw)
        if sw > 0:
            processserial()
        
        time.sleep(0.001)
    server.shutdown()
    server.server_close()

except (KeyboardInterrupt):
    running = False
    print "Applications closed!"
