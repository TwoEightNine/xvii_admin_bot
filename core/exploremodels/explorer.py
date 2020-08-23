from typing import List

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import make_scorer, f1_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV

from core.transformers import CleanTextTransformer
from .models import ExplorerParams, ExplorerResult
from .explore_progress import ExploreProgress


class ModelsExplorer:

    def __init__(self, params: ExplorerParams, progress: ExploreProgress):
        self.params = params
        self.progress = progress
        self.results = None

    def explore_models(self, messages: List[str], classes: List[str]):
        self.progress.on_exploration_started()
        messages, classes_ohe = self.__prepare_data(messages, classes)
        clean_messages = CleanTextTransformer().fit_transform(messages)
        tfidf_vectors = TfidfVectorizer().fit_transform(clean_messages)

        scoring = self.__create_scorers()
        results_over_all = []
        for estimator, params in self.params.search_estimators:
            model_name = str(estimator)
            search_results = self.__perform_search(
                estimator, params, tfidf_vectors, classes_ohe, self.params.cv, scoring)
            results = self.__get_valuable_results(search_results, model_name)
            results_over_all.append(results)
            self.progress.on_explored_model(model_name)

        results = pd.concat(results_over_all, axis=0, ignore_index=True)
        self.__prepare_results(results)
        self.progress.on_results_ready()

    @staticmethod
    def __prepare_data(messages: List[str], classes: List[str]):
        data = pd.DataFrame()
        data['message'] = messages
        data['class'] = classes

        class_ohe = pd.get_dummies(data['class'], prefix='class')
        print(class_ohe.columns)
        class_ohe.drop(columns=['class_undefined'], inplace=True)  # drop_first but drop_undefined

        return data['message'], class_ohe

    @staticmethod
    def __perform_search(estimator, params, x, y, cv: int, scoring, verbose: int = 0) -> pd.DataFrame:
        search = GridSearchCV(estimator, params, cv=cv, scoring=scoring, refit=False, verbose=verbose, n_jobs=-1)
        search.fit(x, y)
        results = pd.DataFrame()
        for k, v in search.cv_results_.items():
            results[k] = v
        return results

    @staticmethod
    def __get_valuable_results(results_df: pd.DataFrame, algo_name: str) -> pd.DataFrame:
        results_df['algorithm'] = [algo_name] * results_df.shape[0]
        info_columns = [col for col in results_df.columns if 'split' not in col and
                        'rank_' not in col and
                        'param_' not in col]
        results_df = results_df[info_columns]
        return results_df

    @staticmethod
    def __create_scorers():
        return {
            'f1_micro': make_scorer(f1_score, average='micro', zero_division=0),
            'f1_macro': make_scorer(f1_score, average='macro', zero_division=0),

            'pres_micro': make_scorer(precision_score, average='micro', zero_division=0),
            'pres_macro': make_scorer(precision_score, average='macro', zero_division=0),

            'rec_micro': make_scorer(recall_score, average='micro', zero_division=0),
            'rec_macro': make_scorer(recall_score, average='macro', zero_division=0),
        }

    def __prepare_results(self, results: pd.DataFrame):
        self.results = ExplorerResult()

