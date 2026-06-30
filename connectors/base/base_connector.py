from abc import ABC, abstractmethod

class BaseConnector(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def search(self, query, max_results=10):
        pass

    def connector_info(self):
        return {
            "name": self.name,
            "type": "AROS Connector",
            "status": "available"
        }
