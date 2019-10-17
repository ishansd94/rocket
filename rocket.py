from settings import init
from slack import slack
from helpers import utils
from jira import jira
from notifications import notifications


import re

messages = slack.get_messages()

jira_tickets = []

for r in messages:

    tickets = re.findall(r"^(COPS-[0-9]*)", r)

    for ticket in tickets:
        jira_tickets.append(ticket)

jira_tickets = utils.unique(jira_tickets)
inprogress, done, incidents = jira.print_report(jira_tickets)
notification_json = jira.formatted_notification("Morning", "Evening", incidents, inprogress, done)
slack.notification(notification_json)


