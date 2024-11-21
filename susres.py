import os
import subprocess
from datetime import datetime
from log import Logger
from dotenv import load_dotenv

cdate = datetime.now().strftime('%Y%m%d')

loggersuspend = Logger('suspend', 'logs/suspend')
loggerresume = Logger('resume', 'logs/resume')

class SuspendResumed:
    def Suspend(self,ref):
        repdesc = 'Suspend using SR system on '+cdate

        if self['circuit'] != "":
            xmlfile = open('files/suspend.ldif', 'r')
            body = xmlfile.read()
            indata = {"uidrep": self['circuit'], "repdesc": repdesc}
            for key in indata:
                value = indata[key]
                body = body.replace(key, value)

            filename = self['circuit']+'.ldif'
            fh = open(filename, 'w')
            fh.write(body)
            fh.close()
            loggersuspend.info(ref + " - " + str(body))

            cmdexe = subprocess.Popen('cmd /c "ldapmodify -h '+os.getenv("ldapip")+' -D \"uid='+os.getenv("ldapusr")+',cn=config\" -w \"'+os.getenv("ldappwd")+'\" -f '+filename+'"', shell=True, stdout=subprocess.PIPE)
            result = cmdexe.stdout.readlines()

            for line in result:
                loggersuspend.info(ref + " - " + str(line))

            os.remove(filename)
            responsedata = {"result": "success", "msg": 'LDAP Suspend Completed'}
            return  responsedata
        else:
            responsedata = {"result": "failed", "msg": 'invalid request check the parameters'}
            return  responsedata
    def Resume(self):
        pass
