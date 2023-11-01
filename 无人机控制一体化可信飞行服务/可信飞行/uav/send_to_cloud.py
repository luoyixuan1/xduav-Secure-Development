import subprocess

usr = 'ubuntu'
host = '43.136.136.199'
path = ':~/trusted_fly/'
subprocess.getoutput('scp new_parent.pub ' + usr + '@' + host + path )