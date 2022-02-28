import copy
import json
from pathlib import Path


def generate(file):
    return Path(file).stem


class Playlist(object):
    def __init__(self):
        self.roms = []

    def __iadd__(self, other):
        if type(other) in [tuple, list]:
            self.roms.append([other[0], other[1]])
        else:
            assert isinstance(other, str)
            self.roms.append(other)
        return self

    def create_json(self, filename=None):
        json_file = {
            "version": "1.0",
            "items": []
        }
        item_json = {
            "path": None,
            "label": None,
            "core_path": "DETECT",
            "core_name": "DETECT",
            "crc32": "DETECT",
            "db_name": None
        }
        for i in self.roms:
            item = copy.copy(item_json)
            item["db_name"] = filename
            if type(i) == str:
                item["path"] = i
                item["label"] = generate(i)
            else:
                item["label"] = i[0]
                item["path"] = i[1]
            json_file["items"].append(item)
        if filename:
            with open(filename, "w") as d:
                json.dump(json_file, d)
        else:
            print(json_file)
