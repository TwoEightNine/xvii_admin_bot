from typing import List

from core.model import Message
from .models import FilterParams, FilterResult


class MessageFilterer:

    def __init__(self, params: FilterParams):
        self.params = params
        self.results = None

    def filter(self, messages: List[Message]):
        filtered_messages = []
        for message in messages:
            if self.params.filter_func(message):
                filtered_messages.append(message)
        self.results = FilterResult(filtered_messages)
