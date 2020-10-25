#!/usr/bin/python3

import serial
import time
import pprint
import string
import json
import os
import paho.mqtt.client as mqtt
import socket


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

running = True


mqttclient = mqtt.Client()
mqttclient.connect("localhost")
mqttclient.loop_start()

ser = serial.Serial('/dev/ttyUSB0',115200)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_data(data,port):
    sock.sendto(data,("127.0.0.1",port))
    return

def send_bmp(data):
    #5572
    send_data(bytes(json.dumps(data),"utf-8"),5572)
    return
    
def send_mpu(data):
    #5573
    send_data(bytes(json.dumps(data),"utf-8"),5573)
    return

def send_mpl(data):
    #5574
    send_data(bytes(json.dumps(data),"utf-8"),5574)
    return

def send_wifi(data):
    #5575
    send_data(bytes(json.dumps(data),"utf-8"),5575)
    return

def send_gps(data):
    #5576
    return

def process_bmp(data):
    kv=dict()
    dv=data.split(",")
    if len(dv)==3:
        mqttclient.publish("bmp180/temperature",float(dv[0]))
        mqttclient.publish("bmp180/pressure",float(dv[1]))
        mqttclient.publish("bmp180/altitude",float(dv[2]))
#        kv['temperature']=float(dv[0])
#        kv['pressure']=float(dv[1])
#        kv['altitude']=float(dv[2])
#        kv['sensor']='bmp180'
#        kv['ts']=time.time()
#        send_bmp(kv)
    return

def process_mpu(data):
    kv=dict()
    dv=data.split(",")
    if len(dv)==7:
        mqttclient.publish("mpu6050/accelerometer_x",float(dv[0]))
        mqttclient.publish("mpu6050/accelerometer_y",float(dv[1]))
        mqttclient.publish("mpu6050/accelerometer_z",float(dv[2]))
        mqttclient.publish("mpu6050/gyroscope_x",float(dv[3]))
        mqttclient.publish("mpu6050/gyroscope_y",float(dv[4]))
        mqttclient.publish("mpu6050/gyroscope_z",float(dv[5]))
        mqttclient.publish("mpu6050/temperature",float(dv[6]))
#        kv['accelerometerx']=float(dv[0])
#        kv['accelerometery']=float(dv[1])
#        kv['accelerometerz']=float(dv[2])
#        kv['gyroscopex']=float(dv[3])
#        kv['gyroscopey']=float(dv[4])
#        kv['gyroscopez']=float(dv[5])
#        kv['temperature']=float(dv[6])
#        kv['sensor']='mpu6050'
#        kv['ts']=time.time()
#        send_mpu(kv)
    return

def process_mpl(data):
    kv=dict()
    dv=data.split(",")
    if len(dv)==2:
        mqttclient.publish("mpl3115a2/altitude",float(dv[0]))
        mqttclient.publish("mpl3115a2/temperature",float(dv[1]))
#        kv['altitude']=float(dv[0])
#        kv['temperature']=float(dv[1])
#        kv['sensor']='mpl3115a2'
#        kv['ts']=time.time()
#        send_mpl(kv)
    return

def process_wifi(data):
    dv=data.split("|")
    wv=dict()
    i=0
    for s in range(int(len(dv)/5)):
        mqttclient.publish("esp8266wifi/"+dv[s*5+2]+"/ssid",dv[s*5])
        mqttclient.publish("esp8266wifi/"+dv[s*5+2]+"/rssi",dv[s*5+1])
        mqttclient.publish("esp8266wifi/"+dv[s*5+2]+"/channel",dv[s*5+3])
        mqttclient.publish("esp8266wifi/"+dv[s*5+2]+"/encryption",dv[s*5+4])
#        kv = dict()        
#        kv['ssid']=dv[s*5]
#        kv['rssi']=int(dv[s*5+1])
#        kv['bssid']=dv[s*5+2]
#        kv['channel']=dv[s*5+3]
#        kv['encryption']=dv[s*5+4]
#        kv['sensor']='esp8266wifi'
#        kv['ts']=time.time()
#        wv[i]=kv
#        i=i+1
#    send_wifi(wv)
    return


try:
    print("Application started!")
    while running:
        sl=ser.readline().rstrip().decode()
        sv=sl.split("\t",1)
        if len(sv)==2:
            if sv[0]=="BMP":
                process_bmp(sv[1])
            elif sv[0]=="MPU":
                process_mpu(sv[1])
            elif sv[0]=="MPL":
                process_mpl(sv[1])
            elif sv[0]=="WIFI":
                process_wifi(sv[1])
            else:
                print("okänd")
        else:
            print(sv)

except (KeyboardInterrupt):
    running = False
    print("Applications closed!")






#<dictwrapper: {u'epx': 10.465, u'epy': 12.295, u'track': 0.0, u'ept': 0.005, u'lon': 11.988043333
#, u'eps': 24.59, u'lat': 58.556681667, u'mode': 2, u'time': u'2020-06-07T20:20:38.000Z', u'device': u'/dev/ttyACM0', u'speed': 0.0, u'class': u'TPV'}>
#<dictwrapper: {u'epx': 10.465, u'epy': 12.295, u'epv': 43.7, u'ept': 0.005, u'lon': 11.988043333
#, u'eps': 24.59, u'lat': 58.556681667, u'track': 0.0, u'mode': 3, u'time': u'2020-06-07T20:20:38.000Z', u'device': u'/dev/ttyACM0', u'alt': 104.4, u'speed': 0.0, u'class': u'TPV'}>

# epx, epy, epv, eps
# lon, lat, alt, speed
# track, mode




#<dictwrapper: {u'gdop': 2.57, u'tdop': 1.21, u'vdop': 1.9, u'hdop': 1.0, u'pdop': 2.2, 
#u'satellites': [<dictwrapper: {u'ss': 7, u'el': 18, u'PRN': 1, u'az': 153, u'used': False}>, <dictwrapper: {u'ss': 18, u'el': 7, u'PRN': 2, u'az': 317, u'used': False}>, <dictwrapper: {u'ss': 21, u'el': 63, u'PRN': 3, u'az': 103, u'used': True}>, <dictwrapper: {u'ss': 30, u'el': 61, u'PRN': 4, u'az': 187, u'used': True}>, <dictwrapper: {u'ss': 19, u'el': 36, u'PRN': 6, u'az': 303, u'used': True}>, <dictwrapper: {u'ss': 21, u'el': 29, u'PRN': 9, u'az': 215, u'used': True}>, <dictwrapper: {u'ss': 12, u'el': 8, u'PRN': 12, u'az': 334, u'used': True}>, <dictwrapper: {u'ss': 0, u'el': 8, u'PRN': 14, u'az': 49, u'used': False}>, <dictwrapper: {u'ss': 19, u'el': 27, u'PRN': 17, u'az': 244, u'used': True}>, <dictwrapper: {u'ss': 21, u'el': 34, u'PRN': 19, u'az': 266, u'used': True}>, <dictwrapper: {u'ss': 26, u'el': 38, u'PRN': 22, u'az': 105, u'used': True}>, <dictwrapper: {u'ss': 26, u'el': 10, u'PRN': 25, u'az': 1, u'used': True}>, <dictwrapper: {u'ss': 20, u'el': 29, u'PRN': 31, u'az': 53, u'used': False}>], 
#u'ydop': 0.82, u'xdop': 0.7, u'device': u'/dev/ttyACM0', u'class': u'SKY'}>


