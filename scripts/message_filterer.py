import argparse
import importlib.util
import os.path

from scripts.datasource import CsvMessageDataSource
from scripts.utils import StdoutLogger
from usecase import filtermessages


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='filter fetched messages')
    parser.add_argument('-m', '--messages_csv', required=True, help='file with fetched messages; .csv')
    parser.add_argument('-f', '--filter_py', required=True,
                        help='python file with defined `def filter_func(message: Message) -> bool` to filter messages')
    args = parser.parse_args()

    if args.messages_csv[-4:] != '.csv':
        print(f'--messages_csv should have .csv extension')
        exit(0)

    if args.filter_py[-3:] != '.py':
        print(f'--filter_py should have .py extension and be a valid python file')
        exit(0)

    filter_func = None
    try:
        module_name = os.path.basename(args.filter_py)[:-3]
        filter_file = module_from_file(module_name, args.filter_py)
        filter_func = filter_file.filter_func
    except Exception as e:
        print(e)
        print(f'unable to find filter_func in {args.filter_py}. is it really there?')
        exit(0)

    logger = StdoutLogger()
    message_data_source = CsvMessageDataSource(args.messages_csv)

    filter_args = filtermessages.FilterArgs(filter_func)
    use_case = filtermessages.FilterUseCase(message_data_source, logger, filter_args)
    use_case.filter_messages()
