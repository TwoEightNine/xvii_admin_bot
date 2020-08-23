from typing import Dict, List, Tuple

from sklearn.base import BaseEstimator


class ExplorerArgs:

    def __init__(self, cv: int, search_estimators: List[Tuple[BaseEstimator, Dict[str, list]]]):
        self.cv = cv
        self.search_estimators = search_estimators
