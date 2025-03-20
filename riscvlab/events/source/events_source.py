from abc import ABC, abstractmethod

class EventsSource(ABC):

    @abstractmethod
    def poll_events(self, timestamp: str, kind: str, arch: str):
        """
        Polls events from a source.
        It might be a service, a local source, or other
        """
        ...

