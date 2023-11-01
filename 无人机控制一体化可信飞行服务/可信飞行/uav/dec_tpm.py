import subprocess
import base64


def dec_data(enc_msg):
    f = open('data.encrypted','wb')
    for i in range(0,len(enc_msg),4):
        s1 = enc_msg[i:i+4]
        f.write(base64.decodebytes(s1.encode('utf-8')))
    f.close()
    subprocess.getoutput('tpm2_flushcontext --transient-object')
    plain_data = subprocess.getoutput('tpm2_rsadecrypt -p foo -c dup.ctx data.encrypted')
    subprocess.getoutput('sudo rm -rf data.encrypted')
    return plain_data
