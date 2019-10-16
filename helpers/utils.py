import json

def unique(items):
    output = []
    for x in items:
        if x not in output:
            output.append(x)
    
    return output

def past_in_progress_tickets(filepath="../past_in_progress/COPS.json"):
    with open(filepath) as past_progress_json:
        data = json.load(past_progress_json)
        return data