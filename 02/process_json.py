import json
from typing import Callable, List


def process_json(json_str: str,
                 required_keys: List[str] | None = None,
                 tokens: List[str] | None = None,
                 callback: Callable[[str, str], str] | None = None) -> None:
    """
    :param json_str: json string
    :param required_keys: list of keys to be processed
    :param tokens: a list of tokens to find
    :param callback: key and token handler function
    :return:
    """
    json_obj = json.loads(json_str)

    for key, value in json_obj.items():
        if key not in required_keys:
            continue

        for token in tokens:
            if token.lower() in value.lower():
                print(callback(key, token))
