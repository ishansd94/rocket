import requests
import json
import re
import time
import os

from helpers import utils


def do_req(endpoint, params):
    response = requests.get(endpoint, params=params)
    json_response = response.json()
    return json_response

responses = []

url = 'https://slack.com/api/conversations.history'

params = {
        'token': os.getenv("SLACK_TOKEN"),
        'channel': os.getenv("SLACK_READ_CHANNEL_ID"),
        'latest': time.time(),
        'oldest': '1569892525'
}

def get_messages():

    res = do_req(url, params)

    for msg in res["messages"]:
        responses.append(msg["text"])

    if res["has_more"] is True:
        cursor = res["response_metadata"]["next_cursor"]
        params.update({'cursor': cursor})
        get_messages()

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
                    "text": "Your one stop shop for all support inquiries for Server, Database, Application Engineering, Storage, Data Center Services, Backups, and Network Operations. If you require assistance, please post your ticket number. \n Example:- `I need help with COPS-1234`"
                }
            ],
            "text": "*Welcome to Hosting & Network Operations*",
        },
        auth=BearerAuth(os.getenv("SLACK_TOKEN"))
    )

    if response.status_code == 200:
        print("Automated notification sent..")
    else:
        print("Failed to send Automated notification sent..")
        print(response.text)


def formatted_notification(nofication_json):
    response = requests.post(
        'https://slack.com/api/chat.postMessage',
        json=nofication_json,
        auth=BearerAuth(os.getenv("SLACK_TOKEN"))
    )
    json_response = response.json()
    print json_response