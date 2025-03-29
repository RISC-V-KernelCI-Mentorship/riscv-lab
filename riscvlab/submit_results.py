#!/usr/bin/python3 
import argparse
import os
import re
import sys
import hashlib
import logging
from test_results.submit.parser.kselftest_parser import parse_from_log
from kci.kci_submitter import KCITestResultsSubmitter
from kci.kci_tests_results import KCIKSelftestBuilder, KCIKSelftestTestResult

logger = logging.getLogger(__name__)

def _generate_test_id(collection, name):
    base_id = os.getenv("RISCV_KCIDB_TEST_ID", "")
    test_id = f"{base_id}-{collection}-{name}".encode()
    sha256 = hashlib.sha256()
    sha256.update(test_id)
    return sha256.hexdigest()

def submit_test_results(build_id, logs_dir):
    tests = []
    builder = KCIKSelftestBuilder(_generate_test_id, build_id)
    submitter = KCITestResultsSubmitter()
    for (dirpath, _, filenames) in os.walk(logs_dir):
        for file in filenames:
            log = os.path.join(dirpath, file)
            parsed_tests = parse_from_log(log, builder)
            if parsed_tests is not None:
                tests += parsed_tests

    logger.debug([test.to_json() for test in tests])
    submitter.submit(tests)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    
    parser = argparse.ArgumentParser(description="Submit results to KCIDB")
    parser.add_argument("--build-id", required=True, help="Maestro build id")
    parser.add_argument("--logs-dir", required=True, help="Tests logs directory")

    args = parser.parse_args()
    submit_test_results(args.build_id, args.logs_dir)

