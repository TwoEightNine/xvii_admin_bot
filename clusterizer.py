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


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='find clustering parameters and perform clustering')
    parser.add_argument('--search', action='store_true', help='perform search for best quantity of clusters')
    args = parser.parse_args()

    # process messages and explore clusters
    messages = files.load_messages()
    clean_messages = CleanTextTransformer().fit_transform(messages)
    tfidf_vectors = TfidfVectorizer().fit_transform(clean_messages)
    tfidf_dense = tfidf_vectors.todense()

    if args.search:
        print('investigating the best quantity of clusters..')
        sil_scores = []
        cluster_counts = []
        max_sil_score = 0
        clusters = 2
        while len(sil_scores) == 0 or sil_scores[-1] > 0.8 * max_sil_score:
            print(f'{clusters} clusters', end='')
            model = SpectralClustering(
                n_clusters=clusters,
                random_state=hyperparam.random_state,
                n_jobs=-1
            ).fit(tfidf_vectors)
            labels = model.labels_
            score = silhouette_score(tfidf_dense, labels)
            print(f': {score:.3f}')
            if score > max_sil_score:
                max_sil_score = score
            cluster_counts.append(clusters)
            sil_scores.append(score)
            clusters += max(2, int(round(clusters * 0.1)))

        print('search is done!')
    else:
        sc_model = SpectralClustering(
            n_clusters=hyperparam.clusters_count,
            random_state=hyperparam.random_state,
            n_jobs=-1
        ).fit(tfidf_vectors)

        print('scores:')
        print(f'silhouette: {silhouette_score(tfidf_dense, sc_model.labels_):.3f}')
        print(f'davies-bouldin: {davies_bouldin_score(tfidf_dense, sc_model.labels_):.3f}')
        print(f'calinski-harabasz: {calinski_harabasz_score(tfidf_dense, sc_model.labels_):.3f}')

        # save messages with cluster
        files.save_messages_with_clusters(messages, sc_model.labels_)

        # save clustering results
        explanation = ""
        for cl_i in range(hyperparam.clusters_count):
            explanation += get_cluster_preview(sc_model, clean_messages, cl_i)
        files.save_model_explanation(explanation)
