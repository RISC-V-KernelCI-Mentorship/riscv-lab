import logging
import json
import time
from events.source.events_source import EventsSource
from events.storage.events_storage import EventsStorage
from events.source import source
from events.storage import storage
from runners import run_event_processing

logger = logging.getLogger(__name__)

class EventHandler:
    def __init__(self, events_source: EventsSource, events_storage: EventsStorage):
        self.__events_source = events_source
        self.__events_storage = events_storage

    def poll_events(self, kind: str, arch: str):
        timestamp = self.__events_storage.get_stored_timestamp()
        return self.__events_source.poll_events(timestamp, kind, arch)

    def process_single_event(self, event):
        """
        event:
        
        json event to process. It includes the kernel image and selftests.
        """
        kernel_image = event["node"]["artifacts"]["kernel"]
        selftests = event["node"]["artifacts"]["kselftest_tar_gz"]
        build_id = event["id"]
        
        run_event_processing(kernel_image, selftests, build_id)

    def process_events(self, events):
        if len(events) == 0:
            logger.info("No new events, sleeping for 30 seconds")
            time.sleep(30)
            return
        logger.info(f"Got {len(events)} events")
        for event in events:
            logger.debug(json.dumps(event, indent=2))
            self.process_single_event(event)
            timestamp = event["timestamp"]
            self.__events_storage.store_timestamp(timestamp)

    
_handler = EventHandler(source, storage)
def pollevents(kind, arch):
    """
    kind:
    There are a few different kinds:
    * checkout: a new git tree checkout to be tested. Maestro frequently cuts new tree checkout from tree it is subscribed to. See 'config/pipeline.yaml'
    * kbuild: a new kernel build for a given config and arch
    * job: the execution of a test suite
    * test: the execution of a test inside a job
    """

    return _handler.poll_events(kind, arch)

def processevents(events):
    """
    Processes all events. This function will probably be called
    from a while True loop
    """
    _handler.process_events(events)

