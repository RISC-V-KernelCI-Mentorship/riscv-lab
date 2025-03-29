from abc import ABC, abstractmethod

class KSelftestBuilder(ABC):

    def __init__(self, test_class):
        self.__test_class = test_class

    @abstractmethod
    def build(self, collection, name, result, log):
        ...

class KSelftestTestResult(ABC):
    def __init__(self, collection, name, result, log):
        self.__name = name
        self.__collection = collection
        self.result = result
        self.log = log
    
    def get_path(self):
        test_path = f"kselftest.{self.__collection}"
        if self.__name is not None and len(self.__name):
            test_path = f"{test_path}.{self.__name.replace('.','_')}"
        return test_path

    @abstractmethod
    def to_json(self):
        ...

