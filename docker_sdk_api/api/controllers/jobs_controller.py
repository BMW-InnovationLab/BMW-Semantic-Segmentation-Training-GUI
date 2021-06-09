from typing import List

from fastapi import APIRouter, HTTPException
from containers import Services
from domain.exceptions.application_error import ApplicationError
from domain.models.api_response import ApiResponse
from domain.models.container_info import ContainerInfo
from domain.models.container_settings import ContainerSettings

router = APIRouter()
job_management_service = Services.job_management_service()
job_utility_service = Services.job_utility_service()

"""
Gets all the running training jobs.

Returns
-------
list of str
    a list of all running training jobs names

"""


@router.get("/")
async def get_running_jobs() -> List[str]:
    try:
        return job_utility_service.get_all_jobs()
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Starts a job

Parameters
----------
containerSettings: ContainerSettnigs
                   object of type ContainerSettings containing all the necessary info to start a job
Returns
-------
ApiResponse
    Success Message
"""


@router.post("/start")
async def start_container(container_settings: ContainerSettings) -> ApiResponse:
    try:
        job_management_service.start_container(container_settings=container_settings)
        return ApiResponse(success=True, data="Container Started")
    except ApplicationError as e:
        raise HTTPException(status_code=404, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.__str__())


"""
Stops a specific job

Parameters
----------
containerInfo: ContainerInfo
               object of type ContainerInfo containing the container name 

Returns
-------
ApiResponse
    Success Message
"""


@router.post("/stop")
async def stop_container(container_info: ContainerInfo) -> ApiResponse:
    try:
        job_management_service.stop_container(container_info=container_info)
        return ApiResponse(success=True, data="Job Killed")
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Get logs for a specific job

Parameters
----------
containerInfo: ContainerInfo
               object of type ContainerInfo containing the container name 

Returns
-------
list of str
    logs of the job
"""


@router.post("/container/logs")
async def get_job_logs(container_info: ContainerInfo) -> List[str]:
    try:
        return job_utility_service.get_container_logs(container_info=container_info)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Get all finished jobs by comparing the models that are in the servable folder (done training) with the models currently in progress 

Returns
-------
list of str
    finished jobs names
"""


@router.get("/container/finished")
async def get_finished_jobs() -> List[str]:
    try:
        return job_utility_service.get_finished_jobs()
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
