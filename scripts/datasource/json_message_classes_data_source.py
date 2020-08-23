import json
from typing import List

from core.model import MessageClass
from usecase.datasource import MessageClassesDataSource


class JsonMessageClassesDataSource(MessageClassesDataSource):

    def __init__(self, file_name: str):
        self.file_name = file_name

    def get_classes(self) -> List[MessageClass]:
        with open(self.file_name, 'r') as fp:
            data = json.load(fp)
            message_classes = []
            for name, info in data.items():
                message_classes.append(MessageClass(
                    name=name,
                    cluster_indexes=info['clusters'],
                    response=info['response']
                ))
            return message_classes
