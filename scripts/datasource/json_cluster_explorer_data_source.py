from core import ExplorerResults
from usecase.datasource import ClusterExplorerDataSource

import json


class JsonClusterExplorerDataSource(ClusterExplorerDataSource):
    column_clusters_count = 'clusters_count'

    def __init__(self, file_name: str):
        self.file_name = file_name

    def save_results(self, results: ExplorerResults):
        with open(self.file_name, 'w') as fp:
            results = {'results': results.get_results()}
            json.dump(results, fp, indent=4)

    def get_results(self) -> ExplorerResults:
        results = ExplorerResults()
        with open(self.file_name, 'r') as fp:
            loaded_results = json.load(fp)
            for clusters_count, metrics in loaded_results['results'].items():
                results.add_metrics(clusters_count, metrics)
        return results
