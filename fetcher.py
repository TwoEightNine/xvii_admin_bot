from tqdm import tqdm

import files
import hyperparam
from secret import no_fetch_users

if __name__ == "__main__":

    social = hyperparam.social

    # fetch user ids to fetch message history
    user_ids = social.get_list_of_peers(hyperparam.peers_count)
    user_ids = [user_id for user_id in user_ids if user_id not in no_fetch_users]
    print(f'fetched {len(user_ids)} users')

    # fetch message history as a list of messages
    messages = []
    for user_id in tqdm(user_ids):
        messages += social.get_messages(user_id)
    messages = [message for message in messages if hyperparam.is_text_informative(message)]
    print(f'fetched {len(messages)} messages')

    # save messages to data dir
    files.save_messages(messages)
