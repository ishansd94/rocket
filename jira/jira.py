from atlassian import Jira

import os

def jira_status(issue):

    jira_host=os.getenv("JIRA_HOST")
    jira_username=os.getenv("JIRA_USERNAME")
    jira_password=os.getenv("JIRA_PASSWORD")

    jira = Jira(url=jira_host, username=jira_username, password=jira_password)

    data = jira.issue(issue)
    info = {
        "ticket" : data['key'],
        "summary": data['fields']['summary'],
        "status": data['fields']['status']['statusCategory']['name'],
        "priority": data['fields']['priority']['name']
    }
    return info


def print_report(args):
    inprogress = []
    closed = []
    for ticket in args:
        info = jira_status(ticket)
        if info["status"] == "In Progress":
            inprogress.append(info)
        else:
            closed.append(info)

    # format the json according to slack
    print(inprogress,closed)

