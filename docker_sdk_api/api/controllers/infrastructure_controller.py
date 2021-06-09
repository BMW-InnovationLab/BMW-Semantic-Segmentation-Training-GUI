from typing import Dict, List

from fastapi import APIRouter, HTTPException
from containers import Services
from domain.exceptions.application_error import ApplicationError
from application.infrastructure.services.gpu_service import GpuService
from application.infrastructure.services.port_scanner_service import PortScannerService

router = APIRouter()

"""
Gets the available gpus.

Returns
-------
Dict of str
    a Dict of gpu names with less than 25% memory consumption and corresponding name and avialable memory

"""


@router.get("/gpu/info")
async def get_gpu_info() -> Dict[str, str]:
    try:
        return GpuService().get_gpu_info()
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Get all the used ports on the system

Returns
-------
list of str
    used ports
"""


@router.get("/used/ports")
async def get_used_ports() -> List[str]:
    try:
        return PortScannerService().get_used_ports()
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
