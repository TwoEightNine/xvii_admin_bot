import json

from usecase.datasource import ClustersExplanationDataSource

from typing import List
from core.makeclusters.models import MakerResults


class JsonClustersExplanationDataSource(ClustersExplanationDataSource):

    key_cluster_index = 'cluster_index'
    key_words_count = 'words_count'
    key_frequent_words = 'frequent_words'

    def __init__(self, file_name: str):
        self.file_name = file_name

    def set_explanation(self, explanations: List[MakerResults.ClusterExplanation]):
        data = {}
        for explanation in explanations:
            data[explanation.cluster_index] = {
                self.key_cluster_index: explanation.cluster_index,
                self.key_words_count: explanation.words_count,
                self.key_frequent_words: explanation.frequent_words
            }
        with open(self.file_name, 'w') as fp:
            json.dump(data, fp, indent=4, ensure_ascii=False)

    def get_explanation(self) -> List[MakerResults.ClusterExplanation]:
        with open(self.file_name, 'r') as fp:
            data = json.load(fp)
            explanations = []
            for exp in data.values():
                explanations.append(MakerResults.ClusterExplanation(
                    cluster_index=exp[self.key_cluster_index],
                    words_count=exp[self.key_words_count],
                    frequent_words=exp[self.key_frequent_words]
                ))
            return explanations
