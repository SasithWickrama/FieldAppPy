import random
import requests

from log import Logger
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from susres import SuspendResumed
from modifypw import modifypassword

app = Flask(__name__)
api = Api(app)

logger = Logger('server_requests', 'logs/server_requests')

loggerbbusage = Logger('cust360bbusage', 'logs/cust360bbusage')
loggerbbpwreset = Logger('cust360bbpwreset', 'logs/cust360bbpwreset')
loggerpeobub = Logger('cust360peobub', 'logs/cust360peobub')

def random_ref(length):
    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # define the specific string
    return ''.join((random.choice(sample_string)) for x in range(length))


class SuspendResume(Resource):
    def post(self):
        ref = random_ref(15)
        data = request.get_json()
        logger.info(ref + " - " + str(data))

        if data['action'] == 'suspend':
            return SuspendResumed.Suspend(data, ref)
        if data['action'] == 'resume':
            return SuspendResumed.Resume(data, ref)

class Modifypassword(Resource):
    def post(self):
        ref = random_ref(15)
        data = request.get_json()
        logger.info(ref + " - " + str(data))

        if data['action'] == 'modifypw':
            return modifypassword.Modifypw(data, ref)

# cust360bbusage #
class cust360bbusage(Resource):
    def post(self):
        return bbusageHandler().getbbusage()

