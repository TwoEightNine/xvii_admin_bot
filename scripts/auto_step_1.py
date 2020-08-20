import argparse
import os
import json

from scripts.social import SocialFactoryImpl

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='create clusters on messages from social network')
    parser.add_argument('-p', '--peers_count', required=True, type=int, help='how many recent dialogs to fetch')
    parser.add_argument('-s', '--social', required=True,
                        help=f'which social network to use; supported values = {SocialFactoryImpl.supported_values}')
    args = parser.parse_args()

    messages_csv = "/tmp/messages.csv"
    os.system(f"python3 scripts/fetcher.py -p {args.peers_count} -s {args.social} -o {messages_csv}")

    cluster_exploration_json = "/tmp/clusters.json"
    random_state = 289
    os.system(f"python3 scripts/cluster_explorer.py -i {messages_csv} -o {cluster_exploration_json} -r {random_state}")

    metrics = "silhouette_score"
    with open(cluster_exploration_json, 'r') as fp:
        exploration_data = json.load(fp)['results']
        best_clusters_count = 2
        best_metrics = 0.0
        for cl_cnt, m in exploration_data.items():
            if m[metrics] > best_metrics:
                best_metrics = m[metrics]
                best_clusters_count = cl_cnt
    print(f'best clusters count ({metrics}) = {best_clusters_count}')
    messages_with_clusters_csv = "/tmp/messages_with_clusters.csv"
    clusters_explanation_json = "/tmp/clusters_explanation.json"
    os.system(f"python3 scripts/cluster_maker.py -i {messages_csv} -om {messages_with_clusters_csv} "
              f"-oe {clusters_explanation_json} -r {random_state} -c {best_clusters_count}")
