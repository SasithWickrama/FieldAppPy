from log import Logger
import requests
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import requests


app = Flask(__name__)
api = Api(app)

# Logger setup
loggerbbusage = Logger('cust360bbusage', 'logs/cust360bbusage')
loggerbbpwreset = Logger('cust360bbpwreset', 'logs/cust360bbpwreset')
loggerpeobub = Logger('cust360peobub', 'logs/cust360peobub')

# cust360bbusage #
class cust360bbusage(Resource):
    def post(self):
        return bbusageHandler().getbbusage()

class bbusageHandler:

    def get_bb_token(self):
        try:
            url = "https://omnitest.slt.com.lk/api/Account/ExternalAuthonticationV2"
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
                return {"status" : "success", "data"  : response.json()}
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
            token_result = get_bb_token()
    
            if token_result["status"] == "success":
                url = f"https://omnitest.slt.com.lk/api/BBVAS/UsageSummaryV2?subscriberID={bb_username}"
                bearer_token = "fJLQdQAnjEUj5B361IsA2vBbFwcHvdmuvRJSLsMXHPJ9SKWFEbbjjBDyXsmpY0zH2u7vfNDh2uAEhdJy2fruvp2f_Ftn17u1CvNla-aqze8Nc_Oi12_S6NgsroRgCUWzVR0Ghd7MTjGXIV4h6WZTFEpc8UmqHc83PzXrfTqPwFvKiLGsT2Hjyihf91e4_In-xX5_0WOSUNHBjFf69s7KxBXoHOV6qWLG2uP8lBcJ6ft8aURVgFouyQPv4XHdBVzEIUMuMzP3gyVpf92w5T4aONIvz1YFHrnL97HXRHP0Jh4PYY_w"
                # bearer_token = token_result["data"]
                headers = {
                    'Authorization': f'Bearer {bearer_token}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }

                response = requests.get(url, headers=headers)
                loggerbbusage.info("Request get_usage_summary", response.json())

                if response.json().get("isSuccess", False):
                    loggerbbusage.info("Request success with status code: %s", response.status_code)
                    return {"status" : "success", "data"  : response.json()}
                else:
                    loggerbbusage.info("Request failed with status code: %s", response.status_code)
                    return {"status": "error", "data": f"Request failed with status code-1: {response.status_code}"}
                
            else:
                loggerbbusage.info(token_result["data"])
                return {"status": "error", "data": token_result["data"]}

        except Exception as e:
            loggerbbusage.info("Exception: %s", str(e))
            return {"status" : "error", "data"  : str(e)}

  
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
            

# cust360peobindub #
class cust360peobindub(Resource):
    def post(self):
        return peobindubHandler().peobindub()

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
                return result
            elif ominitestres["status"] == "error":
                result = {"data": [{"status": "error", "message": [ominitestres["data"]]}]}
                return result

        except Exception as e:
            loggerbbusage.error("Exception: %s", str(e))
            result = {"data": [{"status": "error", "message": str(e)}]}
            return result
            
    def get_peobindub_summary(self, peotv_username, data):  # Add data as a parameter
        try:
            url = "http://10.68.148.10/slt/api/modifyPin"

            payload = {
                "CustomerId": data["peotvUsername"],
                "Platform": "IPTV/HYBRID",
                "Action": "ResetPIN",
                "Key": "key"
            }

            response = requests.post(url, json=payload)

            if response.json().get("Status", "Success"):
                loggerbbusage.info("Request success with status code: %s", response.status_code)
                return {"status" : "success", "data"  : response.json()}
            else:
                loggerbbusage.info("Request failed with status code: %s", response.status_code)
                return {"status": "error", "data": f"Request failed with status code: {response.status_code}"}

        except Exception as e:
            loggerbbusage.info("Exception: %s", str(e))
            return {"status" : "error", "data"  : str(e)}

# Customer360
api.add_resource(cust360bbusage, '/api/SLT/customer360/bbusage/')
api.add_resource(cust360peobindub, '/api/SLT/customer360/peobindub/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20005)
