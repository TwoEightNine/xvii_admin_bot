from typing import Dict, List, Tuple

from sklearn.base import BaseEstimator
from core.model import ClassificationMetrics


class ExplorerParams:

    def __init__(self, cv: int, search_estimators: List[Tuple[BaseEstimator, Dict[str, list]]]):
        self.cv = cv
        self.search_estimators = search_estimators


class ExplorerResult:

    def __init__(self):
        self._model_to_metrics_dict = {}

    def add_result(self, model: Tuple[str, Dict[str, list]], metrics: ClassificationMetrics):
        self._model_to_metrics_dict[model] = metrics

    def get_results(self):
        return self._model_to_metrics_dict.copy()
