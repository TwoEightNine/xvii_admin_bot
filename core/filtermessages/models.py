from typing import List, Callable

from core.model import Message


class FilterParams:

    def __init__(self, filter_func: Callable):
        self.filter_func = filter_func


class FilterResult:

    def __init__(self, messages: List[Message]):
        self.messages = messages
