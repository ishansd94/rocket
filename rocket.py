from settings import init
from slack import slack
from helpers import utils
from jira import jira
from notifications import notifications

import re
import time

def filter_messages():
    
    print("collecting messages")

    messages = slack.get_messages()

    jira_tickets = []

    print("processing tickets from messages")

    for r in messages:

        tickets = re.findall(r"(COPS-[0-9]*)", r)

        for ticket in tickets:
            jira_tickets.append(ticket)

    return utils.unique(jira_tickets)

def handoff():
    # schedule.every().day.at("06:00").do(job)
    time.sleep(60)

    print("running handoff for morning")

    tkts = jira.get_tickets_status(filter_messages())

    print("sending handoff to slack")

    slack.formatted_notification(jira.formatted_notification("Morning", tkts))
    
    # schedule.every().day.at("13:00").do(job)
    time.sleep(60)

    print("running handoff for evening")

    tkts = jira.get_tickets_status(filter_messages())

    print("sending handoff to slack")

    slack.formatted_notification(jira.formatted_notification("Evening", tkts))

    # schedule.every().day.at("21:30").do(job)
    time.sleep(60)

    print("running handoff for night")

    tkts = jira.get_tickets_status(filter_messages())

    print("sending handoff to slack")

    slack.formatted_notification(jira.formatted_notification("Night", tkts))


handoff()
