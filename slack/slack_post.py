import requests

TOKEN = ''


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

    json_response = response.json()
    print json_response


automated_notification()
