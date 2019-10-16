import requests
import json
import re
from helpers import utils


TOKEN=''

def post_req(endpoint, params):
    response = requests.get(endpoint, params=params)
    json_response = response.json()
    return json_response

responses = []

def get_messages(channel_id):

    url = 'https://slack.com/api/conversations.history'
    params = {
        'token': TOKEN,
        'channel': channel_id,
        'latest': '',
        'oldest': ''
    }

    res = post_req(url, params)

    for msg in res["messages"]:
        responses.append(msg["text"])

    if res["has_more"]:
        cursor = res["response_metadata"]["next_cursor"]
        params.update({'cursor': cursor})
        get_messages(channel_id)

    return responses




