from fastapi import APIRouter, HTTPException, BackgroundTasks

from containers import Managers
from domain.exceptions.application_error import ApplicationError
from domain.models.api_response import ApiResponse
from domain.models.dataset_information import DatasetInformation
from domain.models.hyper_parameter_information import HyperParameterInformation

router = APIRouter()
configuration_factory = Managers.configuration_factory()
model_train_evaluate_manager = Managers.model_train_evaluate_manager()
"""
Get Default Configuration Content 

Returns
-------
HyperParameterInformation
    HyperParameterInformation Object containing default configuration content 
"""


@router.post('/default')
async def default_configuration():
    try:
        return HyperParameterInformation()
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
