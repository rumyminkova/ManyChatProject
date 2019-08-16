import requests
from requests import HTTPError
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from static_data import MESSAGE_TO_SEND, CUSTOM_FIELD_VALUE, CUSTOM_FIELD_NAME
import auth_token
import send_message


auth_token = auth_token.AUTH_TOKEN
header = {'Authorization': 'Bearer ' + auth_token}


def convert(s):
    return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S%z')


def get_custom_field_id():  # returns CustomField Id
    response = requests.get("https://api.manychat.com/fb/page/getCustomFields", headers=header)
    custom_fields_list = response.json()['data']
    for cf in custom_fields_list:
        for k, v in cf.items():
            if v == CUSTOM_FIELD_NAME:
                return cf['id']


def get_subscribers_last30min(subscribers_dict):
    send_data_to = set()
    for sub in subscribers_dict:
        d = sub['data']['subscribed']
        time_subscribed = convert(d).replace(tzinfo=None)
        if datetime.now() - timedelta(minutes=30) < time_subscribed:
            send_data_to.add(sub['data']['id'])
    return send_data_to


def get_new_subscribers():  # subscribers with CustomField = "999999999"
    custom_field_id = get_custom_field_id()
    params = {"field_id": custom_field_id, "field_value": CUSTOM_FIELD_VALUE}
    response = requests.get("https://api.manychat.com/fb/subscriber/findByCustomField", params=params, headers=header)
    if response:
        return response.json()
    else:
        print(f'An error has occurred: {response.status_code}')
        raise HTTPError


def start_script():
    try:
        subs = get_new_subscribers()
    except HTTPError:
        scheduler.remove_job('my_job_id')
    else:
        subscribed_last_30min = get_subscribers_last30min(subs)
        send_message.send_message_to_subscribers(MESSAGE_TO_SEND, subscribed_last_30min)
        send_message.change_custom_field_value(subscribed_last_30min)


scheduler = BlockingScheduler()
scheduler.add_job(start_script, 'interval', minutes=30, id='my_job_id')
scheduler.start()
