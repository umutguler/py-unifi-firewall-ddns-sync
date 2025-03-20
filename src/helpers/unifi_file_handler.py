"""
Handles the file operations for the Unifi API.
"""
import os
import json


class FileHandler:
    def __init__(self, file):
        if os.path.isfile(file):
            self._file = file

    def read_json(self):
        with open(self._file, 'r', encoding="utf-8") as file:
            return json.load(file)
