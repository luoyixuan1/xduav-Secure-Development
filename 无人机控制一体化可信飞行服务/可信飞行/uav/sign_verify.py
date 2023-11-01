import subprocess
def sign_verify_tpm(enc, sign):
    file = open('file.txt', 'w', encoding='UTF-8')
    file.write(enc)
    file.close()
    subprocess.getoutput('tpm2_sign -c dup.ctx -g sha256 -o sig.rss -p foo file.txt')
    subprocess.getoutput('dd if=sig.rss of=sign.raw bs=1 skip=6 count=256')
    sign2 = subprocess.getoutput('sha256sum sign.raw')
    subprocess.getoutput('sudo rm -rf sign.raw file.txt')
    return sign2 == sign
