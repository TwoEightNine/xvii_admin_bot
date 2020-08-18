import argparse

from usecase import exploreclusters
from scripts.datasource import CsvMessageDataSource, JsonClusterExplorerDataSource
from scripts.utils.stdout_logger import StdoutLogger


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='find clustering parameters and perform clustering')
    parser.add_argument('-i', '--input_csv', required=True, help='where to take messages from; .csv')
    parser.add_argument('-o', '--output_json', required=True, help='where to save exploration results; .csv')
    parser.add_argument('-r', '--random_state', required=True, type=int, help='random state for better reproducibility')
    args = parser.parse_args()

    if args.input_csv[-4:] != '.csv':
        print(f'--input_csv should have .csv extension')
        exit(0)

    if args.output_json[-5:] != '.json':
        print(f'--output_json should have .json extension')
        exit(0)

    message_data_source = CsvMessageDataSource(args.input_csv)
    cluster_explorer_data_source = JsonClusterExplorerDataSource(args.output_json)
    logger = StdoutLogger()

    explorer_args = exploreclusters.ExplorerArgs(args.random_state)
    explorer = exploreclusters.ClusterExplorerUseCase(
        message_data_source, cluster_explorer_data_source,
        explorer_args, logger
    )
    explorer.explore_clusters()
