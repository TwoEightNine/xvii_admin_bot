import argparse

from usecase import makeclusters
from scripts.datasource import CsvMessageDataSource, CsvClusteredMessageDataSource, JsonClustersExplanationDataSource


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='find clustering parameters and perform clustering')
    parser.add_argument('-i', '--input_csv', required=True, help='where to get messages from; .csv')
    parser.add_argument('-om', '--output_messages_csv', required=True,
                        help='where to save messages with clusters to; .csv')
    parser.add_argument('-oe', '--output_explanation_json', required=True,
                        help='where to save clusters explanation to; .json')
    parser.add_argument('-c', '--clusters_count', required=True, type=int,
                        help='how many clusters to use, required if not search')
    parser.add_argument('-r', '--random_state', required=True, type=int, help='random state for better reproducibility')
    args = parser.parse_args()

    if args.input_csv[-4:] != '.csv':
        print(f'--input_csv should have .csv extension')
        exit(0)

    if args.output_messages_csv[-4:] != '.csv':
        print(f'--output_messages_csv should have .csv extension')
        exit(0)

    if args.output_explanation_json[-5:] != '.json':
        print(f'--output_explanation_json should have .json extension')
        exit(0)

    message_data_source = CsvMessageDataSource(args.input_csv)
    clustered_message_data_source = CsvClusteredMessageDataSource(args.output_messages_csv)
    clusters_explanation_data_source = JsonClustersExplanationDataSource(args.output_explanation_json)

    args = makeclusters.MakerArgs(args.clusters_count, args.random_state)
    maker = makeclusters.MakeUseCase(
        message_data_source,
        clustered_message_data_source,
        clusters_explanation_data_source,
        args
    )
    maker.make_clusters()
