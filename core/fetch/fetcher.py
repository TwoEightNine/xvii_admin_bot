from core.social import AbsSocial
from .models import FetchParams
from .fetch_progress import FetchProgress


class Fetcher:

    def __init__(self, params: FetchParams, social: AbsSocial, progress: FetchProgress):
        self.params = params
        self.social = social
        self.progress = progress
        self.messages = []

    def fetch_messages(self):
        # fetch user ids to fetch message history
        self.progress.on_fetching_started()
        user_ids = self.social.get_list_of_peers(self.params.peers_count)
        self.progress.on_peers_fetched(len(user_ids))

        # fetch message history as a list of messages
        for i, user_id in enumerate(user_ids):
            self.messages += self.social.get_messages(user_id)
            self.progress.on_fetched_messages_out_of(i + 1, len(user_ids))
        self.progress.on_messages_fetched()
