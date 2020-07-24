import pandas as pd
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

import files
import hyperparam
import predictor
from transformers import *

data_path = 'data/'

class_undefined = 'undefined'

if __name__ == "__main__":

    messages_with_clusters = files.load_messages_with_clusters()
    messages_with_clusters.dropna(inplace=True)

    cluster_to_class = files.load_clusters_to_classes()

    messages_with_clusters['class'] = messages_with_clusters['cluster'].apply(
        lambda cl_i: cluster_to_class[cl_i] if cl_i in cluster_to_class else predictor.class_undefined)
    messages_with_clusters.drop(columns=['cluster'], inplace=True)

    class_ohe = pd.get_dummies(messages_with_clusters['class'], prefix='class')
    class_ohe.drop(columns=['class_undefined'], inplace=True)  # drop_first but drop_undefined

    steps = [
        ('clean_text', CleanTextTransformer()),
        ('tfidf', TfidfVectorizer()),
        ('dense', DenseTransformer()),
    ]
    if hyperparam.pca_n_components is not None:
        steps.append(('pca', PCA(n_components=hyperparam.pca_n_components)))
    steps.append(('estimator', hyperparam.estimator))

    pipeline = Pipeline(steps)
    pipeline.fit(messages_with_clusters['message'], class_ohe)

    files.save_pipeline(pipeline)
    files.save_classes(class_ohe.columns.values)
