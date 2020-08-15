import argparse

from tqdm import tqdm

import files
import hyperparam
import social
from secret import no_fetch_users

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='fetch messages from target social network')
    parser.add_argument('--count', required=True, type=int, help='how many recent dialogs to fetch')
    parser.add_argument('--social', required=True,
                        help=f'which social network to use (supported values: {social.supported_socials})')
    args = parser.parse_args()

    social_network = social.create_social(args.social)
    if not social_network:
        print(f'incorrect social network passed: {args.social}. use -h to see help')
        exit(0)

    # fetch user ids to fetch message history
    user_ids = social_network.get_list_of_peers(args.count)
    user_ids = [user_id for user_id in user_ids if user_id not in no_fetch_users]
    print(f'fetched {len(user_ids)} dialogs')

    # fetch message history as a list of messages
    messages = []
    for user_id in tqdm(user_ids):
        messages += social_network.get_messages(user_id)
    messages = [message for message in messages if hyperparam.is_text_informative(message)]
    print(f'fetched {len(messages)} messages')

    # save messages to data dir
    files.save_messages(messages)
