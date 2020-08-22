from core.model import ClusteringMetrics
from typing import Dict


class ExplorerParams:

    def __init__(self, random_state: int):
        self.random_state = random_state


class ExplorerResults:

    def __init__(self):
        self._metrics_for_clusters_count = {}

    def add_metrics(self, clusters_count: int, metrics: ClusteringMetrics):
        self._metrics_for_clusters_count[clusters_count] = metrics

    def get_results(self) -> Dict[str, ClusteringMetrics]:
        return self._metrics_for_clusters_count.copy()
