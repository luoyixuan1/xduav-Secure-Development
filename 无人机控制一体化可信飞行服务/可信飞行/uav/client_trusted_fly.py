from pymavlink import mavutil
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import json
import sign_verify
import dec_tpm
import socket
import sys

def send_body_ned_velocity(vehicle, velocity_x, velocity_y, velocity_z, duration=0):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED, # frame Needs to be MAV_FRAME_BODY_NED for forward/back left/right control.
        0b0000111111000111, # type_mask
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # m/s
        0, 0, 0, # x, y, z acceleration
        0, 0)
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)


def fly_height(vehicle, takeoff_alt):
    while not vehicle.is_armable:
        time.sleep(1)
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    while not vehicle.armed:
        print('Waiting for arming...')
        time.sleep(1)
    vehicle.simple_takeoff(takeoff_alt)  # Take off to target altitude
    while True:
        print('Altitude: %d' % vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= takeoff_alt * 0.95:
            print('REACHED TARGET ALTITUDE')
            break
        time.sleep(1)

def sock_client_data(vehicle):
    # 连接
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(ADDR)
        print(conn)
    except socket.error as msg:
        print(msg)
        print(sys.exit(1))

    fly_in_air = False

    while True:
       try:
           res = conn.recv(BUFSIZ)
           msg = res.decode('utf-8')
           recvmsg = json.loads(msg)

           sign = recvmsg['sign']
           enc = recvmsg['enc']

           print('received sign：' + sign)
           print('received enc：' + enc)

           if sign_verify.sign_verify_tpm(enc, sign):
               print('identity attestation success！\nintegrity attestation success！')
               dec_msg = dec_tpm.dec_data(enc)
               order = dec_msg
               print('dec msg：' + dec_msg)

               '''
               if fly_in_air == False and dec_msg.upper() != "F":
                   fly_msg = 'please let uav takeoff first !'
                   print(fly_msg)
                   continue

               if fly_in_air and dec_msg.upper() == "F":
                   print('uav is in the air! Dot need to takeoff again!')
                   continue
               '''
               if fly_in_air == False and dec_msg.upper() == "F":
                   print('takeoff!!!')
                   takeoff_alt = 3
                   fly_height(vehicle,takeoff_alt)
                   fly_in_air = True
                   continue

               if dec_msg.upper() == "L":
                   vehicle.mode = VehicleMode("LAND")
                   print("start land")
                   break;
               if dec_msg.upper() == "Q":
                   print("client quit")
                   break

               dec_msg = dec_msg.split(' ')
               # print(dec_msg)
               velocity_x = int(dec_msg[0])
               velocity_y = int(dec_msg[1])
               velocity_z = int(dec_msg[2])
               duration = int(dec_msg[3])
               # print(duration)
               if velocity_x > 3 or velocity_y > 3 or velocity_z > 3:
                   print("Too fast\n")
                   continue
               if duration > 10:
                   print("Too long\n")
                   continue

               send_body_ned_velocity(vehicle,velocity_x, velocity_y, velocity_z, duration)
               print('Executing order:', order)
               time.sleep(duration)

           else:
               print('identity attestation failed！')
               continue

       except Exception as e:
           break

    # 关闭socket
    conn.close()


if __name__ == '__main__':
    # 初始化

    HOST = '43.136.136.199'  # 比如 99.100.101.102是你的服务器的公网IP
    PORT = 7000  # IP开放的socket端口
    BUFSIZ = 2048
    ADDR = (HOST, PORT)

    connection_string = '/dev/ttyACM0'  # Edit to suit your needs.   real
    # connection_string = '127.0.0.1:14551'
    vehicle = connect(connection_string, wait_ready=True)
    #vehicle = '123'
    sock_client_data(vehicle)
