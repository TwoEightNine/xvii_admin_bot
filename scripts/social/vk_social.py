import json
import random
import time

import requests

from core.social import AbsSocial
from core.model import Message


class VkSocial(AbsSocial):
    base_url = 'https://api.vk.com/method/'

    def __init__(self):
        self._server = None
        self._key = None
        self._ts = None
        self._access_token = None

    def set_api_keys(self, api_keys):
        self._access_token = api_keys

    def get_list_of_peers(self, size) -> list:
        count = 200

        remain = size
        peer_ids = []
        while remain > 0:
            err, conv = self.__execute('messages.getConversations', {
                'count': min(remain, count),
                'offset': size - remain
            })
            if err is None:
                conv_list = conv['items']
                if len(conv_list) == 0:
                    break
                for con in conv_list:
                    user_id = con['conversation']['peer']['id']
                    peer_ids.append(user_id)
            remain -= count
        return peer_ids

    def get_messages(self, peer_id: int) -> list:
        messages = []
        err, conv = self.__execute('messages.getHistory', {'count': 200, 'user_id': peer_id})
        if err is None:
            for mess in conv['items']:
                if mess['out'] == 0:
                    message = Message(mess['id'], peer_id, mess['text'])
                    messages.append(message)
        return messages

    def mark_message_as_read(self, peer_id, message_id) -> bool:
        err, response = self.__execute('messages.markAsRead', {'peer_id': peer_id})
        return err is None

    def send_message(self, peer_id, message_text) -> bool:
        err, response = self.__execute('messages.send', {
            'peer_id': peer_id,
            'message': message_text,
            'random_id': random.randint(0, 65535)
        })
        return err is None

    def wait_for_messages(self) -> list:
        self.__update_long_poll()
        response = requests.get(self.__get_lp_url())
        if response.status_code == 200:
            response = json.loads(response.text)
            ts = response.get('ts', 0)
            if ts == 0:
                self.__update_long_poll(force=True)
                return self.wait_for_messages()
            else:
                self._ts = ts
                updates = response.get('updates', [])
                messages = [Message(upd[1], upd[3], upd[6]) for upd in updates
                            if len(upd) >= 7 and upd[0] == 4 and upd[2] & 2 == 0]
                return messages
        else:
            return []

    def __get_lp_url(self):
        return f"https://{self._server}" \
            f"?act=a_check&key={self._key}" \
            f"&ts={self._ts}&wait=50&mode=2&version=1"

    def __update_long_poll(self, force: bool = False) -> bool:
        if not force and self._server is not None:
            return True

        error, response = self.__execute('messages.getLongPollServer', {'lp_version': 2})
        if error is None:
            self._server = response['server']
            self._key = response['key']
            self._ts = response['ts']
        return error is None

    def __execute(self, method, params):
        url = self.base_url + method + '?'
        for k, v in params.items():
            url += k + '=' + str(v) + '&'
        url += f'access_token={self._access_token}&v=5.103'
        r = requests.get(url).text
        response = None
        err = None
        try:
            response = json.loads(r)
        except Exception as e:
            err = str(e)
        try:
            if 'response' not in response:
                err = response['error']
                err = str(err['error_code']) + ': ' + err['error_msg']
                response = None
            else:
                response = response['response']
        except Exception as e:
            err = f'error while parsing: {e}'
        time.sleep(.33)  # vk timeout restrictions
        return err, response
