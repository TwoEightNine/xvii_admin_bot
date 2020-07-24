import pickle

import pandas as pd
import json
from sklearn.pipeline import Pipeline

data_path = 'data/'
messages_file_name = data_path + 'messages.csv'
messages_with_clusters_file_name = data_path + 'messages_with_clusters.csv'
class_to_cluster_file_name = 'class_to_cluster.json'
model_explanation_file_name = data_path + 'model_explanation.txt'
model_pipeline_file_name = data_path + 'model_pipeline.pkl'
model_classes_file_name = data_path + 'model_classes.pkl'

key_message = 'message'
key_cluster = 'cluster'


def save_messages(messages: list) -> pd.DataFrame:
    df = pd.DataFrame()
    df[key_message] = messages
    df.to_csv(messages_file_name, index=False)
    return df


def load_messages() -> pd.Series:
    messages = pd.read_csv(messages_file_name)
    return messages[key_message]


def save_messages_with_clusters(messages, clusters) -> pd.DataFrame:
    df = pd.DataFrame()
    df[key_message] = messages
    df[key_cluster] = clusters
    df.to_csv(messages_with_clusters_file_name, index=False)
    return df


def load_messages_with_clusters() -> pd.DataFrame:
    return pd.read_csv(messages_with_clusters_file_name)


def save_model_explanation(explanation: str):
    with open(model_explanation_file_name, 'w') as f:
        f.write(explanation)


def load_clusters_to_classes() -> dict:
    with open(class_to_cluster_file_name, 'r') as f:
        class_to_clusters = json.load(f)

    cluster_to_class = {}
    for klass, cl_list in class_to_clusters.items():
        for cl in cl_list:
            cluster_to_class[cl] = klass
    return cluster_to_class


def save_pipeline(pipeline: Pipeline):
    with open(model_pipeline_file_name, 'wb') as f:
        pickle.dump(pipeline, f)


def load_pipeline() -> Pipeline:
    with open(model_pipeline_file_name, 'rb') as f:
        return pickle.load(f)


def save_classes(classes):
    with open(model_classes_file_name, 'wb') as f:
        pickle.dump(classes, f)


def load_classes():
    with open(model_classes_file_name, 'rb') as f:
        return pickle.load(f)
