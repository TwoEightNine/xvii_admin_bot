from abc import ABC, abstractmethod
from typing import Optional


class Logger(ABC):

    @abstractmethod
    def log(self, message: str, exception: Optional[Exception] = None):
        pass

    @abstractmethod
    def indicate_progress(self, done, total):
        pass
