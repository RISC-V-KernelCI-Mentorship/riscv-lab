from events.storage.events_storage import EventsStorage
from events.storage.file_storage import FileEventsStorage

_start_timestamp = "1970-01-01T00:00:00.000000"
storage = FileEventsStorage(_start_timestamp)

