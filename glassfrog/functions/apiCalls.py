from flask import json
import requests

from .messageFunctions import createMessageDict


class GlassfrogApiHandler(object):
    def __init__(self):
        pass

    def glassfrogApiCall(self, apiEndpoint, glassfrogToken):
        headers = {'X-Auth-Token': glassfrogToken}
        apiUrl = 'https://glassfrog.holacracy.org/api/v3/'+apiEndpoint
        apiResponse = requests.get(apiUrl, headers=headers)
        code = apiResponse.status_code
        responsebody = json.loads(apiResponse.text)
        return code, responsebody


class HipchatApiHandler(object):
    def __init__(self):
        pass

    def getCapabilitiesData(self, capabilitiesUrl):
        return json.loads(requests.get(capabilitiesUrl).text)

    def getTokenData(self, tokenUrl, client_auth, post_data):
        return json.loads(requests.post(tokenUrl, auth=client_auth, data=post_data).text)

    def sendMessage(self, color, message, installation):
        messageUrl = '{}/room/{}/notification'.format(installation.hipchatApiProvider_url,
                                                      installation.roomId)
        token_header = {"Authorization": "Bearer "+installation.access_token}
        data = createMessageDict(color, message)
        messageresponse = requests.post(messageUrl,
                                        headers=token_header,
                                        data=data)


def getCapabilitiesDict(myserver):
    capabilities_dict = \
        {
            "name": "Glassfrog Hipchat Bot",
            "description": "A Hipchat bot for accessing Glassfrog",
            "key": "glassfrog-hipchat-bot",
            "links": {
                "homepage": myserver,
                "self": myserver+"/capabilities.json"
            },
            "vendor": {
                "name": "The Hyve",
                "url": "https://www.thehyve.nl/"
            },
            "capabilities": {
                "hipchatApiConsumer": {
                    "fromName": "Glassfrog Hipchat Bot",
                    "scopes": [
                        "send_notification",
                        "view_room",
                        "view_group"
                    ]
                },
                "installable": {
                    "allowGlobal": False,
                    "allowRoom": True,
                    "callbackUrl": myserver+"/installed"
                },
                "webhook": [
                    {
                        "event": "room_message",
                        "pattern": "\\A\\/hola\\b",
                        "url": myserver+"/hola",
                        "name": "Holacracy webhook",
                        "authentication": "jwt"
                    }
                ],
                "configurable": {
                    "url": myserver+"/configure.html"
                }
            }
        }
    return capabilities_dict
