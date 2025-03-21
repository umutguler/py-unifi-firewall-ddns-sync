"""
Handles the file operations for the Unifi API.
"""
import json
import os

import py_logging

logging = py_logging.get_logger(__name__)


class FileHandler:
    """Handles file operations for the Unifi API."""

    def __init__(self, file):
        if os.path.isfile(file):
            logging.info("Found file: %s", file)
            self._file = file

    def read_json(self):
        """Reads the JSON file and returns the data."""
        with open(self._file, 'r', encoding="utf-8") as file:
            return json.load(file)
