import requests

from log import Logger
from flask import Flask, request, jsonify
from flask_restful import Api, Resource

def get_peopinreset_summary(self, data):  # Add data as a parameter
    try:
        url = "http://10.68.148.10/slt/api/modifyPin"
        payload = {
            "CustomerId": data["peotvUsername"],
            "Platform": data["platform"],
            "Action": "ResetPIN",
            "Key": "gn%_3sq1!"
        }
        response = requests.post(url, json=payload)
        print(response.json())
        response_data = response.json()
        if (response_data["Status"] == "Success"):
            print("Request success with status code: %s", response.status_code)
            return {"status" : "success", "data"  : response.json()}
        elif (response_data["Status"] == "Fail"):
            print("Request failed with error: %s", response.json()["Reason"])
            return {"status": "error", "data": response.json()}
    except Exception as e:
        print("Exception: %s", str(e))
        return {"status" : "error", "data"  : str(e)}  
    
# data = request.get_json()
# print("data: %s", data)
data = {
    "peotvUsername" : "0888881005",
    "platform" : "MIT"
}

print(data)
peotv_username = data["peotvUsername"]
# peobindub_handler = peobindubHandler()
ominitestres = get_peopinreset_summary(peotv_username, data)  # Pass data as a parameter
print("ominitest response: %s", ominitestres)

if ominitestres["status"] == "success":
    result = {"data": [{"status": "success", "message": [ominitestres["data"]]}]}
    print(result)
elif ominitestres["status"] == "error":
    result = {"data": [{"status": "error", "message": [ominitestres["data"]]}]}
    print(result)

        
