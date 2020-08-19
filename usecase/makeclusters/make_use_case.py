from core import makeclusters

from usecase.datasource import MessageDataSource, ClusteredMessageDataSource, ClustersExplanationDataSource
from .models import MakerArgs


class MakeUseCase:

    def __init__(self, message_data_source: MessageDataSource,
                 clustered_message_data_source: ClusteredMessageDataSource,
                 clusters_explanation_data_source: ClustersExplanationDataSource,
                 args: MakerArgs):
        self.message_data_source = message_data_source
        self.clustered_message_data_source = clustered_message_data_source
        self.clusters_explanation_data_source = clusters_explanation_data_source
        self.args = args

        params = makeclusters.MakerParams(args.clusters_count, args.random_state)
        self.maker = makeclusters.ClusterMaker(params)

    def make_clusters(self):
        messages = self.message_data_source.get_messages()
        messages = [message.text for message in messages]
        self.maker.make_clusters(messages)

        results = self.maker.results
        self.clustered_message_data_source.set_messages(messages, results.message_labels)
        self.clusters_explanation_data_source.set_explanation(results.explanation)
