from typing import List

from fastapi import APIRouter, HTTPException

from domain.exceptions.application_error import ApplicationError
from domain.models.datase_information import DatasetInformation
from containers import Services

from domain.models.api_response import ApiResponse

dataset_service = Services.dataset_service()
dataset_validator_service = Services.dataset_validator_service()
object_classes_discovery_service = Services.object_classes_discovery_service()
router = APIRouter()

"""
Get all datasets

Returns
-------
list of str
    datasets
"""


@router.get("/")
async def get_datasets() -> List[str]:
    try:
        return dataset_service.get_datasets()
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Checks if a dataset is valid

Parameters
----------
datasetInfo: DatasetInfo
             object of type DatasetInfo containing the dataset path 

Returns
-------
Boolean
        true if the dataset is valid, false otherwise

"""


@router.post("/validate")
async def get_object_classes(dataset_info: DatasetInformation) -> ApiResponse:
    try:
        dataset_validator_service.validate_dataset(dataset_info=dataset_info)
        return ApiResponse(success=True)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Get the object classes for a specific dataset


Parameters
----------
datasetInfo: DatasetName
             object of type DatasetName containing the dataset name

Returns
-------
datasetInfo: DatasetName
             object of type DatasetName containing the dataset name
"""


@router.post("/classes")
async def get_object_classes(dataset_info: DatasetInformation) -> DatasetInformation:
    try:
        classes: List[str] = object_classes_discovery_service.discover_object_classes(dataset_info=dataset_info).classes
        return DatasetInformation(dataset_name=dataset_info.dataset_name, classes=classes, num_classes=len(classes))
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
