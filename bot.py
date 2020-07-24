import json
import random

import dumper
import predictor
import utils
import requests

marker_leave_unread = '__UNREAD'
marker_mark_as_read = '__READ'


class LongPoll:

    def __init__(self, server, key, ts):
        self._server = server
        self._key = key
        self.ts = ts

    def get_url(self):
        return f"https://{self._server}" \
            f"?act=a_check&key={self._key}" \
            f"&ts={self.ts}&wait=50&mode=2&version=1"


def get_long_poll():
    error, response = utils.execute('messages.getLongPollServer', {'lp_version': 2})
    if error is None:
        return LongPoll(response['server'], response['key'], response['ts'])


def wait_for_messages(lp: LongPoll) -> tuple:
    response = requests.get(lp.get_url())
    if response.status_code == 200:
        response = json.loads(response.text)
        ts = response.get('ts', 0)
        updates = response.get('updates', [])
        failed = response.get('failed', 0)
        messages = [(upd[3], upd[6]) for upd in updates
                    if len(upd) >= 7 and upd[0] == 4 and upd[2] & 2 == 0]
        return ts, messages
    else:
        return 0, []


def mark_as_read(user_id: int):
    err, response = utils.execute('messages.markAsRead', {'peer_id': user_id})
    if err is not None:
        print(f'marking as read: {err}')


def send_message(user_id: int, text: str):
    err, response = utils.execute('messages.send', {
        'peer_id': user_id,
        'message': text,
        'random_id': random.randint(0, 65535)
    })
    if err is not None:
        print(f'sending message: {err}')


def respond(user_id: int, message_class: str):
    if message_class in responses:
        response = responses[message_class]
        if response != "":
            send_message(user_id, response)
        else:
            mark_as_read(user_id)


if __name__ == "__main__":
    responses = dumper.load_class_responses()
    pr = predictor.Predictor(dumper.load_pipeline(), dumper.load_classes())
    while True:
        try:
            long_poll = get_long_poll()
            print('longpoll server obtained..')
            is_long_poll_valid = True
            while is_long_poll_valid:
                ts, messages = wait_for_messages(long_poll)
                if ts != 0:
                    for message in messages:
                        user_id, message_text = message
                        message_class = pr.predict(message_text)
                        print(f'{user_id}: {message_text} ({message_class})')

                        # find response
                        if message_class in responses:
                            response = responses[message_class]
                        else:
                            response = marker_leave_unread
                        print(f'response: {response}')

                        # perform action according to response
                        if response == marker_mark_as_read:
                            mark_as_read(user_id)
                        elif response != marker_leave_unread:
                            send_message(user_id, response)

                        print('')
                    long_poll.ts = ts
                else:
                    is_long_poll_valid = False
        except Exception as e:
            print(f'error occurred: {e}')
