import logging
import kcidb
import json
import yaml
import os
from test_results.submit.submitters.tests_submitter import KSelftestsResultsSubmitter

logger = logging.getLogger(__name__)

class KCITestResultsSubmitter(KSelftestsResultsSubmitter):

    def __init__(self, debug):
        config_path = os.path.join(os.path.dirname(__file__), "kcidb.yml")
        with open(config_path, "r") as f:
            config_file = yaml.safe_load(f)
        self.__client = kcidb.Client(project_id=config_file["kcidb"]["project_id"],
                                     topic_name=config_file["kcidb"]["topic"])
        self.__version_major = config_file["kcidb"]["major"]
        self.__version_minor = config_file["kcidb"]["minor"]
        self.__debug = debug

    def submit(self, tests):
        report = {
            "tests": [test.to_json() for test in tests],
            "version": {
                "major": self.__version_major,
                "minor": self.__version_minor
            }
        }
        if self.__debug:
            logger.info(report)
        else:
            self.__client.submit(report)

