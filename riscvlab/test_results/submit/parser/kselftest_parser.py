import re
import logging

_selftest_re = re.compile(r"(?P<status>\w+( \w+)?) +\d+ +selftests: +\w+: +(?P<name>[^# ]+)( +# +(?P<extra>.*))?\s")
_boot_failed_re = re.compile(r"\[[.0-9 ]+\] +Kernel panic")
_collection_re = re.compile(r".*kselftest-(?P<collection>.*)\.log")
logger = logging.getLogger(__name__)

def parse_from_log(log_file, test_builder):
    results = []
    try:
        collection_match = _collection_re.match(log_file)
        if collection_match is None:
            return None
        collection = collection_match.groupdict()["collection"]
        with open(log_file, "r") as f:
            log_content = f.read()
        if _boot_failed_re.search(log_content) is not None:
            results.append(test_builder.build(collection, 
                                              "", "MISS", 
                                              log_content))
            return results

        m = _selftest_re.finditer(log_content)
        for match in m:
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
                                              groups["name"], status, 
                                              log_content))
        return results

    except KeyError as e:
        logger.error(f"Test results has an invalid format")
        return None
    except Exception as e:
        logger.warning(f"Could not parse log: {str(e)}")
        return None
