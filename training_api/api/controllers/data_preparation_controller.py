from fastapi import APIRouter, HTTPException

from containers import Managers
from domain.exceptions.application_error import ApplicationError
from domain.models.api_response import ApiResponse
from domain.models.dataset_information import DatasetInformation
from domain.models.hyper_parameter_information import HyperParameterInformation

router = APIRouter()
dataset_preparation_manager = Managers.dataset_preparation_manager()
"""
Create Dataset Objects and store them in memory   
Parameters
----------
dataset_info: DatasetInformation
                object of type DatasetInformation containing the dataset name, classes names , classes number and the train test split ratio
config: HyperParameterInformation
                object of type HyperParameterInformation containing all hyper parameters information 
Returns
-------
ApiResponse
    Success Message
"""


@router.post('/')
async def prepare_dataset(dataset_info: DatasetInformation, config: HyperParameterInformation):
    try:
        dataset_preparation_manager.prepare_dataset(dataset_info=dataset_info, config=config)
        return ApiResponse(success=True, data="dataset preparation successful")
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
