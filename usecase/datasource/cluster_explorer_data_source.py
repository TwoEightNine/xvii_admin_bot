from abc import ABC, abstractmethod
from core.exploreclusters.models import ExplorerResults


class ClusterExplorerDataSource(ABC):

    @abstractmethod
    def save_results(self, results: ExplorerResults):
        pass

    @abstractmethod
    def get_results(self) -> ExplorerResults:
        pass
