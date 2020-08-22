from usecase.datasource import MessageDataSource
from core.model import Message
import pandas as pd
from typing import List


class CsvMessageDataSource(MessageDataSource):
    column_message_id = 'message_id'
    column_peer_id = 'peer_id'
    column_text = 'text'
    column_time_stamp = 'time_stamp'

    def __init__(self, file_name: str):
        self.file_name = file_name

    def get_messages(self) -> List[Message]:
        try:
            messages = pd.read_csv(self.file_name)
            messages = [
                Message(
                    item[self.column_message_id],
                    item[self.column_peer_id],
                    item[self.column_text],
                    item[self.column_time_stamp]
                )
                for item in messages.iloc
            ]
            for message in messages:
                if message.text != message.text:
                    message.text = ""
            return messages
        except Exception as e:
            return []

    def set_messages(self, messages: List[Message]):
        message_lists = [[message.id, message.peer_id, message.text, message.time_stamp] for message in messages]
        df = pd.DataFrame(
            message_lists,
            columns=[self.column_message_id, self.column_peer_id, self.column_text, self.column_time_stamp]
        )
        df.to_csv(self.file_name, index=False)
