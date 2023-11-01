import subprocess

usr = 'ubuntu'
host = '43.136.136.199'
path = ':~/trusted_fly/'
subprocess.getoutput('scp ' + usr + '@' + host + path+'dup* .')