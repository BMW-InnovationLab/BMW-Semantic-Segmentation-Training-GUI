from pydantic import BaseModel


class Paths(BaseModel):
    base_dir: str
    image_name: str
    api_folder: str
    dataset_folder_on_host: str
    checkpoints_folder_on_host: str
    inference_api_models_folder: str
    classifier_folder_on_host: str
    servable_folder_on_host: str

    classifier_folder: str
    dataset_folder: str
    checkpoints_folder: str
    servable_folder: str
    networks_path: str
