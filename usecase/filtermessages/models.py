from typing import List


class FilterArgs:

    def __init__(self, ignored_peers: List[int], ignored_substrs: List[str]):
        self.ignored_peers = ignored_peers
        self.ignored_substrs = ignored_substrs
