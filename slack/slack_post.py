import requests

TOKEN = ''


class BearerAuth(requests.auth.AuthBase):
    token = None

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

# Ticket Dict
# {
#   "ticket_id" : "COPS-XXXX",
#   "stage": "in-progess",
#   "description": "description of the Ticket",
#   "add_details" : True | False
# }
#Incidents = [Ticket]
#In_Progess = [Ticket]
#completed = [Ticket]


def automated_notification(from_shift, to_shift, incidents, in_progess, completed):

    nofication_json = {
        "channel": "#test",
        "username": "HandOff Bot",
        "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "@here Shift Handoff from *"+from_shift+"* to *"+to_shift+"*"
                        }
                    },
                {
                        "type": "divider"
                        },
            {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": ":bangbang:* Incident Tickets (P1,P2,P3):*"
                        }
            },
            # incident list 3
            {
                        "type": "section",
                        "fields": [
                        ]
            },
            {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": ":warning:* Immediate Attention Required Tickets:*"
                        }
            },
            # in progress list 5
            {
                        "type": "section",
                        "fields": [

                        ]
            },
            {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": ":heavy_check_mark:* Changes/Releases Carried out during Shift:*"
                        }
            },
            # completed list 7
            {
                        "type": "section",
                        "fields": [
                        ]
            },
            {
                        "type": "divider"
            },
            {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Detailed View of Open Tickets*"
                        }
            },
            # Details 10 - *

        ]
    }
    response = requests.post(
        'https://slack.com/api/chat.postMessage',
        json=nofication_json,
        auth=BearerAuth(TOKEN)
    )

    json_response = response.json()
    print(json_response)


automated_notification("Morning","Evening",[],[],[])
