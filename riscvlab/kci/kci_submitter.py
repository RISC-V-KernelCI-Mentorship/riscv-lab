import logging
import kcidb
import json
from test_results.submit.submitters.tests_submitter import KSelftestsResultsSubmitter
from kci.node import get_node, create_node, update_node

logger = logging.getLogger(__name__)

class KCITestResultsSubmitter(KSelftestsResultsSubmitter):
    # TODO: Move this to a config file
    __version_major = 5
    __version_minor = 1
    __project_id = "kernelci-production"
    __topic_name = "playground_kcidb_new"

    def __init__(self, debug):
        self.__client = kcidb.Client(project_id=self.__project_id,
                                     topic_name=self.__topic_name)
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

