from abc import ABC, abstractmethod
from test_results.submit.parser.tests import KSelftestTestResult

class KSelftestsResultsSubmitter(ABC):
    
    @abstractmethod
    def submit(self, tests: list[KSelftestTestResult]):
        ...

