#!/usr/bin/env python3
"""
This example will retrieve the latest events from the KernelCI API
and print them to the console.
It will filter only completed kernel builds, limit to 100 events per request,
and retrieve corresponding nodes with artifacts.
"""
import argparse
import requests
import logging
import json
import sys
import time

LOGGING_FORMAT = "[(asctime)s][%(levelname)s][%(name)s] %(message)s"

# This is staging server: "https://staging.kernelci.org:9000/latest"
# For production use "https://kernelci-api.westus3.cloudapp.azure.com/latest/"
BASE_URI = "https://staging.kernelci.org:9000/latest"
EVENTS_PATH = "/events"

# Start from the beginning of time, but you might implement
# saving last processed timestamp to a file or database
timestamp = "1970-01-01T00:00:00.000000"
logger = logging.getLogger(__name__)

def processevent(event):
    """
    event:

    json event to process. It includes the kernel image and selftests.
    """
    kernel_image = event["node"]["artifacts"]["kernel"]
    selftests = event["node"]["artifacts"]["kselftest_tar_gz"]


def pollevents(timestamp, kind, arch):
    """
    kind:
    
    There are a few different kinds:
    
    * checkout: a new git tree checkout to be tested. Maestro frequently cuts
        new tree checkout from tree it is subscribed to. See 'config/pipeline.yaml'
    * kbuild: a new kernel build for a given config and arch
    * job: the execution of a test suite
    * test: the execution of a test inside a job
    
    
    state:
    
    In this example we track state=done to get an event when Maestro is ready to
    provide all the information about the node. Eg for checkout it will provide
    the commit hash to test and for builds the location of the kernel binaries built.
    """
    url = BASE_URI + EVENTS_PATH + f"?state=done&kind={kind}&limit=100&recursive=true&from={timestamp}"
    response = requests.get(url)
    response.raise_for_status()
    json_response = response.json()
    # We skip builds with result != pass
    filtered_events = [event for event in json_response if event["data"]["result"] == "pass" and event["data"]["data"]["arch"] == arch]
    return filtered_events


def main():
    global timestamp

    parser = argparse.ArgumentParser(description="Listen to events in Maestro.")
    parser.add_argument("--kind", default="kbuild", help="The kind of events")
    parser.add_argument("--arch", default="riscv", help="The arch whose events we'll keep")
    parser.add_argument("--debug", default=False,
                        action=argparse.BooleanOptionalAction, help="Marks service as debug")
    args = parser.parse_args()
    logging.basicConfig(filename="process_builds.log",
                        format=LOGGING_FORMAT,
                        level=logging.DEBUG if args.debug else logging.INFO)
    while True:
        try:
            events = pollevents(timestamp, args.kind, args.arch)
            if len(events) == 0:
                logger.info("No new events, sleeping for 30 seconds")
                time.sleep(30)
                continue
            logger.info(f"Got {len(events)} events")
            for event in events:
                logger.debug(json.dumps(event, indent=2))
                processevent(event)
                timestamp = event["timestamp"]
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
