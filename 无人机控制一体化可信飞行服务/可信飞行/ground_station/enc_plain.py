import os
import base64
import subprocess

def enc_tpm(msg):
    file = open('plain.txt', 'w', encoding='UTF-8')
    # f2 = open('data123.encrypted', 'wb')
    file.write(msg)
    file.close()
    subprocess.getoutput('tpm2_rsaencrypt -c key.ctx -o data.encrypted plain.txt')
    enc_file = 'data.encrypted'
    size = os.path.getsize(enc_file)
    # print(size)
    enc_msg=''
    with open(enc_file,'rb') as f:
        for i in range(size):
            data = f.read(1)  # 每次输出一个字节
            # print(data)
            enc_msg = enc_msg + str(base64.b64encode(data), encoding="utf-8")

    # for j in range(0, len(enc_msg), 4):
    #     res = base64.decodebytes(enc_msg[j:j+4].encode('utf-8'))
    #     f2.write(res)
    # f2.close()
    subprocess.getoutput('sudo rm -rf plain.txt data.encrypted')
    return enc_msg


if __name__ == '__main__':
    msg = 'xwq12345'
    print(enc_tpm(msg))
    # filepath = 'data.encrypted'
    # binfile = open(filepath, 'rb')  # 打开二进制文件
    # size = os.path.getsize(filepath)  # 获得文件大小
    # for i in range(size):
    #     data = binfile.read(1)  # 每次输出一个字节
    #     print(data)
    # binfile.close()
    # res = str(base64.b64encode(b'\r'), encoding="utf-8")
    # print(res)
    # res2 = base64.decodebytes(res.encode('utf-8'))
    # print(res2)
    # s = 'xwq123123sqsqwxq'
    # for i in range(0,len(s),4):
    #     print(s[i:i+4])
