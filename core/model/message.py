class Message:
    """
    class that represents a message
    """

    def __init__(self, id, peer_id, text: str, time_stamp: int):
        self.id = id
        self.peer_id = peer_id
        self.text = text
        self.time_stamp = time_stamp
