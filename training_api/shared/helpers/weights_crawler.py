import os
import json
from typing import Dict
from model_store import get_model_file


def get_networks(config_dict: Dict[str, bool]):
    if config_dict['select_all']:
        print("Downloading All Weights")
        config_dict.pop('select_all')
        download_networks(config_dict=config_dict, check_network=False)
    else:
        config_dict.pop('select_all')
        download_networks(config_dict=config_dict, check_network=True)


def download_networks(config_dict: Dict[str, bool], check_network: bool):
    for key, value in config_dict.items():
        if check_network:
            if value:
                print("Downloading:" + str(key))
                get_model_file(str(key), root=os.path.join('~', '.mxnet', 'models'))
                continue
        else:
            print("Downloading:" + str(key))

            get_model_file(str(key), root=os.path.join('~', '.mxnet', 'models'))


if __name__ == '__main__':
    with open('assets/networks.json', 'rb') as f:
        config = json.load(f)
    get_networks(config_dict=config)
