# BMW Semantic Segmentation GPU/CPU Inference API
This is a repository for a Semantic Segmentation inference API using the [Gluoncv CV toolkit](https://cv.gluon.ai/contents.html).

This repository can be deployed using  **docker**.

![api](./docs/api.gif)


## Prerequisites

- Ubuntu 18.04 or 20.04 LTS
- Windows 10 pro with **hyper-v** enabled and **docker** desktop 
- NVIDIA Drivers (410.x or higher) 
- Docker CE latest stable release
- NVIDIA Docker 2

*Note: the **windows** deployment supports only CPU version thus **nvidia driver** and **nvidia docker** are not required*

### Check for prerequisites

To check if you have docker-ce installed:

```
docker --version
```

To check if you have nvidia-docker2 installed:

```
dpkg -l | grep nvidia-docker2
```

![nvidia-docker2](./docs/nvidia-docker2.png)

**To check your nvidia drivers version, open your terminal and type the command `nvidia-smi`**

![nvidia-smi](./docs/nvidiasmi.png)

### Install prerequisites

Use the following command to install docker on Ubuntu:

```
chmod +x install_prerequisites.sh && source install_prerequisites.sh
```

Install NVIDIA Drivers (410.x or higher) and NVIDIA Docker for GPU by following the [official docs](https://github.com/nvidia/nvidia-docker/wiki/Installation-(version-2.0))



## Build The Docker Image

To build the docker environment, run the following command in the project's directory:  

- For GPU Build:  

```sh
docker build -t gluoncv_semantic_segmentation_inference_api_gpu -f ./docker/GPU/dockerfile .
```

- For CPU Build:

```
docker build -t gluoncv_semantic_segmentation_inference_api_cpu -f ./docker/CPU/dockerfile .
```



### Behind a proxy

- For GPU Build:  

```sh
docker build --build-arg http_proxy='' --build-arg https_proxy='' -t gluoncv_semantic_segmentation_inference_api_gpu -f ./docker/GPU/dockerfile .
```

- For CPU Build:

```sh
docker build --build-arg http_proxy='' --build-arg https_proxy='' -t gluoncv_semantic_segmentation_inference_api_cpu -f ./docker/CPU/dockerfile .
```



## Run the docker container

To run the inference  API go the to the API's directory and run the following:



#### Using Linux based docker:

- For GPU:

```sh
docker run --gpus '"device=<- gpu numbers seperated by commas ex:"0,1,2" ->"' -itv $(pwd)/models:/models -v $(pwd)/models_hash:/models_hash -p <port-of-your-choice>:4343 gluoncv_semantic_segmentation_inference_api_gpu
```
- For CPU:

```sh
docker run -itv $(pwd)/models:/models -v $(pwd)/models_hash:/models_hash -p <port-of-your-choice>:4343 gluoncv_semantic_segmentation_inference_api_cpu
```

- For Windows

```sh
docker run -itv ${PWD}/models:/models -v ${PWD}/models_hash:/models_hash -p <port-of-your-choice>:4343 gluoncv_semantic_segmentation_inference_api_cpu
```



## API Endpoints

To see all available endpoints, open your favorite browser and navigate to:

```
http://<machine_URL>:<Docker_host_port>/docs
```
The 'predict_batch' endpoint is not shown on swagger. The list of files input is not yet supported.

### Endpoints summary

#### /load (GET)

Loads all available models and returns every model with it's hashed value. Loaded models are stored and aren't loaded again

#### /detect (POST)

Performs inference on specified model, image, and returns json file

#### /get_labels (POST)

Returns all of the specified model labels with their hashed values

#### /models (GET)

Lists all available models

#### /models/{model_name}/load (GET)

Loads the specified model. Loaded models are stored and aren't loaded again

#### /models/{model_name}/predict (POST)

Performs inference on specified model, image, and returns json file (exactly like detect)

#### /models/{model_name}/predict_image (POST)

Performs inference on specified model, image, and returns the image with transparent segments on it.

#### /models/{model_name}/inference (POST)

Performs inference on specified model,image, and returns the segments only (image) 

![inference](./docs/inference.png)

#### /models/{model_name}/labels (GET)

Returns all of the specified model labels

#### /models/{model_name}/config (GET)

Returns the specified model's configuration

## Model structure

The folder "models" contains sub-folders of all the models to be loaded.

You can copy your model sub-folder generated after training, put it inside the "models" folder in  your inference repos and you're all set to infer. 	

The model sub-folder should contain the following : 

- model_best.params

- palette.txt 
  **If you don't have your own palette, you can generate a random one using the command below in your project's repository and copy `palette.txt` to your model directory:**

```sh
python3 generate_random_palette.py

```
- configuration.json


The configuration.json file should look like the following : 

```json
{
    "inference_engine_name" : "gluonsegmentation",
    "backbone": "resnet101",
    "batch_size": 4,
    "checkpoint_name": "bmwtest",
    "num_classes": 3,
    "classes_names": [
        "background",
        "pad",
        "circle"
    ],
    "network": "fcn",
    "type":"semantic",
    "epochs": 10,
    "lr": 0.001,
    "momentum": 0.9,
    "num_workers": 4,
    "weight_decay": 0.0001
}
```

## Acknowledgements

- Roy Anwar,Beirut, Lebanon
- Hadi Koubeissy, [inmind.ai](https://inmind.ai/), Beirut, Lebanon