class Message:

    def __init__(self, text: str, peer_id: int, time_stamp: int):
        self.text = text
        self.peer_id = peer_id
        self.time_stamp = time_stamp


class FetchParams:

    def __init__(self, peers_count: int):
        self.peers_count = peers_count
