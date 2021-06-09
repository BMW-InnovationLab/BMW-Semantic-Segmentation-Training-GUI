import socket
from typing import List
from domain.services.contracts.abstract_port_scanner_service import AbstractPortScannerService

from domain.exceptions.infrastructure_exception import ErrorReadingAvailableSockets


class PortScannerService(AbstractPortScannerService):

    def get_used_ports(self) -> List[str]:
        try:
            used_ports: List[str] = []

            for port in range(1, 65535):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((socket._LOCALHOST, port))
                if result == 0:
                    used_ports.append(str(port))
                sock.close()
            return used_ports
        except Exception:
            raise ErrorReadingAvailableSockets()
