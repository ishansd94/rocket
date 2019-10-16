from atlassian import Jira

USERNAME = ''
PASSWORD = ''
jira = Jira(url='https://agile-jira.pearson.com', username=USERNAME, password=PASSWORD)


def jira_status(issue):
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
    print inprogress,closed


tickets = ['COPS-4029','COPS-4028']
print_report(tickets)
