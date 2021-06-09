import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.controllers import dataset_controller, infrastructure_controller, jobs_controller, models_controller

app = FastAPI(version='2.0', title='BMW Semantic Segmentation Docker SDK API',
              description="API for managing training containers")

app.mount("/models_services", StaticFiles(directory="/checkpoints/servable"), name="models_services")

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )
app.include_router(
    dataset_controller.router,
    prefix="/dataset",
    tags=["dataset"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    infrastructure_controller.router,
    prefix="/infrastructure",
    tags=["infrastructure"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    jobs_controller.router,
    prefix="/jobs",
    tags=["jobs"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    models_controller.router,
    prefix="/models",
    tags=["models"],
    responses={404: {"description": "Not found"}},

)
if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=5555)
