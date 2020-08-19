from abc import ABC, abstractmethod
from typing import List
from core.makeclusters.models import MakerResults


class ClustersExplanationDataSource(ABC):

    @abstractmethod
    def set_explanation(self, explanations: List[MakerResults.ClusterExplanation]):
        pass

    @abstractmethod
    def get_explanation(self) -> List[MakerResults.ClusterExplanation]:
        pass
