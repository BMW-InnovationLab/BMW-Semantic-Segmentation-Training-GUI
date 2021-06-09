from fastapi import APIRouter, HTTPException, BackgroundTasks
from containers import Managers
from domain.models.api_response import ApiResponse
from domain.models.dataset_information import DatasetInformation
from domain.exceptions.application_error import ApplicationError
from domain.models.hyper_parameter_information import HyperParameterInformation

configuration_factory = Managers.configuration_factory()
model_train_evaluate_manager = Managers.model_train_evaluate_manager()
export_manager = Managers.export_manager()
router = APIRouter()

"""
Create network configuration and start  training and evaluation in the background and export the resulting model

Parameters
----------
dataset_info: DatasetInformation
                object of type DatasetInformation containing the dataset info for the training
                
                
config: HyperParameterInformation
            object of type HyperParameterInformation containing the hyper parameters for the training

Returns
-------
ApiResponse
    ApiResponse containing success status
"""


@router.post('/')
async def start_train(background_tasks: BackgroundTasks, dataset_info: DatasetInformation, config: HyperParameterInformation):
    try:
        background_tasks.add_task(configuration_factory.create_configuration, dataset_info=dataset_info, config=config)
        background_tasks.add_task(model_train_evaluate_manager.train_eval_continuously, config=config)
        background_tasks.add_task(export_manager.save_trained_model, dataset_info=dataset_info, config=config)
        return ApiResponse(success=True)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
