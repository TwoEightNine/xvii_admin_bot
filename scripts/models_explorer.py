import argparse

import hyperparam
from usecase import exploremodels
from scripts.datasource import CsvClusteredMessageDataSource, JsonMessageClassesDataSource, JsonModelsExplorerDataSource
from scripts.utils import StdoutLogger

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='find better classifier')
    parser.add_argument('-m', '--messages_csv', required=True, help='where to take messages with clusters from; .csv')
    parser.add_argument('-c', '--classes_json', required=True, help='where to take message classes from; .json')
    parser.add_argument('-e', '--exploration_json', required=True, help='where to save exploration results; .json')
    args = parser.parse_args()

    clustered_messages_data_source = CsvClusteredMessageDataSource(args.messages_csv)
    message_classes_data_source = JsonMessageClassesDataSource(args.classes_json)
    models_explorer_data_source = JsonModelsExplorerDataSource(args.exploration_json)
    logger = StdoutLogger()
    args = exploremodels.ExplorerArgs(5, hyperparam.search_estimators)
    use_case = exploremodels.ModelsExplorerUseCase(
        clustered_messages_data_source,
        message_classes_data_source,
        models_explorer_data_source,
        logger, args
    )
    use_case.explore_models()
