from abc import ABC, abstractmethod
from core.model import Prediction


class Predictor(ABC):

    @abstractmethod
    def predict(self, message) -> Prediction:
        pass
