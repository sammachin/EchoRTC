import requests
import uuid
import time
import datetime



url = "https://api.amazonalexa.com/v3/events"
skill_token  =  'Atza|xxxxxxx'
customer_token = 'Atza|zzzzzzzzzzz'
headers = {'Authorization' : 'Bearer '+customer_token}
payload = {
    "context": {},
    "event": {
        "header": {
            "messageId": str(uuid.uuid4()),
            "namespace" : "Alexa.DoorbellEventSource",
            "name": "DoorbellPress",
            "payloadVersion": "3"
        },
        "endpoint": {
            "scope": {
                "type": "BearerToken",
                "token": customer_token
            },
            "endpointId": "browser-001"
        },
        "payload" : {
            "cause": {
                "type": "PHYSICAL_INTERACTION"
            },
            "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
    }
} 
print(payload)
resp = requests.post(url, headers=headers, json=payload)
print(resp)




