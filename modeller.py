import json
import pickle

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline

import dumper
import predictor
from transformers import *

data_path = 'data/'

class_undefined = 'undefined'

if __name__ == "__main__":

    messages_with_clusters = dumper.load_messages_with_clusters()
    messages_with_clusters.dropna(inplace=True)

    cluster_to_class = dumper.load_clusters_to_classes()

    messages_with_clusters['class'] = messages_with_clusters['cluster'].apply(
        lambda cl_i: cluster_to_class[cl_i] if cl_i in cluster_to_class else predictor.class_undefined)
    messages_with_clusters.drop(columns=['cluster'], inplace=True)

    class_ohe = pd.get_dummies(messages_with_clusters['class'], prefix='class')
    class_ohe.drop(columns=['class_undefined'], inplace=True)  # drop_first but drop_undefined

    pipeline = Pipeline([
        ('clean_text', CleanTextTransformer()),
        ('tfidf', TfidfVectorizer()),
        ('dense', DenseTransformer()),
        ('pca', PCA(n_components=0.99)),
        ('knn', KNeighborsClassifier(n_neighbors=3, weights='distance', n_jobs=-1))
    ])
    pipeline.fit(messages_with_clusters['message'], class_ohe)

    dumper.save_pipeline(pipeline)
    dumper.save_classes(class_ohe.columns.values)
