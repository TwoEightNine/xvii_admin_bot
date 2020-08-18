from abc import ABC, abstractmethod


class MessageDataSource(ABC):

    @abstractmethod
    def get_messages(self) -> list:
        pass

    @abstractmethod
    def set_messages(self, messages: list):
        pass
