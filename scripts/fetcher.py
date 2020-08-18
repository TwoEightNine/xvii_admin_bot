import argparse

from usecase import fetch
from scripts.utils import StdoutLogger
from scripts.social import SocialFactoryImpl
from scripts.datasource import CsvMessageDataSource

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='fetch messages from target social network')
    parser.add_argument('-o', '--output_csv', required=True, help='where to save fetched messages; .csv')
    parser.add_argument('-p', '--peers_count', required=True, type=int, help='how many recent dialogs to fetch')
    parser.add_argument('-s', '--social', required=True,
                        help=f'which social network to use; supported values = {SocialFactoryImpl.supported_values}')
    args = parser.parse_args()

    if args.social not in SocialFactoryImpl.supported_values:
        print(f'undefined social parameter passed: {args.social}')
        exit(0)

    if args.output_csv[-4:] != '.csv':
        print(f'output_csv should have .csv extension')
        exit(0)

    logger = StdoutLogger()
    social_factory = SocialFactoryImpl()
    message_data_source = CsvMessageDataSource(args.output_csv)

    fetch_args = fetch.FetchArgs(args.social, args.peers_count)
    use_case = fetch.FetchUseCase(social_factory, message_data_source, fetch_args, logger)
    use_case.fetch_messages()
