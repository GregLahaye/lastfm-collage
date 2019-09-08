import json


def get_key():
    with open("secrets.json", "r") as f:
        content = json.load(f)

    key = content["key"]

    return key

