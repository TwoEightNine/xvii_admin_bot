import argparse
import collections

from sklearn.cluster import SpectralClustering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

import hyperparam
import files
from transformers import *


def get_cluster_preview(model, messages_list, cluster_num):
    cluster_messages = []
    preview = ""
    for i in range(len(messages_list)):
        if model.labels_[i] == cluster_num:
            cluster_messages += messages_list[i].split(' ')
    count = collections.Counter(cluster_messages)

    total = len(cluster_messages)
    preview += f'\ncluster {cluster_num}: words size = {total}\n'
    for word, cnt in count.items():
        if cnt > total * 0.05:
            preview += f'{word} {cnt / total * 100:.2f}%\t\t'
    preview += '\n'
    return preview


def investigate_clusters(tfidf_vectors, random_state: int):
    print('investigating the best quantity of clusters..')
    tfidf_dense = tfidf_vectors.todense()
    sil_scores = []
    cluster_counts = []
    max_sil_score = 0
    clusters = 2
    while len(sil_scores) == 0 or sil_scores[-1] > 0.8 * max_sil_score:
        print(f'{clusters} clusters', end='')
        model = SpectralClustering(
            n_clusters=clusters,
            random_state=random_state,
            n_jobs=-1
        ).fit(tfidf_vectors)
        labels = model.labels_
        score = silhouette_score(tfidf_dense, labels)
        print(f': silhouette score = {score:.3f}')
        if score > max_sil_score:
            max_sil_score = score
        cluster_counts.append(clusters)
        sil_scores.append(score)
        clusters += max(2, int(round(clusters * 0.1)))

    print('search is done!')


def perform_clustering(tfidf_vectors, clusters_count: int, random_state: int):
    print('performing clustering')
    tfidf_dense = tfidf_vectors.todense()
    sc_model = SpectralClustering(
        n_clusters=clusters_count,
        random_state=random_state,
        n_jobs=-1
    ).fit(tfidf_vectors)

    print('scores:')
    print(f'silhouette: {silhouette_score(tfidf_dense, sc_model.labels_):.3f}')
    print(f'davies-bouldin: {davies_bouldin_score(tfidf_dense, sc_model.labels_):.3f}')
    print(f'calinski-harabasz: {calinski_harabasz_score(tfidf_dense, sc_model.labels_):.3f}')

    return sc_model


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='find clustering parameters and perform clustering')
    parser.add_argument('--search', action='store_true', help='perform search for best quantity of clusters')
    parser.add_argument('--clusters_count', type=int, help='how many clusters to use, required if not search')
    parser.add_argument('--random_state', required=True, type=int, help='random state for better reproducibility')
    args = parser.parse_args()

    if not args.search and args.clusters_count is None:
        parser.error('--clusters_count is required if --search not set')

    # process messages and explore clusters
    messages = files.load_messages()
    clean_messages = CleanTextTransformer().fit_transform(messages)
    tfidf_vectors = TfidfVectorizer().fit_transform(clean_messages)
    tfidf_dense = tfidf_vectors.todense()

    if args.search:
        investigate_clusters(tfidf_vectors, args.random_state)
    else:
        cluster_model = perform_clustering(tfidf_vectors, args.clusters_count, args.random_state)

        # save messages with cluster
        files.save_messages_with_clusters(messages, cluster_model.labels_)

        # save clustering results
        explanation = ""
        for cl_i in range(hyperparam.clusters_count):
            explanation += get_cluster_preview(cluster_model, clean_messages, cl_i)
        files.save_model_explanation(explanation)
