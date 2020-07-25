import collections

from sklearn.cluster import SpectralClustering
from sklearn.feature_extraction.text import TfidfVectorizer

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
    # process messages and explore clusters
    messages = files.load_messages()
    clean_messages = CleanTextTransformer().fit_transform(messages)
    tfidf_vectors = TfidfVectorizer().fit_transform(clean_messages)
    sc_model = SpectralClustering(
        n_clusters=hyperparam.clusters_count,
        random_state=hyperparam.random_state,
        n_jobs=-1
    ).fit(tfidf_vectors)

    # save messages with cluster
    files.save_messages_with_clusters(messages, sc_model.labels_)

    # save clustering results
    explanation = ""
    for cl_i in range(hyperparam.clusters_count):
        explanation += get_cluster_preview(sc_model, clean_messages, cl_i)
    files.save_model_explanation(explanation)
