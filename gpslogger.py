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

def processgps():
    update=gps.next()
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
        print(gw)
        if gw:
            processgps()
        time.sleep(0.001)

except (KeyboardInterrupt):
    running = False
    print("Applications closed!")









    # For a list of all supported classes and fields refer to:
    # https://gpsd.gitlab.io/gpsd/gpsd_json.html
