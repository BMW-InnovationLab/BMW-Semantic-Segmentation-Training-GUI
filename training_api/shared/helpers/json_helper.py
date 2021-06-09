import json
from typing import Dict


def parse_json(file_path: str) -> Dict:
    with open(file_path, "rb") as json_file:
        return json.load(json_file)


def write_json_dict(file_path: str, json_dict: Dict) -> None:
    with open(file_path, 'w') as json_writer:
        json.dump(json_dict, json_writer, indent=4)


def jsonify_string(content: str) -> object:
    return json.loads(content)
