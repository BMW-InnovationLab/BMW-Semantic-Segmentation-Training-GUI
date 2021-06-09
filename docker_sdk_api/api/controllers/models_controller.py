from typing import List, Dict

from fastapi import APIRouter, HTTPException

from containers import Services
from domain.exceptions.application_error import ApplicationError

router = APIRouter()

models_architecture_service = Services.models_architecture_service()
checkpoint_service = Services.checkpoint_service()
classifier_service = Services.classifier_service()
download_models_service = Services.download_models_service()
"""
Get all models architectures

Returns
-------
list of str
    models architectures
"""


@router.get("/architecture")
async def get_all_architecture() -> Dict[str, List[str]]:
    try:
        return models_architecture_service.get_architectures()
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


@router.get("/architecture/pretrained_networks")
async def get_all_architecture() -> Dict[str, List[str]]:
    try:
        return models_architecture_service.get_pretrained_models()
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Get all the pre-trained weights (or checkpoints) for a specific models architecture

Parameters
----------
networkInfo: NetworkInfo
                   object of type NetworkInfo containing the name of the models architecture

Returns
-------
dict of str
    checkpoint : network_name 
"""


@router.get("/checkpoints")
async def get_checkpoints() -> Dict[str, str]:
    try:
        return checkpoint_service.get_checkpoints()
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Get all the classifier

Returns
-------
list of str
    checkpoints
"""


@router.get("/classifiers")
async def get_classifiers() -> Dict[str, str]:
    try:
        return classifier_service.get_classifiers()
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Get all models in the static folder called servable

Returns
-------
list of str
    servable models
"""


@router.get("/downloadable")
async def get_downloadable_models() -> Dict[str, str]:
    try:
        return download_models_service.get_downloadable_models()
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
