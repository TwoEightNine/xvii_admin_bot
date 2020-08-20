import argparse

from usecase import filtermessages
from scripts.utils import StdoutLogger
from scripts.datasource import CsvMessageDataSource

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='filter fetched messages')
    parser.add_argument('-m', '--messages_csv', required=True, help='file with fetched messages; .csv')
    parser.add_argument('-ip', '--ignored_peers', help='list of comma-separated peer ids to ignore messages from')
    parser.add_argument('-is', '--ignored_substrings',
                        help='list of comma-separated phrases to ignore messages that contains any of them')
    args = parser.parse_args()

    if args.messages_csv[-4:] != '.csv':
        print(f'--messages_csv should have .csv extension')
        exit(0)

    logger = StdoutLogger()
    message_data_source = CsvMessageDataSource(args.messages_csv)

    ignored_peers = []
    if args.ignored_peers:
        ignored_peers.extend([int(peer_id) for peer_id in args.ignored_peers.split(',')])

    ignored_substrings = []
    if args.ignored_substrings:
        ignored_peers.extend([phrase for phrase in args.ignored_substrings.split(',')])

    filter_args = filtermessages.FilterArgs(ignored_peers, ignored_substrings)
    use_case = filtermessages.FilterUseCase(message_data_source, logger, filter_args)
    use_case.filter_messages()
