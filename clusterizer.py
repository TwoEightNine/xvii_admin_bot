import collections
import pickle
import time

import pandas as pd
from sklearn.cluster import SpectralClustering
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import *

import utils

data_path = 'data/'
last_model_file = f'{data_path}last_model.txt'
clusters_count = 30
random_state = 289


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
        if cnt > total * 0.1:
            preview += f'{word} {cnt / total * 100:.2f}%\t\t'
    preview += '\n'
    return preview


if __name__ == "__main__":
    # process messages and explore clusters
    messages = pd.read_csv(data_path + 'messages.csv')
    clean_messages = CleanTextTransformer().fit_transform(messages['message'])
    tfidf_vectors = TfidfVectorizer().fit_transform(clean_messages)
    sc_model = SpectralClustering(
        n_clusters=clusters_count,
        random_state=random_state
    ).fit(tfidf_vectors)

    # save messages with cluster
    messages['cluster'] = sc_model.labels_
    messages.to_csv(f'{data_path}messages_with_cluster.csv', index=False)

    # save clustering results
    model_explanation_name = f'{data_path}model_explanation.txt'
    with open(model_explanation_name, 'w') as f:
        for cl_i in range(clusters_count):
            f.write(get_cluster_preview(sc_model, clean_messages, cl_i))
    print(f'model explanation is saved to {model_explanation_name}')

