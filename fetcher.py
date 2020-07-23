import time
import pandas as pd
from tqdm import tqdm
import utils
from notebooks.secret import no_fetch_users

data_path = 'data/'


def is_text_informative(text):
    """
    defines if text is going to be informative for model
    :param text: message to check
    :return: true if message is informative, false if deny the message
    """
    return len(text) != 0 \
           and 'CRASH REPORT' not in text \
           and 'android.' not in text \
           and '[service]' not in text \
           and 'DEVICE INFORMATION' not in text \
           and 'com.twoeightnine.root.xvii.' not in text \
           and 'okhttp3.internal.' not in text \
           and '[longpoll]' not in text


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
                    if is_text_informative(text):
                        messages.append(text)
        time.sleep(.33)

    print(f'fetched {len(messages)} messages')

    # save messages to data dir
    df = pd.DataFrame()
    df['message'] = messages
    df.to_csv(data_path + 'messages.csv', index=False)
    df.head(20)
