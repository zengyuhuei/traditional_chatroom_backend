import json

class Response:
    def __init__(self):
        self._data = {}

    def success(self, message ="ok", code = 200):
        self._data["code"] = 200
        self._data["status"] = "success"
        self._data["message"] = message

    def error(self, message):
        self._data["status"] = "error"
        self._data["message"] = message

    def get_data(self):
        return self._data

    def get_json(self):
        return json.dumps(self._data)