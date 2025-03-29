import re
import logging

_selftest_re = re.compile(r"(?P<status>\w+( \w+)?) +\d+ +selftests: +\w+: +(?P<name>[^#\s]+)( +# +(?P<extra>.*))?\s")
_boot_failed_re = re.compile(r"\[[.0-9 ]+\] +Kernel panic")
_collection_re = re.compile(r".*kselftest-(?P<collection>.*)\.log")
logger = logging.getLogger(__name__)

def parse_ktests_from_log(log_file, test_builder, submit_as_collections):
    try:
        collection_match = _collection_re.match(log_file)
        if collection_match is None:
            return None
        collection = collection_match.groupdict()["collection"]
        with open(log_file, "r") as f:
            log_content = f.read()
        if _boot_failed_re.search(log_content) is not None:
            return [test_builder.build(collection, 
                                        "", "MISS", 
                                        log_content)]

        m = _selftest_re.finditer(log_content)
        if submit_as_collections:
            return _process_collection_tests(m, test_builder, collection, log_content) 
        return _process_individual_tests(m, test_builder, collection, log_content)

    except KeyError as e:
        logger.error(f"Test results has an invalid format")
        return None
    except Exception as e:
        logger.warning(f"Could not parse log: {str(e)}")
        return None

def _process_individual_tests(matches, test_builder, collection, log_content):
    results = []
    for match in matches:
        groups = match.groupdict()
        result = "PASS"
        status = groups["status"]
        extra = groups["extra"]
        if status == "ok" and extra == "SKIP":
            result = "SKIP"
        elif status == "not ok" and extra is None:
            result = "FAIL"
        elif status == "not ok" and extra is not None:
            result = "ERROR"
        results.append(test_builder.build(collection, 
                                          groups["name"], 
                                          result, 
                                          log_content))
    return results


def _process_collection_tests(matches, test_builder, collection, log_content):
    status = "SKIP"
    for match in matches:
        groups = match.groupdict()
        test_status = groups["status"]
        extra = groups["extra"]
        # FAIL is highest priority
        if test_status == "not ok" and extra is None:
            status = "FAIL"
            break
        elif test_status == "not ok" and extra is not None:
            status = "ERROR"
        elif test_status == "ok" and extra == "SKIP" and status == "SKIP":
            status = "SKIP"
        elif test_status == "ok" and extra != "SKIP" and status != "ERROR":
            status = "PASS"
                                                                     
    return [test_builder.build(collection, "", status, log_content)]
