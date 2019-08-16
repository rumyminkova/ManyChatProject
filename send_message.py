import requests
import json
import auth_token
from static_data import CUSTOM_FIELD_NAME


auth_token = auth_token.AUTH_TOKEN
header = {'Authorization': 'Bearer ' + auth_token}


def send_message_to_subscribers(msg, subscribers_list):
    url = "https://api.manychat.com/fb/sending/sendContent"
    headers = {'Authorization': 'Bearer ' + auth_token,
               'Accept': 'application/json',
               'Content-Type': 'application/json'}

    for subscriber in subscribers_list:
        payload = {
            "subscriber_id": subscriber,
            "data": {
                    "version": "v2",
                    "content": {
                        "messages": [{"type": "text",
                                      "text": msg}]
                    }
            }
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response:
            print(f'Message sent to subscriber with ID: {subscriber}')
        else:
            print(f'An error has occurred: {response.status_code}')


def change_custom_field_value(subscribers_list):
    url = "https://api.manychat.com/fb/subscriber/setCustomFieldByName"
    headers = {'Authorization': 'Bearer ' + auth_token,
               'Accept': 'application/json',
               'Content-Type': 'application/json'}

    for subscriber in subscribers_list:
        payload = {
            "subscriber_id": subscriber,
            "field_name": CUSTOM_FIELD_NAME,
            "field_value": "000000000"
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response:
            print(f'Custom filed changed subscriber with ID: {subscriber}')
        else:
            print(f'An error has occurred: {response.status_code}')


