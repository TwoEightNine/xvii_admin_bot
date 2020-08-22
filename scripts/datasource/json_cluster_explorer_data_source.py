from core import ExplorerResults
from core.model import ClusteringMetrics
from usecase.datasource import ClusterExplorerDataSource

import json


class JsonClusterExplorerDataSource(ClusterExplorerDataSource):
    column_clusters_count = 'clusters_count'
    column_silhouette_score = 'silhouette_score'
    column_davis_bouldin_score = 'davis_bouldin_score'
    column_calinski_harabasz_score = 'calinski_harabasz_score'

    def __init__(self, file_name: str):
        self.file_name = file_name

    def save_results(self, results: ExplorerResults):
        with open(self.file_name, 'w') as fp:
            results_dict = {}
            for cc, metrics in results.get_results().items():
                results_dict[cc] = {
                    self.column_silhouette_score: metrics.silhouette,
                    self.column_davis_bouldin_score: metrics.davis_bouldin,
                    self.column_calinski_harabasz_score: metrics.calinski_harabasz
                }
            json.dump(results_dict, fp, indent=4)

    def get_results(self) -> ExplorerResults:
        results = ExplorerResults()
        with open(self.file_name, 'r') as fp:
            loaded_results = json.load(fp)
            for clusters_count, metrics in loaded_results.items():
                results.add_metrics(clusters_count, ClusteringMetrics(
                    silhouette=metrics[self.column_silhouette_score],
                    davis_bouldin=metrics[self.column_davis_bouldin_score],
                    calinski_harabasz=metrics[self.column_calinski_harabasz_score]
                ))
        return results
