from slack import slack
from helpers import utils
from jira import jira
import re

SLACK_CHANNEL_ID=""

messages = slack.get_messages(SLACK_CHANNEL_ID)

jira_tickets = []

for r in messages:

    tickets = re.findall(r"^(-[0-9]*)", r)

    for ticket in tickets:
        jira_tickets.append(ticket)

jira_tickets = utils.unique(jira_tickets)

jira.print_report(jira_tickets)

slack.automated_notification()

