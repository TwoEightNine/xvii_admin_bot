from abc import ABC, abstractmethod


class FetchProgress(ABC):

    @abstractmethod
    def on_fetching_started(self):
        pass

    @abstractmethod
    def on_peers_fetched(self, peers_count):
        pass

    @abstractmethod
    def on_fetched_messages_out_of(self, fetched, out_of):
        pass

    @abstractmethod
    def on_messages_fetched(self):
        pass
