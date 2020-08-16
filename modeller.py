import argparse

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import make_scorer, f1_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_validate
from sklearn.pipeline import Pipeline

import files
import hyperparam
import predictor
from transformers import *

class_undefined = 'undefined'

column_algorithm = 'algorithm'

default_cv = 5
default_sort_by = 'f1_macro'


def create_data():
    messages_with_clusters = files.load_messages_with_clusters()
    messages_with_clusters.dropna(inplace=True)

    cluster_to_class = files.load_clusters_to_classes()

    messages_with_clusters['class'] = messages_with_clusters['cluster'].apply(
        lambda cl_i: cluster_to_class[cl_i] if cl_i in cluster_to_class else predictor.class_undefined)
    messages_with_clusters.drop(columns=['cluster'], inplace=True)

    class_ohe = pd.get_dummies(messages_with_clusters['class'], prefix='class')
    class_ohe.drop(columns=['class_undefined'], inplace=True)  # drop_first but drop_undefined

    return messages_with_clusters['message'], class_ohe


def create_pipeline(args, estimator):
    steps = [
        ('clean_text', CleanTextTransformer()),
        ('tfidf', TfidfVectorizer()),
        ('dense', DenseTransformer()),
    ]
    if args.pca_n_components:
        steps.append(('pca', PCA(n_components=args.pca_n_components)))
    steps.append(('estimator', estimator))

    return Pipeline(steps)


def create_scorers():
    return {
        'f1_micro': make_scorer(f1_score, average='micro', zero_division=0),
        'f1_macro': make_scorer(f1_score, average='macro', zero_division=0),

        'pres_micro': make_scorer(precision_score, average='micro', zero_division=0),
        'pres_macro': make_scorer(precision_score, average='macro', zero_division=0),

        'rec_micro': make_scorer(recall_score, average='micro', zero_division=0),
        'rec_macro': make_scorer(recall_score, average='macro', zero_division=0),
    }


def perform_search(estimator, params, x, y, verbose=0) -> pd.DataFrame:
    search = GridSearchCV(estimator, params, cv=cv, scoring=scoring, refit=False, verbose=verbose, n_jobs=-1)
    search.fit(x, y)
    results = pd.DataFrame()
    for k, v in search.cv_results_.items():
        results[k] = v
    return results


def get_valuable_results(results_df: pd.DataFrame, algo_name: str) -> pd.DataFrame:
    results_df[column_algorithm] = [algo_name] * results_df.shape[0]
    info_columns = [col for col in results_df.columns if 'split' not in col and
                    'rank_' not in col and
                    'param_' not in col]
    results_df = results_df[info_columns]
    return results_df


def prettify_results(results, scoring) -> pd.DataFrame:
    to_compose = [f'test_{key}' for key in scoring.keys()] + ['fit_time', 'score_time']
    for value in to_compose:
        mean_col = f'mean_{value}'
        std_col = f'std_{value}'
        results[mean_col] = results[mean_col].apply(lambda f: f'{f:.2f}')
        results[std_col] = results[std_col].apply(lambda f: f'{f:.2f}')
        results[value] = results[[mean_col, std_col]].apply(lambda x: f'{x[0]} +-({x[1]})', axis=1)
        results.drop(columns=[mean_col, std_col], inplace=True)
    return results


def merge_results(list_of_results) -> pd.DataFrame:
    return pd.concat(list_of_results, axis=0, ignore_index=True)


def print_scores(scores, scoring):
    for score_key in scoring.keys():
        print(f'{score_key} score: '
              f'{scores[f"test_{score_key}"].mean():.3f} '
              f'+-({scores[f"test_{score_key}"].std():.3f})')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='build a model that classifies text according to found clusters')
    parser.add_argument('--search', action='store_true', help='perform search for best quantity of clusters')
    parser.add_argument('--pca_n_components', type=float, help='argument for PCA(n_components); default no PCA')
    parser.add_argument('--cv', type=int, help=f'number of folds in cross validation; default {default_sort_by}')
    parser.add_argument('--sort_by', help=f'which metrics to use in sorting; default {default_sort_by}')
    args = parser.parse_args()

    x_train, y_train = create_data()
    scoring = create_scorers()
    cv = args.cv if args.cv else default_cv
    sort_by = args.sort_by if args.sort_by else default_sort_by

    if args.search:
        clean_messages = CleanTextTransformer().fit_transform(x_train)
        tfidf_vectors = TfidfVectorizer().fit_transform(clean_messages)
        if args.pca_n_components:
            train_data = PCA(n_components=args.pca_n_components).fit_transform(tfidf_vectors.todense())
        else:
            train_data = tfidf_vectors

        results_over_all = []
        for estimator, params in hyperparam.search_estimators:
            print(str(estimator))
            search_results = perform_search(estimator, params, train_data, y_train)
            results = get_valuable_results(search_results, str(estimator))
            results_over_all.append(results)

        results = merge_results(results_over_all)
        sort_by_columns = [col for col in results.columns if 'mean' in col and sort_by in col]
        if sort_by_columns:
            results = results.sort_values(by=sort_by_columns, ascending=False)
        results = prettify_results(results, scoring)
        files.save_search_results(results)

        print('5 best results:')
        sort_by_columns = [col for col in results.columns if sort_by in col]
        print(results[['params', column_algorithm] + sort_by_columns].head(5))
    else:
        pipeline = create_pipeline(args, hyperparam.estimator)
        scores = cross_validate(pipeline, x_train, y_train, scoring=scoring, cv=cv)
        print_scores(scores, scoring)

        pipeline.fit(x_train, y_train)
        files.save_pipeline(pipeline)
        files.save_classes(y_train.columns.values)
