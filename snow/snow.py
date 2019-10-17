import pysnow
import json

INSTANCE=""
USER=""
PASSWORD=""

def get_ticket(ticket_id):

    # Create client object
    c = pysnow.Client(instance=INSTANCE, user=USER, password=PASSWORD)

    # Query incident records with number starting with 'INC0123', created between 60 days ago and today.
    qb = (
        pysnow.QueryBuilder()
        .field('number').starts_with(ticket_id[:6])
    )

    incident = c.resource(api_path='/table/incident')

    response = incident.get(query=qb)

    # Iterate over the matching records and print out number
    for record in response.all():
        # print(record['number'])
        if record['number'] == ticket_id:
           return record