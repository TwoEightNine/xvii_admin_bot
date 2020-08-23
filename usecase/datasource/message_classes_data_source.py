from abc import ABC, abstractmethod
from typing import List
from core.model import MessageClass


class MessageClassesDataSource(ABC):

    @abstractmethod
    def get_classes(self) -> List[MessageClass]:
        pass
