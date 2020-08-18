from core import exploreclusters

from usecase.logger import Logger
from usecase.datasource import MessageDataSource, ClusterExplorerDataSource
from .models import ExplorerArgs


class ClusterExplorerUseCase:

    def __init__(self, message_data_source: MessageDataSource,
                 cluster_explorer_data_source: ClusterExplorerDataSource,
                 args: ExplorerArgs, logger: Logger):
        self.message_data_source = message_data_source
        self.cluster_explorer_data_source = cluster_explorer_data_source
        self.logger = logger

        params = exploreclusters.ExplorerParams(args.random_state)
        progress = self.ExploreProgressWatcher(self)
        self.explorer = exploreclusters.ClusterExplorer(params, progress)

    def explore_clusters(self):
        messages = self.message_data_source.get_messages()
        messages = [message.text for message in messages]
        self.explorer.explore(messages)
        self.cluster_explorer_data_source.save_results(self.explorer.results)

    class ExploreProgressWatcher(exploreclusters.ExploreProgress):

        def __init__(self, use_case):
            self.use_case = use_case

        def on_exploration_started(self):
            self.use_case.logger.log('exploration started')

        def on_explored_clusters(self, clusters_count: int):
            self.use_case.logger.log(f'clusters count: {clusters_count}')

        def on_results_ready(self):
            self.use_case.logger.log('exploration finished')
