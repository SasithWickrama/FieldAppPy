import os
import subprocess
from datetime import datetime
from log import Logger
import hashlib
import base64

def hash_generate(password_text):
    salt = os.urandom(8)
    hashed_password = hashlib.sha1(password_text.encode('utf-8') + salt).digest()
    final_hash = base64.b64encode(hashed_password + salt).decode('utf-8')
    return "{SSHA}" + final_hash

cdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

loggerresume = Logger('modifypw', 'logs/modifypw')

class modifypassword:
    def Modifypw(self, ref):
        repdesc = 'modify password from OSS on ' + cdate
        
        password_text = self['BBpassword']
        ldap_hash = hash_generate(password_text)

        if self['circuit'] != "":
            with open('files/modifypw.ldif', 'r') as xmlfile:
                body = xmlfile.read()

            indata = {"uidrep": self['circuit'], "repdesc": repdesc, "bbPasswd": ldap_hash}
            for key in indata:
                value = indata[key]
                body = body.replace(key, value)

            filename = self['circuit'] + '.ldif'
            with open(filename, 'w') as fh:
                fh.write(body)
            
            print(f"LDIF file created at {filename}")

            loggerresume.info(ref + " - " + str(body))

            ldapmodify_path = '/usr/bin/ldapmodify'
            ldapip = "10.68.74.32"
            ldapusr = "OSSUser"
            ldappwd = 'o$Sld@PAdm!N'

            # Use subprocess.run for better handling and escaping
            cmd = [
                ldapmodify_path,
                '-h', ldapip,
                '-D', f"uid={ldapusr},cn=config",
                '-w', ldappwd,
                '-f', filename
            ]
            print(f"Executing command: {' '.join(cmd)}")

            try:
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True
                )
                
                loggerresume.info(ref + " - STDOUT: " + result.stdout.decode('utf-8'))
                loggerresume.info(ref + " - STDERR: " + result.stderr.decode('utf-8'))

                os.remove(filename)
                return {"result": "success", "msg": password_text}

            except subprocess.CalledProcessError as e:
                loggerresume.error(ref + " - Command failed with error: " + e.stderr.decode('utf-8'))
                return {"result": "failed", "msg": f'LDAP modify password failed with return code {e.returncode}'}

            except Exception as e:
                loggerresume.error(ref + " - Exception occurred: " + str(e))
                return {"result": "failed", "msg": str(e)}

        else:
            responsedata = {"result": "failed", "msg": 'invalid request check the parameters'}
            return responsedata
