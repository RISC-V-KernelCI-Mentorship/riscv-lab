from datetime import datetime, timezone
from test_results.submit.parser.tests import KSelftestBuilder, KSelftestTestResult

class KCIKSelftestBuilder(KSelftestBuilder):
    def __init__(self, id_generator, build_id):
        self.__id_generator = id_generator
        self.__build_id = build_id

    def build(self, collection, name, result, log):
        return KCIKSelftestTestResult(collection, name, result, log,
                                      self.__id_generator(collection, name),
                                      self.__build_id)


class KCIKSelftestTestResult(KSelftestTestResult):
    __origin = "riscv"

    def __init__(self, collection, name, result, log, test_id, build_id):
        self.__test_id = test_id
        self.__build_id = build_id
        super().__init__(collection, name, result, log)

    def to_json(self):
        return {
                "id": f"{self.__origin}:{self.__test_id}",
                "build_id": self.__build_id,
                "origin": self.__origin,
                "status": self.result,
                "path": self.get_path(),
                "start_time": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                "misc": {}
            }

