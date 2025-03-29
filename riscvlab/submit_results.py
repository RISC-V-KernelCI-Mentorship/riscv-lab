#!/usr/bin/python3 
import argparse
import os
import re
import sys
import hashlib
import logging
from test_results.submit.parser.kselftest_parser import parse_ktests_from_log
from kci.kci_submitter import KCITestResultsSubmitter
from kci.kci_tests_results import KCIKSelftestBuilder, KCIKSelftestTestResult

logger = logging.getLogger(__name__)

def _generate_test_id(collection, name):
    base_id = os.getenv("RISCV_KCIDB_TEST_ID", "")
    test_id = f"{base_id}-{collection}-{name}".encode()
    sha256 = hashlib.sha256()
    sha256.update(test_id)
    return sha256.hexdigest()

def submit_test_results(build_id, logs_dir, submit_as_collections, only_print):
    tests = []
    builder = KCIKSelftestBuilder(_generate_test_id, build_id)
    submitter = KCITestResultsSubmitter(only_print)
    for (dirpath, _, filenames) in os.walk(logs_dir):
        for file in filenames:
            log = os.path.join(dirpath, file)
            parsed_tests = parse_ktests_from_log(log, builder, submit_as_collections)
            if parsed_tests is not None:
                tests += parsed_tests

    submitter.submit(tests)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    
    parser = argparse.ArgumentParser(description="Submit results to KCIDB")
    parser.add_argument("--build-id", required=True, help="Maestro build id")
    parser.add_argument("--logs-dir", required=True, help="Tests logs directory")
    parser.add_argument("--submit-as-collections", default=False, 
                        action=argparse.BooleanOptionalAction,
                        help="Submit results per collection (instead of individual tests)")
    parser.add_argument("--only-print", default=False,
                        action=argparse.BooleanOptionalAction,
                        help="Do not submit the tests, only print the payload")

    args = parser.parse_args()
    submit_test_results(args.build_id, args.logs_dir, args.submit_as_collections, 
                        args.only_print)

