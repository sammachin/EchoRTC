import json
from botocore.vendored import requests

local_server_host = "https://exampl.ngrok.io"

def lambda_handler(event, context):
    print(event)
    print(context)
    if event['directive']['header']['namespace'] == 'Alexa.Discovery':
        return handleDiscovery(context, event)
    elif event['directive']['header']['namespace'] == 'Alexa.Authorization':
        return handleGrant(context, event)
    elif event['directive']['header']['namespace'] == 'Alexa.RTCSessionController':
        if event['directive']['header']['name'] == 'InitiateSessionWithOffer':
          return handleOffer(context, event)
        elif event['directive']['header']['name'] == 'SessionConnected':
          return handleConnected(context, event)
        elif event['directive']['header']['name'] == 'SessionDisconnected':
          return handleDisconnected(context, event)
        else:
          print(event['header']['name'])
          return {}


def handleDiscovery(context, event):
    requests.post(local_server_host+'/event', json=event)
    message_id = event['directive']['header']['messageId']
    resp = {
    "event": {
      "header": {
        "namespace":"Alexa.Discovery",
        "name":"AddOrUpdateReport",
        "payloadVersion":"3",
        "messageId": message_id
      },
      "payload":{
        "endpoints":[
          {
            "endpointId" : "browser-001",
            "manufacturerName": "The Internet",
            "modelName": "WebRTCClient",
            "friendlyName": "RTC Camera",
            "description": "A web browser with WebRTC",
            "displayCategories": [ "CAMERA", "DOORBELL" ],
            "capabilities":
            [
              {
                "type": "AlexaInterface",
                "interface": "Alexa.RTCSessionController",
                "version": "3",
                "configuration": {
                  "isFullDuplexAudioSupported": True
                }
              },
              {
                "type": "AlexaInterface",
                "interface": "Alexa.DoorbellEventSource",
                "version": "3",
                "proactivelyReported" : True
              }
            ]
          }
        ]
      }
    }
    }
    return resp

def handleOffer(context, event):
    header = event['directive']['header']
    offer = event['directive']['payload']['offer']
    r = requests.post(local_server_host+'/skill', json=offer)
    answer =  r.json()
    header['name'] = 'AnswerGeneratedForSession'
    resp = {
    "event": {
        "header": header,
        "endpoint": {
            "endpointId" : "browser-001",
        },
        "payload": {
            "answer": {
                "format" : "SDP",
                "value" : answer['sdp']
            }
        }
      } 
    }
    return resp
 
def handleConnected(context, event):
    header = event['directive']['header']
    sessionid = event['directive']['payload']['sessionId']
    requests.post(local_server_host+'/event', json=event)
    resp = {
    "event": {
        "header": header,
        "endpoint": {
            "endpointId" : "browser-001",
        },
        "payload": {
            "sessionId" : sessionid
        }
      } 
    }
    return resp
    
def handleDisconnected(context, event):
    header = event['directive']['header']
    sessionid = event['directive']['payload']['sessionId']
    requests.post(local_server_host+'/event', json=event)
    resp = {
    "event": {
        "header": header,
        "endpoint": {
            "endpointId" : "browser-001",
        },
        "payload": {
            "sessionId" : sessionid
        }
      } 
    }
    return resp
    
def handleGrant(context, event):
    header = event['directive']['header']
    message_id = event['directive']['header']['messageId']
    requests.post(local_server_host+'/event', json=event)
    resp = {
        "event": {
          "header": {
            "messageId": message_id,
            "namespace": "Alexa.Authorization",
            "name": "AcceptGrant.Response",
            "payloadVersion": "3"
          },
          "payload": {
          }
        }
      }
    return resp

  