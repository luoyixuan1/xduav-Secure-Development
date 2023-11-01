import subprocess
subprocess.getoutput('tpm2_createprimary -C o -g sha256 -G rsa -c primary.ctx')
subprocess.getoutput('tpm2_startauthsession -S session.dat')
subprocess.getoutput('tpm2_policycommandcode -S session.dat -L dpolicy.dat TPM2_CC_Duplicate')
subprocess.getoutput('tpm2_flushcontext session.dat')
subprocess.getoutput('rm session.dat')
subprocess.getoutput('tpm2_create -C primary.ctx -g sha256 -G rsa -p foo -r key.prv \
-u key.pub  -L dpolicy.dat -a "sensitivedataorigin|userwithauth|decrypt|sign"')

subprocess.getoutput('tpm2_load -C primary.ctx -r key.prv -u key.pub -c key.ctx')
subprocess.getoutput('tpm2_readpublic -c key.ctx -o dup.pub')
subprocess.getoutput('tpm2_startauthsession --policy-session -S session.dat')
subprocess.getoutput('tpm2_policycommandcode -S session.dat -L dpolicy.dat TPM2_CC_Duplicate')
subprocess.getoutput('tpm2_loadexternal -C o -u new_parent.pub -c new_parent.ctx')
subprocess.getoutput('tpm2_duplicate -C new_parent.ctx -c key.ctx -G null  \
-p "session:session.dat" -r dup.dpriv -s dup.seed')
subprocess.getoutput('chmod 777 dup.dpriv dup.seed dup.pub')

# usr = 'pi'
# host = '192.168.1.102'
# path = ':~/mytest/'
# subprocess.getoutput('scp dup.dpriv dup.seed dup.pub ' + usr + '@' + host + path)