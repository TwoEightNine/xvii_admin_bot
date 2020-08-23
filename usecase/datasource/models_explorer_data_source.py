from abc import ABC, abstractmethod
from core.exploremodels.models import ExplorerResult


class ModelsExplorerDataSource(ABC):

    @abstractmethod
    def save_results(self, results: ExplorerResult):
        pass

    @abstractmethod
    def get_results(self) -> ExplorerResult:
        pass
