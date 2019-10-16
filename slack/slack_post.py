import requests
from pprint import pprint
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


def get_ticket_id(ticket):
    return {
        "type": "plain_text",
        "text": ticket["ticket_id"]
    }


def get_ticket_ids(tickets):
    if len(tickets) == 0:
        return [{
            "type": "mrkdwn",
            "text": "*None*"
        }]
    else:
        return list(map(get_ticket_id, tickets))


def generate_ticket_details(ticket):
    if ticket["add_details"]:
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*{}*\n*Description:* {}\n*Stage:* {}".format(ticket["ticket_id"], ticket["description"], ticket["stage"])
            }}


def automated_notification(from_shift, to_shift, incidents, in_progess, completed):

    details = list(map(generate_ticket_details, incidents)) + \
        list(map(generate_ticket_details, in_progess))
    nofication_json = {
        "channel": "#test",
        "username": "HandOff Bot",
        "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "@here Shift Handoff from *{}* to *{}*".format(from_shift, to_shift)
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
                        "fields": get_ticket_ids(incidents)
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
                        "fields": get_ticket_ids(in_progess)
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
                        "fields": get_ticket_ids(completed)
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
    nofication_json["blocks"] = nofication_json["blocks"] + list(details)
    pprint(nofication_json)
    response = requests.post(
        'https://slack.com/api/chat.postMessage',
        json=nofication_json,
        auth=BearerAuth(TOKEN)
    )

    json_response = response.json()
    print(json_response)


automated_notification("Morning", "Evening", [{
    "ticket_id": "COPS-202",
    "description": "Test Incident Ticket",
    "stage": "In-Progress",
    "add_details": True
}], [{
    "ticket_id": "COPS-210",
    "description": "Test In Progress Ticket",
    "stage": "In-Progress",
    "add_details": True
}], [{
    "ticket_id": "COPS-221",
    "description": "Test Done Ticket",
    "stage": "Done",
    "add_details": True
}])
