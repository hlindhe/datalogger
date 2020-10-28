#!/usr/bin/python3

import time
import pprint
import string
import json
import os
import subprocess
import paho.mqtt.client as mqtt
import socket


def cpu_temp():
    x=subprocess.check_output(["vcgencmd","measure_temp"])
    if len(x)>5:
        x1=x.decode(encoding='ASCII').split("=")
        x2=x1[1].split("'")
        mqttclient.publish("raspberrypi/cputemp",float(x2[0]))
    return

def get_throttled():
    x=subprocess.check_output(["vcgencmd","get_throttled"])
    if len(x)>5:
        x1=x.decode(encoding='ASCII').split("=")
        x2=x1[1].split("\n")
        mqttclient.publish("raspberrypi/throttled",x2[0])
    return


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

running = True


mqttclient = mqtt.Client()
mqttclient.connect("localhost")
mqttclient.loop_start()



try:
    print("Application started!")
    while running:
        cpu_temp()
        get_throttled()
        time.sleep(1)

except (KeyboardInterrupt):
    running = False
    print("Applications closed!")
