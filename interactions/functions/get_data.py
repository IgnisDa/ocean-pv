import random
from os import path
import json


def get_file_loc():
    return path.dirname(path.dirname(path.abspath(__file__)))


def get_data_fn():
    file_dir = get_file_loc()
    with open(path.join(file_dir, 'static', 'data', 'json_data.json')) as f:
        j = json.load(f)
        for index, dictionary in enumerate(j, 1):
            dictionary.update({'index': index})
        random.shuffle(j)
        return j
