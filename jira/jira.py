from atlassian import Jira

USERNAME = ''
PASSWORD = ''
jira = Jira(url='https://agile-jira.pearson.com', username=USERNAME, password=PASSWORD)


def jira_status(issue):
    data = jira.issue(issue)
    return data['fields']['status']['statusCategory']['name']
