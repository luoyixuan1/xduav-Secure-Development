import subprocess
subprocess.getoutput('tpm2_createprimary -C o -g sha256 -G rsa -c primary.ctx')
subprocess.getoutput('tpm2_create  -C primary.ctx -g sha256 -G rsa \
-r new_parent.prv  -u new_parent.pub \
-a "restricted|sensitivedataorigin|decrypt|userwithauth"')
subprocess.getoutput('chmod 777 new_parent.pub')

# usr = 'pi'
# host = '192.168.1.102'
# path = ':~/test_for_sign/'
# subprocess.getoutput('scp new_parent.pub ' + usr + '@' + host + path)


