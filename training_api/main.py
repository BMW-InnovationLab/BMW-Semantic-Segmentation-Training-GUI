import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.controllers import data_preparation_controller, configuration_controller, training_controller, health_check_controller
from shared.helpers.directories_creator import create_required_directories

app = FastAPI(version='2.0', title='GluonCv Semantic Segmentation Training API ',
              description="API for training semantic segmentation models using GluonCv")

create_required_directories()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    data_preparation_controller.router,
    prefix="/data_preparation",
    tags=["data_preparation"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    configuration_controller.router,
    prefix="/configuration",
    tags=["configuration"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    health_check_controller.router,
    prefix="/health",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    training_controller.router,
    prefix="/training",
    tags=["training"],
    responses={404: {"description": "Not found"}},

)
# todo remove
if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=1234)
