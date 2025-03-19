import json
import os

_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class _Secrets:
    def __init__(self):
        try:
            with open(os.path.join(_ROOT_DIR, "secrets.json"), "r") as f:
                self.__config = json.load(f)
        except Exception as e:
            raise Exception("Could not load secrets file")
    def get(self, key):
        if key not in self.__config:
            raise Exception("Key is missing from secrets")
        return self.__config[key]

secrets = _Secrets()
