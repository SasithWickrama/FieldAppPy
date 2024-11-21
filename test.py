import subprocess
import os
import re
from datetime import datetime
import const
import hashlib
import base64


def hash_generate(password_text):
    salt = os.urandom(8)
    hashed_password = hashlib.sha1(password_text.encode('utf-8') + salt).digest()
    final_hash = base64.b64encode(hashed_password + salt).decode('utf-8')
    return "{SSHA}" + final_hash
    
    
cdate = datetime.now().strftime('%Y%m%d %H:%M:%S')
repdesc = 'Modify Passwd using FieldApp on '+cdate

xmlfile = open('files/modifypw.ldif', 'r')
body = xmlfile.read()

password_text = "94112421563"
ldap_hash = hash_generate(password_text)

indata = {"uidrep": "94112421563", "repdesc": repdesc, "bbPasswd" : ldap_hash}
for key in indata:
    value = indata[key]
    body = body.replace(key, value)

print(body)




filename = '94112421563.ldif'
fh = open(filename, 'w')
fh.write(body)
fh.close()

cmdexe=subprocess.run(["ldapmodify -h "+const.ldapip+" -D uid="+const.ldapusr+",cn=config -w "+const.ldappwd+" -f "+filename], shell=True, stdout=subprocess.PIPE)


#cmd = '"ldapmodify -h '+const.ldapip+' -D \"uid='+const.ldapusr+',cn=config\" -w \"'+const.ldappwd+'\" -f '+filename+'"'
#print(cmd)
#cmdexe = subprocess.run([cmd], shell=True, stdout=subprocess.PIPE)

#cmdexe = subprocess.Popen('"ldapmodify -h '+const.ldapip+' -D \"uid='+const.ldapusr+',cn=config\" -w \"'+const.ldappwd+'\" -f '+filename+'"', shell=True, stdout=subprocess.PIPE)
print("1=========")
print(cmdexe.returncode)
print("2=========")
result = cmdexe.stdout
print(result)

#for line in result:
#   print(line.decode('UTF-8'))

os.remove(filename)