class bbusageHandler:
    def getbbusage(self):
        try:
            data = request.get_json()
            loggerbbusage.info("data: %s", data)
            
            bb_username = data["bbUsername"]
            bbusage_handler = bbusageHandler()
            ominitestres = bbusage_handler.get_usage_summary(bb_username)
            loggerbbusage.info("ominitest response: %s", ominitestres)
            
            if ominitestres["status"] == "success" :
                result = {"data": [{"status": "success", "message": [ominitestres["data"]]}]}
                return result
            elif ominitestres["status"] == "error" :
                result = {"data": [{"status": "error", "message": [ominitestres["data"]]}]}
                return result

        except Exception as e:
            loggerbbusage.error("Exception: %s", str(e))
            result = {"data": [{"status": "error", "message": str(e)}]}
            return result

    def get_bb_token(self):
        try:
            url = "https://omni.slt.com.lk/api/Account/ExternalAuthonticationV2"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            
            data = {
                'username': 'NEYLIE@OMNIUSER',
                'code': 'N@7L#E$3sNp',
                'channelID': 'NEYLIE'
            }
            
            response = requests.post(url, headers=headers, data=data)
            
            if "accessToken" in response.json():
                loggerbbusage.info("Request success with status code: %s", response.status_code)
                return {"status" : "success", "data"  : response.json()["accessToken"]}
            elif "message" in response.json():
                loggerbbusage.info("Request failed with status code: %s with message: %s", response.status_code, response.json()['message'])
                return {"status": "error", "data": f"Request failed with message: {response.json()['message']}"}
            else:
                loggerbbusage.info("Request failed with status code: %s with message: %s", response.status_code, response.json()['errorMessege'])
                return {"status": "error", "data": f"Request failed with message: {response.json()['errorMessege']}"}


        except Exception as e:
            loggerbbusage.info("Exception: %s", str(e))
            return {"status" : "error", "data"  : str(e)}
    
    def get_usage_summary(self, bb_username):
        try:
            bbusage_handler = bbusageHandler()
            token_result = bbusage_handler.get_bb_token()
            loggerbbusage.info("token_result: %s", token_result["data"])
            
            if token_result["status"] == "success":
                url = f"https://omni.slt.com.lk/api/BBVAS/UsageSummaryV2?subscriberID={bb_username}"
                # bearer_token = "bbuCwynAT5nvW98vJ7Xtv0vPxlZ1u4uSGCwWXWbo8WbRk4kzlt-kFGKbsQQIHkY1i4mlLAg4CfpI2p9mrBje79LxdyRDHcZt2mmmy3JFkuYDrvIGGmcEhfPFRMDJokzuX0yWM51LlvatmJ6rxbxJzFIm8KrM-xrokDj-HZL6gPEooCLiU_HUZ9c2Gc3qq07urne0-kNxm3KifQJ3MkzC8WaTQvYrsMpnpYNxm0bRafCZlwqS2yrQUvVGyeJFwsW52ZOZnT7yZFDtpcxjqEcaUC80nv78fOnTmVeV4kl5uXuAif-C"
                bearer_token = token_result["data"]
    
                headers = {
                    'Authorization': f'Bearer {bearer_token}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
    
                response = requests.get(url, headers=headers)
    
                if response.json().get("isSuccess", False):
                    loggerbbusage.info("Request success with status code: %s", response.status_code)
                    return {"status" : "success", "data"  : response.json()}
                elif "message" in response.json():
                    loggerbbusage.info("Request failed with message: %s", response.json()['message'])
                    return {"status": "error", "data": f"Request failed with message: {response.json()['message']}"}
                else:
                    loggerbbusage.info("Request failed with status code: %s", response.status_code)
                    return {"status": "error", "data": f"Request failed with status code: {response.status_code}"}
                    
            else:
                loggerbbusage.info(token_result["data"])
                return {"status": "error", "data": token_result["data"]}


        except Exception as e:
            loggerbbusage.info("Exception: %s", str(e))
            return {"status" : "error", "data"  : str(e)}

# cust360peobindub #
class cust360peobindub(Resource):
    def post(self):
        return peobindubHandler().peobindub()

class cust360peopinreset(Resource):
    def post(self):
        return peopinresetHandler().peopinreset()

class peobindubHandler:
    def peobindub(self):
        try:
            data = request.get_json()
            loggerbbusage.info("data: %s", data)
            
            peotv_username = data["peotvUsername"]
            peobindub_handler = peobindubHandler()
            ominitestres = peobindub_handler.get_peobindub_summary(peotv_username, data)  # Pass data as a parameter
            loggerbbusage.info("ominitest response: %s", ominitestres)
            
            if ominitestres["status"] == "success":
                result = {"data": [{"status": "success", "message": [ominitestres["data"]]}]}
                loggerbbusage.info("return result: %s", result)
                return result
            elif ominitestres["status"] == "error":
                result = {"data": [{"status": "error", "message": [ominitestres["data"]]}]}
                loggerbbusage.info("return result: %s", result)
                return result

        except Exception as e:
            loggerbbusage.error("Exception: %s", str(e))
            result = {"data": [{"status": "error", "message": str(e)}]}
            return result
            
    def get_peobindub_summary(self, peotv_username, data):  # Add data as a parameter
        try:
            url = "http://10.68.148.10/slt/api/device"

            payload = {
                "CustomerId": data["peotvUsername"],
                "Platform": data["platform"],
                "Action": "Unbind",
                "Key": "gn%_3sq1!"
            }

            response = requests.post(url, json=payload)

            response_data = response.json()
            if (response_data["Status"] == "Success"):
                loggerbbusage.info("Request success with status code: %s", response.status_code)
                return {"status" : "success", "data"  : response.json()}
            elif (response_data["Status"] == "Fail"):
                loggerbbusage.info("Request failed with error: %s", response.json()["Reason"])
                return {"status": "error", "data": response.json()}

        except Exception as e:
            loggerbbusage.info("Exception: %s", str(e))
            return {"status" : "error", "data"  : str(e)}            
            

class peopinresetHandler:
    def peopinreset(self):
        try:
            data = request.get_json()
            loggerbbusage.info("data: %s", data)
            
            peotv_username = data["peotvUsername"]
            peoreset_handler = peopinresetHandler()
            ominitestres = peoreset_handler.get_peopinreset_summary(peotv_username, data)  # Pass data as a parameter
            loggerbbusage.info("ominitest response: %s", ominitestres)
            
            if ominitestres["status"] == "success":
                result = {"data": [{"status": "success", "message": [ominitestres["data"]]}]}
                loggerbbusage.info("return result: %s", result)
                return result
            elif ominitestres["status"] == "error":
                result = {"data": [{"status": "error", "message": [ominitestres["data"]]}]}
                loggerbbusage.info("return result: %s", result)
                return result

        except Exception as e:
            loggerbbusage.error("Exception: %s", str(e))
            result = {"data": [{"status": "error", "message": str(e)}]}
            return result

    def get_peopinreset_summary(self, peotv_username, data):  # Add data as a parameter
        try:
            url = "http://10.68.148.10/slt/api/modifyPin"

            payload = {
                "CustomerId": data["peotvUsername"],
                "Platform": data["platform"],
                "Action": "ResetPIN",
                "Key": "gn%_3sq1!"
            }

            response = requests.post(url, json=payload)

            response_data = response.json()
            if (response_data["Status"] == "Success"):
                loggerbbusage.info("Request success with status code: %s", response.status_code)
                return {"status" : "success", "data"  : response.json()}
            elif (response_data["Status"] == "Fail"):
                loggerbbusage.info("Request failed with error: %s", response.json()["Reason"])
                return {"status": "error", "data": response.json()}

        except Exception as e:
            loggerbbusage.info("Exception: %s", str(e))
            return {"status" : "error", "data"  : str(e)}

# LDAP Commands
api.add_resource(SuspendResume, '/sltdevops/apiv1/susres')
api.add_resource(Modifypassword, '/api/SLT/customer360/bbpwreset/')

# Customer360
api.add_resource(cust360bbusage, '/api/SLT/customer360/bbusage/')
api.add_resource(cust360peobindub, '/api/SLT/customer360/peobindub/')
api.add_resource(cust360peopinreset, '/api/SLT/customer360/peopinreset/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8450)