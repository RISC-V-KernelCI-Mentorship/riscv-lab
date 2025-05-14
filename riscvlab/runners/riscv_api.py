import requests
import logging

logger = logging.getLogger(__name__)

class RiscVAPIRunner:

    def __init__(self, url, tests, test_collection):
        self.__service_url = url
        self.__tests = tests
        self.__test_collection = test_collection

    def __call__(self, kernel_url, selftests_url, modules_url, build_id):
        inputs = {
                "kernel_image_url": kernel_url,
                "tests": self.__tests,
                "collection": self.__test_collection,
                "modules_url": modules_url,
                "build_id": build_id,
        }
        logger.info(f"Running RISCV API Runner: {inputs}")
        try:
            requests.post(self.__service_url, json=inputs)
        except Exception as e:
            logger.warning(f"Could not run RISC-V API runner: {str(e)}")


class RiscVAPIBootRunner:

    def __init__(self, url):
        self.__service_url = url

    def __call__(self, kernel_url, selftests_url, modules_url, build_id):
        inputs = {
                "kernel_image_url": kernel_url,
                "modules_url": modules_url,
                "build_id": build_id,
        }
        logger.info(f"Running RISCV API Boot testing Runner: {inputs}")
        try:
            requests.post(self.__service_url, json=inputs)
        except Exception as e:
            logger.warning(f"Could not run RISC-V API runner: {str(e)}")