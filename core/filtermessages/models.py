from core.model import Message
from typing import List, Optional


class TimeConstraint:

    def __init__(self, from_time: Optional[int] = None, until_time: Optional[int] = None):
        self.from_time = from_time
        self.until_time = until_time


class FilterParams:

    def __init__(self, time_constraint: TimeConstraint, ignored_peers: List[int], ignored_substrings: List[str]):
        self.time_constraint = time_constraint
        self.ignored_peers = ignored_peers
        self.ignored_substrings = ignored_substrings


class FilterResult:

    def __init__(self, messages: List[Message]):
        self.messages = messages
