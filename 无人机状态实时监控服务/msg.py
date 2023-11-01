import socket
import json
from pymavlink import mavutil
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import csv
from threading import Thread, Timer
from geopy.distance import geodesic
import datetime
import subprocess
import math

SEND_DATA = 'send_data'

def input_client_name():
    return input("please input uav name :")

def send_data(client, cmd, uav_info):
    msg = {CMD: cmd, 'client_name': client_name, 'uav_info': uav_info}
    msg[TIME] = time.time()
    client.sendall(json.dumps(msg).encode('utf8'))

def realtime_msg(vehicle):

    uav_info = "========================================================================" +'\n'\
               "Real-Time：%s" % time.strftime('%a %b %d %H:%M:%S %Y', time.localtime())+'\n'\
               "Autopilot Firmware version: %s" % vehicle.version+'\n'\
               "Autopilot capabilities (supports ftp): %s" % vehicle.capabilities.ftp+'\n'\
               "Global Location: %s" % vehicle.location.global_frame+'\n'\
               "Global Location (relative altitude): %s" % vehicle.location.global_relative_frame+'\n'\
               "Local Location: %s" % vehicle.location.local_frame +'\n'\
               "Attitude: %s" % vehicle.attitude+'\n'\
               "Velocity: %s" % vehicle.velocity+'\n'\
               "GPS: %s" % vehicle.gps_0+'\n'\
               "Groundspeed: %s" % vehicle.groundspeed+'\n'+\
               "Airspeed: %s" % vehicle.airspeed+'\n'+\
               "Gimbal status: %s" % vehicle.gimbal+'\n'+\
               "Battery: %s" % vehicle.battery+'\n'+\
               "EKF OK?: %s" % vehicle.ekf_ok+'\n'+\
               "Last Heartbeat: %s" % vehicle.last_heartbeat+'\n'+\
               "Rangefinder: %s" % vehicle.rangefinder+'\n'+\
               "Rangefinder distance: %s" % vehicle.rangefinder.distance+'\n'+\
               "Rangefinder voltage: %s" % vehicle.rangefinder.voltage+'\n'+\
               "Heading: %s" % vehicle.heading+'\n'+\
               "Is Armable?: %s" % vehicle.is_armable+'\n'+\
               "System status: %s" % vehicle.system_status.state+'\n'+\
               "Mode: %s" % vehicle.mode.name +'\n'+\
               "Armed: %s" % vehicle.armed # settable
    send_data(client, SEND_DATA, uav_info)

if '__main__' == __name__:
    HOST = '192.168.1.100'  # 比如 99.100.101.102是你的服务器的公网IP
    PORT = 8713  # IP开放的socket端口
    ADDR = (HOST, PORT)

    client_name = input_client_name()
    client = socket.socket()
    client.connect(ADDR)
    print(client.recv(2048).decode(encoding='utf8'))
    send_data(client, CONNECT, 'success')
    connection_string = '/dev/ttyACM0'  # Edit to suit your needs.   real
    # connection_string = '127.0.0.1:14551'
    vehicle = connect(connection_string, wait_ready=True)
    while True:
        try:
            realtime_msg(vehicle)
            time.sleep(1)
        except Exception as e:
            print(e)
            break


