import pandas as pd
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

import files
import hyperparam
import predictor
from transformers import *
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, f1_score, precision_score, recall_score

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

    scoring = {
        'f1_micro': make_scorer(f1_score, average='micro'),
        'f1_macro': make_scorer(f1_score, average='macro'),

        'pres_micro': make_scorer(precision_score, average='micro'),
        'pres_macro': make_scorer(precision_score, average='macro'),

        'rec_micro': make_scorer(recall_score, average='micro'),
        'rec_macro': make_scorer(recall_score, average='macro'),
    }
    scores = cross_validate(pipeline,
                            messages_with_clusters['message'],
                            class_ohe,
                            scoring=scoring,
                            cv=5)
    for score_key in scoring.keys():
        print(f'{score_key} score: '
              f'{scores[f"test_{score_key}"].mean():.3f} '
              f'+-({scores[f"test_{score_key}"].std():.3f})')

    pipeline.fit(messages_with_clusters['message'], class_ohe)

    files.save_pipeline(pipeline)
    files.save_classes(class_ohe.columns.values)
