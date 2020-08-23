from typing import List


class MessageClass:

    def __init__(self, name: str, cluster_indexes: List[int], response: str):
        self.name = name
        self.cluster_indexes = cluster_indexes
        self.response = response
