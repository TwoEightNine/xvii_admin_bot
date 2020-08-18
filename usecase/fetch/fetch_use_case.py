from core import fetch
from usecase.social import SocialFactory
from usecase.logger import Logger
from usecase.datasource import MessageDataSource
from .models import FetchArgs


class FetchUseCase:

    def __init__(self, social_factory: SocialFactory,
                 message_data_source: MessageDataSource,
                 args: FetchArgs, logger: Logger):
        self.args = args
        self.message_data_source = message_data_source
        self.logger = logger

        social = social_factory.create_social(args.social_param)
        fetch_params = fetch.FetchParams(args.peers_count)
        progress_watcher = self.FetchProgressWatcher(self)
        self.fetcher = fetch.Fetcher(fetch_params, social, progress_watcher)

    def fetch_messages(self):
        self.fetcher.fetch_messages()
        self.message_data_source.set_messages(self.fetcher.messages)

    class FetchProgressWatcher(fetch.FetchProgress):

        def __init__(self, use_case):
            self.use_case = use_case

        def on_fetching_started(self):
            self.use_case.logger.log('start fetching messages')

        def on_peers_fetched(self, peers_count):
            self.use_case.logger.log(f'{peers_count} peers fetched')

        def on_fetched_messages_out_of(self, fetched, out_of):
            self.use_case.logger.progress(fetched, out_of)

        def on_messages_fetched(self):
            messages_count = len(self.use_case.fetcher.messages)
            self.use_case.logger.log(f'fetched {messages_count} messages')
