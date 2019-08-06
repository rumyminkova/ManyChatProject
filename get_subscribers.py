import requests
from requests import HTTPError
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from static_data import CUSTOM_FIELD_ID, MESSAGE_TO_SEND
import auth_token
import send_message


auth_token = auth_token.AUTH_TOKEN
header = {'Authorization': 'Bearer ' + auth_token}


def convert(s):
    return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S%z')


def get_subscribers_last30min(subscribers_dict):
    send_data_to = set()
    for sub in subscribers_dict:
        d = sub['data']['subscribed']
        time_subscribed = convert(d).replace(tzinfo=None)
        if datetime.now() - timedelta(minutes=30) < time_subscribed:
            send_data_to.add(sub['data']['id'])
    return send_data_to


def get_today_subscribers():
    today = datetime.today().strftime('%Y-%m-%d')
    params = {"field_id": CUSTOM_FIELD_ID, "field_value": today}
    response = requests.get("https://api.manychat.com/fb/subscriber/findByCustomField", params=params, headers=header)
    if response:
        return response.json()
    else:
        print(f'An error has occurred: {response.status_code}')
        raise HTTPError


def start_script():
    try:
        subs = get_today_subscribers()
    except HTTPError:
        scheduler.remove_job('my_job_id')
    else:
        send_message.send_message_to_subscribers(MESSAGE_TO_SEND, get_subscribers_last30min(subs))


scheduler = BlockingScheduler()
scheduler.add_job(start_script, 'interval', minutes=30, id='my_job_id')
scheduler.start()







