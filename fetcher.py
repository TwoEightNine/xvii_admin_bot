import time

from tqdm import tqdm

import files
import hyperparam
import utils
from secret import no_fetch_users


if __name__ == "__main__":

    # fetch user ids to fetch message history
    user_ids = []
    for i in tqdm(range(4)):
        err, conv = utils.execute('messages.getConversations', {'count': 200, 'offset': i * 200})
        if err is None:
            conv_list = conv['items']
            if len(conv_list) == 0:
                break
            for con in conv_list:
                user_id = con['conversation']['peer']['id']
                if user_id not in no_fetch_users:
                    user_ids.append(user_id)
    print(f'fetched {len(user_ids)} users')

    # fetch message history as a list of messages
    messages = []
    for user_id in tqdm(user_ids):
        err, conv = utils.execute('messages.getHistory', {'count': 200, 'user_id': user_id})
        if err is None:
            for mess in conv['items']:
                if mess['out'] == 0:
                    text = mess['text']
                    if hyperparam.is_text_informative(text):
                        messages.append(text)
        time.sleep(.33)

    print(f'fetched {len(messages)} messages')

    # save messages to data dir
    files.save_messages(messages)
