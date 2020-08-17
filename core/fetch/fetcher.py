from core.social import AbsSocial
from core.logger import Logger
from .fetch_output import FetchOutput
from .fetch_params import FetchParams


class Fetcher:

    def __init__(self, params: FetchParams, output: FetchOutput, social: AbsSocial, logger: Logger):
        self.params = params
        self.output = output
        self.social = social
        self.logger = logger
        self.messages = []

    def fetch_messages(self):
        # fetch user ids to fetch message history
        user_ids = self.social.get_list_of_peers(self.params.peers_count)
        self.logger.log(f'fetched {len(user_ids)} dialogs')

        # fetch message history as a list of messages
        for i, user_id in enumerate(user_ids):
            self.messages += self.social.get_messages(user_id)
            self.logger.indicate_progress(i + 1, len(user_ids))
        self.logger.log(f'fetched {len(self.messages)} messages')

    def save_messages(self):
        self.output.save_messages(self.messages)
