from core import exploremodels
from usecase.datasource import ClusteredMessageDataSource, MessageClassesDataSource, ModelsExplorerDataSource
from usecase.logger import Logger
from .models import ExplorerArgs


class ModelsExplorerUseCase:

    def __init__(self,
                 clustered_messages_data_source: ClusteredMessageDataSource,
                 message_classes_data_source: MessageClassesDataSource,
                 models_explorer_data_source: ModelsExplorerDataSource,
                 logger: Logger, args: ExplorerArgs):
        self.logger = logger
        self.clustered_messages_data_source = clustered_messages_data_source
        self.message_classes_data_source = message_classes_data_source
        self.models_explorer_data_source = models_explorer_data_source
        self.args = args

        params = exploremodels.ExplorerParams(self.args.cv, self.args.search_estimators)
        self.explorer = exploremodels.ModelsExplorer(params, self.ProgressWatcher(self))

    def explore_models(self):
        messages, cluster_labels = self.clustered_messages_data_source.get_messages()
        message_classes = self.message_classes_data_source.get_classes()
        classes = []
        for label in cluster_labels:
            for message_class in message_classes:
                if label in message_class.cluster_indexes:
                    classes.append(message_class.name)
                    break
        self.explorer.explore_models(messages, classes)
        self.models_explorer_data_source.save_results(self.explorer.results)

    class ProgressWatcher(exploremodels.ExploreProgress):

        def __init__(self, use_case):
            self.use_case = use_case

        def on_exploration_started(self):
            self.use_case.logger.log('start searching through models')

        def on_explored_model(self, model_name: str):
            self.use_case.logger.log(f'search finished with {model_name}')

        def on_results_ready(self):
            self.use_case.logger.log('search finished!')
