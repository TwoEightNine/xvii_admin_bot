class Message:
    """
    class that represents a message
    """

    def __init__(self, id, peer_id, text):
        self.id = id
        self.peer_id = peer_id
        self.text = text
