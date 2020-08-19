import pandas as pd

from usecase.datasource import ClusteredMessageDataSource


class CsvClusteredMessageDataSource(ClusteredMessageDataSource):
    column_message = 'message'
    column_cluster_index = 'cluster_index'

    def __init__(self, file_name: str):
        self.file_name = file_name

    def get_messages(self) -> tuple:
        try:
            messages = pd.read_csv(self.file_name)
            return list(messages[self.column_message]), list(messages[self.column_cluster_index])
        except Exception as e:
            return [], []

    def set_messages(self, messages: list, cluster_labels: list):
        df = pd.DataFrame()
        df[self.column_message] = messages
        df[self.column_cluster_index] = cluster_labels
        df.to_csv(self.file_name, index=False)
