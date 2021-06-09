from typing import List
from abc import ABC, abstractmethod,ABCMeta


class AbstractPortScannerService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_used_ports(self) -> List[str]: raise NotImplementedError
