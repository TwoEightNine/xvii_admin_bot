from abc import ABC, abstractmethod
from typing import List

from core.model import Message


class MessageDataSource(ABC):

    @abstractmethod
    def get_messages(self) -> List[Message]:
        pass

    @abstractmethod
    def set_messages(self, messages: List[Message]):
        pass
