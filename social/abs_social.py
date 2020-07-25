from abc import ABC, abstractmethod


class AbsSocial(ABC):
    """
    abstract class for social network delegates
    to add new social network, inherit this class
    and change delegate in hyperparam.py
    """

    @abstractmethod
    def get_list_of_peers(self, size: int) -> list:
        """
        fetches list of ids of peers to obtain message history
        :param size: how many peers to fetch
        :return: list of peer_id
        """
        pass

    @abstractmethod
    def get_messages(self, peer_id: int) -> list:
        """
        fetches list of messages for given peer
        :param peer_id: if od peer
        :return: messages as a list of strings
        """
        pass

    @abstractmethod
    def mark_message_as_read(self, peer_id, message_id) -> bool:
        """
        marks message as read by bot
        :param peer_id: id of peer (user, community, stc)
        :param message_id: id of message to mark as read
        :return: True if success
        """
        pass

    @abstractmethod
    def send_message(self, peer_id, message_text) -> bool:
        """
        sends message to peer
        :param peer_id: id of peer (user, community, etc)
        :param message_text: text to send
        :return: True if success
        """
        pass

    @abstractmethod
    def wait_for_messages(self) -> list:
        """
        runs periodically to obtain new messages
        :return: list of Message
        """
        pass


class Message:
    """
    class that represents a message
    """
    def __init__(self, id, peer_id, text):
        self.id = id
        self.peer_id = peer_id
        self.text = text
