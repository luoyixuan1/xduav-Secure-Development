import subprocess

def sign_tpm(enc_msg):
    file = open('enc_msg.txt', 'w', encoding='UTF-8')
    file.write(enc_msg)
    file.close()
    subprocess.getoutput('tpm2_sign -c key.ctx -g sha256 -f plain -p foo -o sign.raw enc_msg.txt')
    sign_msg = subprocess.getoutput('sha256sum sign.raw')
    subprocess.getoutput('sudo rm -rf sign.raw enc_msg.txt')
    return sign_msg


if __name__ == '__main__':
    msg = 'xwq'
    print(sign_tpm(msg))


