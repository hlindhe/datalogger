import serial
import time
running = True
ser = serial.Serial('/dev/ttyUSB0',115200)

try:
    print "Application started!"
    while running:
        w=ser.in_waiting
        print w
        if w > 0:
            sl=ser.readline()
            print sl
        else:
            print "."
            time.sleep(0.01)

except (KeyboardInterrupt):
    running = False
    print "Applications closed!"






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
