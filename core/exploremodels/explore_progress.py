from abc import ABC, abstractmethod


class ExploreProgress(ABC):

    @abstractmethod
    def on_exploration_started(self):
        pass

    @abstractmethod
    def on_explored_model(self, model_name: str):
        pass

    @abstractmethod
    def on_results_ready(self):
        pass
