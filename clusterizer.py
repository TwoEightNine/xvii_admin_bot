import collections
import pickle
import time

import pandas as pd
from sklearn.cluster import SpectralClustering
from sklearn.feature_extraction.text import TfidfVectorizer

import utils

data_path = 'data/'
last_model_file = f'{data_path}last_model.txt'
clusters_count = 30
random_state = 289


def get_cluster_preview(model, messages_df, cluster_num):
    cluster_messages = []
    preview = ""
    for i in range(len(messages_df['message'])):
        if model.labels_[i] == cluster_num:
            cluster_messages += messages_df['message'][i].split(' ')
    count = collections.Counter(cluster_messages)

    total = len(cluster_messages)
    preview += f'\ncluster {cluster_num}: words size = {total}\n'
    for word, cnt in count.items():
        if cnt > total * 0.1:
            preview += f'{word} {cnt / total * 100:.2f}%\t\t'
    preview += '\n'
    return preview


if __name__ == "__main__":

    # process messages
    messages = pd.read_csv(data_path + 'messages.csv')
    messages['message'] = [utils.clean_text(m) for m in messages['message']]

    # create tf-idf vectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(list(messages['message']))

    # dump it
    now = time.ctime(time.time()).replace(' ', '_').lower()
    model_name = f'{data_path}model_tfidf_{now}.pkl'
    with open(model_name, 'wb') as f:
        pickle.dump(vectorizer, f)
    print(f'tfidf vectorizer is saved to {model_name}')

    # perform clustering
    sc_model = SpectralClustering(n_clusters=clusters_count, random_state=random_state)
    sc_model.fit(X)

    # save clustering results
    model_explanation_name = f'{data_path}model_exp_{now}.txt'
    with open(model_explanation_name, 'w') as f:
        for cl_i in range(clusters_count):
            f.write(get_cluster_preview(sc_model, messages, cl_i))
    print(f'model explanation is saved to {model_explanation_name}')

    # update last_model to easy use recent models
    with open(last_model_file, 'w') as f:
        f.write(f'{model_name}\n{model_explanation_name}')

