import requests
import json
import re
from helpers import utils


TOKEN=''

def post_req(endpoint, params):
    response = requests.get(endpoint, params=params)
    json_response = response.json()
    return json_response

responses = []

def get_messages(channel_id):

    url = 'https://slack.com/api/conversations.history'
    params = {
        'token': TOKEN,
        'channel': channel_id,
        'latest': '',
        'oldest': ''
    }

    res = post_req(url, params)

    for msg in res["messages"]:
        responses.append(msg["text"])

    if res["has_more"]:
        cursor = res["response_metadata"]["next_cursor"]
        params.update({'cursor': cursor})
        get_messages(channel_id)

    return responses


class BearerAuth(requests.auth.AuthBase):
    token = None

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def automated_notification():
    response = requests.post(
        'https://slack.com/api/chat.postMessage',
        json={
            "channel": "#test",
            "username": "SLACK BOT",
            "attachments": [
                {
                    "text": "Your one stop shop for all support inquiries for Server, Database, Application Engineering, Storage, Data Center Services, Backups, and Network Operations. If you require assistance, please post your ticket number. \n Example:- `TicketID:- COPS-4567`"
                }
            ],
            "text": "*Welcome to Hosting & Network Operations*",
        },
        auth=BearerAuth(TOKEN)
    )



