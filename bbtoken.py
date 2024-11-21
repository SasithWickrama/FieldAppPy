import requests

# cust360bbusage #

def get_bb_token():
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
            print("Request success with status code: %s" % (response.status_code))
            return {"status" : "success", "data"  : response.json()["accessToken"]}
        elif "message" in response.json():
            print("Request failed with status code: %s with message: %s" % (response.status_code, response.json()['message']))
            return {"status": "error", "data": f"Request failed with message: {response.json()['message']}"}
        else:
            print("Request failed with status code: %s with message: %s" % (response.status_code, response.json()['errorMessege']))
            return {"status": "error", "data": f"Request failed with message: {response.json()['errorMessege']}"}
    except Exception as e:
        print("Exception: %s", str(e))
        return {"status" : "error", "data"  : str(e)}
    

def get_usage_summary(bb_username):
    try:
        token_result = get_bb_token()

        if token_result["status"] == "success":
            url = f"https://omni.slt.com.lk/api/BBVAS/UsageSummaryV2?subscriberID={bb_username}"
            # bearer_token = "2w5R_tme9pp83DhflajwaP0_DdLQVO_w4S5qyaFpPgepZl4dear9uV9GGsQYBZEi94m6qOVHjchnG6BldjWvN1eoJqU8SA-EXk0r78g2Wz5FJJAnIYndAGMTqDzowOFqaGbCjXTwZ8HkKMSOCrNkOS4dY2gWaHvepdyJqagSJ1FYoGo0f94JLGmFj0Udw4yOw7JPxIvvuKHILBk-7THBATVksGunG6rbwWDrjUN62ckF3EM6bt6DFIirGPdpFGu4CxE8MMXACIgwcbSE8wOzWHD0UgbCPMrfyOLn4zLq0C1-Keai"
            bearer_token = token_result["data"]
            headers = {
                'Authorization': f'Bearer {bearer_token}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.get(url, headers=headers)
            if response.json().get("isSuccess", False):
                print("Request success with status code: %s", response.status_code)
                return {"status" : "success", "data"  : response.json()}
            else:
                print("Request failed with status code: %s", response.status_code)
                return {"status": "error", "data": f"Request failed with status code: {response.status_code}"}
        else:
            print(token_result["data"])
            return {"status": "error", "data": token_result["data"]}

    except Exception as e:
        print("Exception: %s", str(e))
        return {"status" : "error", "data"  : str(e)}

# data = request.get_json()
# print("data: %s", data)
#0112255078
# bb_username = data["bbUsername"]
bb_username = '94112421563'
# bbusage_handler = bbusageHandler()
# ominitestres = bbusage_handler.get_usage_summary(bb_username)
ominitestres = get_usage_summary(bb_username)
print("ominitest response: %s", ominitestres)

if ominitestres["status"] == "success" :
    result = {"data": [{"status": "success", "message": [ominitestres["data"]]}]}
    print(result)
elif ominitestres["status"] == "error" :
    result = {"data": [{"status": "error", "message": [ominitestres["data"]]}]}
    print(result)


