from abc import ABC, abstractmethod


class BaseAutomationEngine(ABC):

    @abstractmethod
    def run_report(self, config: dict) -> bool:
        pass


    @abstractmethod
    def close(self):
        pass