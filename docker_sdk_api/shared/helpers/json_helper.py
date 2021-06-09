import json
from json import JSONDecodeError
from typing import Dict


def parse_json(file_path: str) -> Dict:
    try:
        with open(file_path, "rb") as json_file:
            return json.load(json_file)
    except JSONDecodeError as e:
        # if json is empty return empty dict
        return {}


# todo check if needed
def write_json(file_path: str, content: object) -> None:
    with open(file_path, "w") as json_file:
        json_file.write(json.dumps(content))


def jsonify_string(content: str) -> object:
    return json.loads(content)
