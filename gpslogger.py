#!/usr/bin/python2

import serial
import time
import pprint
import string
import json
import os
import paho.mqtt.client as mqtt
import socket
from gps import *
import time


last_tpv={}
def processgps_tpv(update):
    for k in update.keys():
        if not last_tpv.has_key(k):
            last_tpv[k]=""
        if last_tpv[k] != update[k]:
            mqttclient.publish("gps/"+k,update[k])
            last_tpv[k] = update[k]


last_sky={}
def processgps_sky(update):
    for k in update.keys():
        if k=='satellites':
            for k2 in update['satellites']:
                for k3 in k2.keys():
                    key="gpssky."+str(k2['PRN'])+"."+k3
                    if not last_sky.has_key(key):
                        last_sky[key]=""
                    if last_sky[key] != k2[k3]:
                        mqttclient.publish("gpssky/"+str(k2['PRN'])+"/"+k3,k2[k3])
                        last_sky[key] = k2[k3]
        else:
            if not last_sky.has_key(k):
                last_sky[k]=""
            if last_sky[k] != update[k]:
                mqttclient.publish("gpssky/"+k,update[k])
                last_sky[k]=update[k]



def processgps():
    update=gps.next()
    if update['class'] == 'TPV':
        processgps_tpv(update)
    elif update['class'] == 'SKY':
        processgps_sky(update)
    else:
        print(update)



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

running = True

mqttclient = mqtt.Client()
mqttclient.connect("localhost")
mqttclient.loop_start()

gps = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

#mqttclient.publish("bmp180/temperature",float(dv[0]))


try:
    print("Application started!")
    while running:
        gw = gps.waiting()
        #print(gw)
        if gw:
            processgps()
        time.sleep(0.001)

except (KeyboardInterrupt):
    running = False
    print("Applications closed!")









    # For a list of all supported classes and fields refer to:
    # https://gpsd.gitlab.io/gpsd/gpsd_json.html
