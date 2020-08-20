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
            has_substrs = False
            for substr in self.params.ignored_substrings:
                if substr in message.text:
                    has_substrs = True
                    break
            if not has_substrs and message.peer_id not in self.params.ignored_peers:
                filtered_messages.append(message)
        self.results = FilterResult(filtered_messages)
