import json
from abc import ABC

from Dataset.DataSetInterface import DataSetInterface


class DataSet(DataSetInterface, ABC):
    def __init__(self, file_path):
        self.file_path = file_path

    def read_all_repositories(self):
        items_list = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

        except FileNotFoundError:
            raise FileNotFoundError("you inserted a non-existent file in the DataSet object")

        for item in data['items']:
            items_list.append(item)

        # Ritorno la lista contenente gli items
        return items_list

    def filter_repositories(self, filter_strategy):
        repositories = self.read_all_repositories()
        return filter_strategy.filtering(repositories)

