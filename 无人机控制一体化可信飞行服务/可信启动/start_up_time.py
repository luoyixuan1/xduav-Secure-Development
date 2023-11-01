import serial, threading, time, os
import platform
import hashlib
import ctypes
from concurrent.futures import ThreadPoolExecutor
import os
import subprocess

x = serial.Serial('/dev/ttyACM0', 19200, timeout=1)


def faSong():  # 0x66 0x20
    myinput = bytes([0x66, 0x20])
    x.write(myinput)
    print("机载计算机正在向飞控发送指令，请求计算飞控硬件和固件的hash值")


def jieShou():
    while True:
        begin_time = time.time()
        while x.inWaiting() > 0:
            myout = x.read(6)
            datas = ''.join(map(lambda x: ('/x' if len(hex(x)) >= 4 else '/x0') + hex(x)[2:], myout))
            new_datas = datas[2:].split('/x')
            need = ''.join(new_datas)
            if need == "1210":
                continue
            else:
                res = hashlib.sha1()
                res.update(need.encode('utf-8'))
                print("机载计算机，接收到飞控硬件和固件的hash结果值：" + res.hexdigest())
                plat = platform.uname()
                tmp = hashlib.sha1()
                tmp.update(str(plat).encode('utf-8'))
                print("机载计算机的hash结果值：" + tmp.hexdigest())
                res.update(str(plat).encode('utf-8'))
                print("机载计算机与飞控混合计算出最终的hash值：" + res.hexdigest())
                print("将最终的hash值，与TPM模块中的预先值，进行比对验证中")
                # 设置正确值
                # subprocess.Popen(['tpm2_pcrextend', '2:sha1=' + 'a58d927484793410521d4191fcf354db62c0f4b1'],stdout=subprocess.PIPE).stdout
                # tpm2_pcrreset 23   清空23号寄存器
                subprocess.Popen(['tpm2_pcrreset', '23'], stdout=subprocess.PIPE).stdout

                # 设置23号寄存器   这次启动时的度量值
                subprocess.Popen(['tpm2_pcrextend', '23:sha1=' + res.hexdigest()], stdout=subprocess.PIPE).stdout
                # subprocess.Popen(['tpm2_pcrextend', '23:sha1='+'a58d927484793410521d4191fcf354db62c0f4b1'], stdout=subprocess.PIPE).stdout

                # 读取pcr寄存器的值
                # 此次值
                read_value = subprocess.Popen(['tpm2_pcrread', 'sha1:23'], stdout=subprocess.PIPE).communicate()
                value1 = str(read_value[0])[19:-3]
                print("将此次开机启动的摘要值，扩展到TPM的PCR寄存器中，并进行读取PCR值,PCR_Value: " + value1)
                # 预期值
                true_value = subprocess.Popen(['tpm2_pcrread', 'sha1:2'], stdout=subprocess.PIPE).communicate()
                value2 = str(true_value[0])[19:-3]
                print("TPM模块中预先设定的正确的开机度量值,True_Value: " + value2)

                # 元组之间的比较
                if value1 == value2:
                    # if need == "121069d83186":  # 121069d83186  成功
                    print(">>> 【验证成功】，机载计算机开始向飞控发送指令，请求启动飞行！")
                    myinput2 = bytes([0x67, 0x20])
                    x.write(myinput2)
                    print(">>> 启动成功！")
                    end_time = time.time()
                    print("【整个过程运行时间】：", end_time - begin_time)
                    os._exit(0)
                else:
                    print(">>>  【验证失败】，无法正常启动！")
                    end_time = time.time()
                    print("【整个过程运行时间】：", end_time - begin_time)
                    os._exit(0)


if __name__ == '__main__':
    # pool = ThreadPoolExecutor(max_workers=10)
    # task_jie = pool.submit(jieShou)
    # task_fa = pool.submit(faSong)
    # res = task_jie.result()
    # print(res)
    t1 = threading.Thread(target=jieShou)
    t2 = threading.Thread(target=faSong)
    myinput = bytes([0x66, 0x20])
    x.write(myinput)
    # time.sleep(0.5)
    t2.start()

    t1.start()
