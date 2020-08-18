from abc import ABC, abstractmethod


class ExploreProgress(ABC):

    @abstractmethod
    def on_exploration_started(self):
        pass

    @abstractmethod
    def on_explored_clusters(self, clusters_count: int):
        pass

    @abstractmethod
    def on_results_ready(self):
        pass
