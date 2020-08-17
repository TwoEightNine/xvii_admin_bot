from abc import ABC, abstractmethod


class FetchOutput(ABC):

    @abstractmethod
    def save_messages(self, messages: list):
        pass
