from abc import ABC, abstractmethod

class EventsStorage(ABC):

    @abstractmethod
    def store_timestamp(self, timestamp: str):
        """
        Stores the timestamp in persistent memory
        """
        ...

    @abstractmethod
    def get_stored_timestamp(self):
        ...
