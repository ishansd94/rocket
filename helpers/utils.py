import json

def unique(items):
    output = []
    for x in items:
        if x not in output:
            output.append(x)
    
    return output
