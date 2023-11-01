import subprocess
subprocess.getoutput('tpm2_startauthsession --policy-session -S session.dat')
subprocess.getoutput('tpm2_policycommandcode -S session.dat -L dpolicy.dat TPM2_CC_Duplicate')
subprocess.getoutput('tpm2_flushcontext --transient-object')
subprocess.getoutput('tpm2_load -C primary.ctx -u new_parent.pub -r new_parent.prv -c new_parent.ctx')
subprocess.getoutput('tpm2_import -C new_parent.ctx -u dup.pub -i dup.dpriv \
-r dup.prv -s dup.seed -L dpolicy.dat')
subprocess.getoutput('tpm2_flushcontext --transient-object')
subprocess.getoutput('tpm2_load -C new_parent.ctx -u dup.pub -r dup.prv -c dup.ctx')