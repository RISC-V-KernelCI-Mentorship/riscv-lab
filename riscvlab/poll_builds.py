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
import os
from events import pollevents, processevents
from logging.handlers import RotatingFileHandler

LOGGING_FORMAT = "[%(asctime)s][%(levelname)s][%(name)s] %(message)s"
logger = logging.getLogger(__name__)


def main():

    parser = argparse.ArgumentParser(description="Listen to events in Maestro.")
    parser.add_argument("--kind", default="kbuild", help="The kind of events")
    parser.add_argument("--arch", default="riscv", help="The arch whose events we'll keep")
    parser.add_argument("--debug", default=False,
                        action=argparse.BooleanOptionalAction, help="Marks service as debug")
    args = parser.parse_args()
    logging.basicConfig(format=LOGGING_FORMAT,
                        level=logging.DEBUG if args.debug else logging.INFO)
    rotating_handler = RotatingFileHandler(os.getenv("LOGS_LOCATION"),
                                           maxBytes=20*1024, backupCount=2)
    logger.addHandler(rotating_handler)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    while True:
        try:
            events, last_timestamp = pollevents(args.kind, args.arch)
            processevents(events, last_timestamp)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
