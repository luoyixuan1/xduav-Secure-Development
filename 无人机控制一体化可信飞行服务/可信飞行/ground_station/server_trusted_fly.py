import socket
import sys
import enc_plain
import sign_plain
import json



def socket_service_data():

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0",PORT))  # 在不同主机或者同一主机的不同系统下使用实际ip
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    # 连接
    while True:
        print("Wait for Connection..................")
        sock, addr = s.accept()
        print(sock)
        print(addr)
        print('connected successfully...............')
        while True:
            try:
                # send data
                strvar = input("(x:,y:,z:,duration: ): ")
                plain = strvar
                strvar = strvar.split(' ')
                if (len(strvar) == 1 and plain.upper() != 'Q' and plain.upper() != 'L' and plain.upper() != 'F') or (len(strvar) != 1 and len(strvar) != 4):
                    print("wrong input\n")
                    continue
                enc_msg = enc_plain.enc_tpm(plain)
                print('enc：' + enc_msg)
                sign_msg = sign_plain.sign_tpm(enc_msg)
                print('sign：' + sign_msg)

                send_msg = {'enc': enc_msg, 'sign': sign_msg}
                msg = json.dumps(send_msg)
                if plain.upper() == 'Q' or plain.upper() == 'L':
                    sock.send(msg.encode('utf-8'))
                    break

                # sendmsg = {'x': int(strvar[0]), 'y': int(strvar[1]), 'z':int(strvar[2]), 'duration':int(strvar[3])}
                # print(msg)

                sock.send(msg.encode('utf-8'))

            except Exception as e:
                print(e)
                break
        # 关闭socket
        sock.close()


if __name__ == '__main__':
    # 初始化
    # name = socket.gethostname()
    # HOST = socket.gethostbyname(name)  # 获取阿里云服务器私网IP，使用ifconfig可查询
    PORT = 7000
    BUFSIZ = 2048
    # ADDR = (HOST, PORT)

    socket_service_data()
