import argparse
import os

from scripts.datasource import JsonClusterExplorerDataSource
from scripts.social import SocialFactoryImpl

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='create clusters on messages from social network')
    parser.add_argument('-p', '--peers_count', required=True, type=int, help='how many recent dialogs to fetch')
    parser.add_argument('-s', '--social', required=True,
                        help=f'which social network to use; supported values = {SocialFactoryImpl.supported_values}')
    parser.add_argument('-f', '--filter_py',
                        help='python file with defined `def filter_func(message: Message) -> bool` to filter messages')
    args = parser.parse_args()

    messages_csv = "/tmp/messages.csv"
    os.system(f"python3 scripts/fetcher.py -p {args.peers_count} -s {args.social} -o {messages_csv}")

    if args.filter_py:
        os.system(f"python3 scripts/message_filterer.py -m {messages_csv} -f {args.filter_py}")

    cluster_exploration_json = "/tmp/clusters.json"
    random_state = 289
    os.system(f"python3 scripts/cluster_explorer.py -i {messages_csv} -o {cluster_exploration_json} -r {random_state}")

    cluster_explorer_data_source = JsonClusterExplorerDataSource(cluster_exploration_json)
    exploration_results = cluster_explorer_data_source.get_results()

    best_metrics = 0.0
    best_clusters_count = 2
    for cl_cnt, m in exploration_results.get_results().items():
        if m.silhouette > best_metrics:
            best_metrics = m.silhouette
            best_clusters_count = cl_cnt
    print(f'best clusters count = {best_clusters_count}')

    messages_with_clusters_csv = "/tmp/messages_with_clusters.csv"
    clusters_explanation_json = "/tmp/clusters_explanation.json"
    os.system(f"python3 scripts/cluster_maker.py -i {messages_csv} -om {messages_with_clusters_csv} "
              f"-oe {clusters_explanation_json} -r {random_state} -c {best_clusters_count}")
