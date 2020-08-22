from usecase.datasource import MessageDataSource
from usecase.logger import Logger
from .models import FilterArgs

from core import filtermessages


class FilterUseCase:

    def __init__(self, message_data_source: MessageDataSource, logger: Logger, args: FilterArgs):
        self.message_data_source = message_data_source
        self.args = args
        self.logger = logger

        params = filtermessages.FilterParams(args.filter_func)
        self.filterer = filtermessages.MessageFilterer(params)

    def filter_messages(self):
        messages = self.message_data_source.get_messages()
        print(len(messages))
        self.filterer.filter(messages)
        filtered_messages = self.filterer.results.messages
        print(len(filtered_messages))
        self.message_data_source.set_messages(filtered_messages)
        remained_count = len(filtered_messages)
        removed_count = len(messages) - remained_count
        self.logger.log(f'filtering completed successfully! '
                        f'removed {removed_count} messages, {remained_count} remained')
