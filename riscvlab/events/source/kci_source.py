import logging
import requests
import argparse
from libs.requests import create_session
from events.source.events_source import EventsSource

logger = logging.getLogger(__name__)

_BASE_URI = "https://staging.kernelci.org:9000/latest"
_EVENTS_PATH = "/events"

class KernelCISource(EventsSource):
    
    def poll_events(self, timestamp: str, kind: str, arch: str):
        s = create_session(_BASE_URI)
        url = _BASE_URI + _EVENTS_PATH + f"?state=done&kind={kind}&limit=100&recursive=true&from={timestamp}"
        try:
            response = s.get(url)
            response.raise_for_status()
            json_response = response.json()
            last_timestamp = json_response[-1]["timestamp"] if len(json_response) > 0 else ""
            # We skip builds with result != pass
            filtered_events = [event for event in json_response if event["data"]["result"] == "pass" and event["data"]["data"]["arch"] == arch]
            return filtered_events, last_timestamp
        except requests.exceptions.RequestException as e:
            logger.warning(f"Could not obtain builds from KernelCI: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Obtains builds from KernelCI")
    parser.add_argument("--timestamp", required=True, help="We obtain builds from this moment forward")
    parser.add_argument("--arch", required=True, help="Arch used to filter builds")
    args = parser.parse_args()
    source = KernelCISource()
    events, timestamp = source.poll_events(args.timestamp, "kbuild", args.arch)
    print(f"Last timestamp: {timestamp}")
    print(events)

