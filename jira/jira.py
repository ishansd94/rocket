from atlassian import Jira
import requests

import os

jira_host = os.getenv("JIRA_HOST")
jira_username = os.getenv("JIRA_USERNAME")
jira_password = os.getenv("JIRA_PASSWORD")

jira = Jira(url=jira_host, username=jira_username, password=jira_password)


def jira_status(issue):
    data = jira.issue(issue)
    if 'priority' in data['fields'].keys():
        priority = data['fields']['priority']
    else:
        priority = 'None'

    info = {
        "ticket_id": data['key'],
        "description": data['fields']['summary'],
        "stage": data['fields']['status']['statusCategory']['name'],
        "priority": priority,
        "url": jira_host+'/browse/'+data['key'],
    }
    return info


def check_incident_or_not(issue):
    labels = jira.issue_field_value(issue, 'labels')
    for label in labels:

        if label == 'INCIDENT':
            return True
        return False


def print_report(args):
    inprogress = []
    done = []
    incidents = []
    open = []
    other = []
    for ticket in args:
        info = jira_status(ticket)

        if info["stage"] == "In Progress":
            info["add_details"] = True
            inprogress.append(info)

        elif info["stage"] == "Done":
            info["add_details"] = False
            done.append(info)

        elif info["stage"] == "To Do":
            info["add_details"] = True
            open.append(info)
        else:
            info["add_details"] = False
            other.append(info)

        if check_incident_or_not(ticket):
            if info["stage"] == "In Progress":
                info["add_details"] = True
            else:
                info["add_details"] = False

            incidents.append(info)

    # format the json according to slack
    # {"incidents": [], "inprogress": [], "done": []}
    return {"inprogress": inprogress, "done": done, "incidents": incidents, "open": open}


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
                "text": "*{}*\n*Description:* {}\n*Priority:* {}\n*Stage:* {}\n*URL:* {}".format(ticket["ticket_id"],
                                                                                      ticket["description"],
                                                                                      ticket["priority"],
                                                                                      ticket["stage"],
                                                                                      ticket["url"])
            }}


def get_to_shift_from(from_shift):
    to_shift = ''
    if from_shift == 'Morning':
        to_shift = 'Evening'
    elif from_shift == 'Evening':
        to_shift = 'Night'
    else:
        to_shift = 'Morning'

    return to_shift


# jira.formatted_notification("Morning", {"incidents": [], "inprogress": [], "done": []})

def formatted_notification(from_shift, tickets):
    to_shift = get_to_shift_from(from_shift)
    incidents = tickets["incidents"]
    open = tickets["open"]
    in_progess = tickets["inprogress"]+open
    completed = tickets["done"]
    details = list(map(generate_ticket_details, in_progess))
    notification_json = {
        "channel": os.getenv("SLACK_POST_CHANNEL_ID"),
        "username": "SLACK BOT",
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
    notification_json["blocks"] = notification_json["blocks"] + list(details)
    return notification_json
