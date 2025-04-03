import os
import logging
from events.storage.events_storage import EventsStorage

logger = logging.getLogger(__name__)

class FileEventsStorage(EventsStorage):
    __FILE_PATH = os.getenv("EVENTS_STORAGE")

    def __init__(self, initial_timestamp):
        try:
            with open(self.__FILE_PATH, "r+") as f:
                line = f.readline()
                logger.debug(f"Current timestamp: {line}")
                if not line.strip():
                    f.write(initial_timestamp)
        except Exception as e:
            raise Exception(f"Could not open events storage: {str(e)}")
    
    def store_timestamp(self, timestamp: str):
        with open(self.__FILE_PATH, "w") as timestamp_f:
            timestamp_f.write(timestamp)


    def get_stored_timestamp(self):
        with open(self.__FILE_PATH, "r") as timestamp_f:
            return timestamp_f.readline().strip()

