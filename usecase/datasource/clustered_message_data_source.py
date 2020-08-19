from abc import ABC, abstractmethod


class ClusteredMessageDataSource(ABC):

    @abstractmethod
    def set_messages(self, messages: list, cluster_labels: list):
        pass

    @abstractmethod
    def get_messages(self) -> tuple:
        pass
