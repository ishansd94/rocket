from settings import init
from slack import slack
from helpers import utils
from jira import jira
from notifications import notifications


import re

messages = slack.get_messages()

print(messages)

jira_tickets = []

for r in messages:

    tickets = re.findall(r"(COPS-[0-9]*)", r)

    for ticket in tickets:
        jira_tickets.append(ticket)

jira_tickets = utils.unique(jira_tickets)
print(jira_tickets)

tickets = jira.print_report(jira_tickets)
notification_json = jira.formatted_notification("Morning", tickets)
slack.formatted_notification(notification_json)


