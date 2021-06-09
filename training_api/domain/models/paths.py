from pydantic import BaseModel


class Paths(BaseModel):
    """
        A class  used to store all necessary paths
    """
    images_dir: str
    labels_dir: str
    training_dir: str
    model_dir: str
    checkpoints_dir: str
    servable_dir: str
    inference_model_dir: str
    classifier_dir: str
