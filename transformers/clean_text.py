from string import punctuation

import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem
from sklearn.base import TransformerMixin, BaseEstimator


class CleanTextTransformer(TransformerMixin, BaseEstimator):

    def __init__(self) -> None:
        super().__init__()
        self._mystem = Mystem()
        self._russian_stopwords = stopwords.words("russian")
        nltk.download("stopwords")

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return [self.__clean_text(text) for text in X]

    def fit_transform(self, X, y=None, **fit_params):
        return [self.__clean_text(text) for text in X]

    def __clean_text(self, text):
        tokens = self._mystem.lemmatize(text.lower())
        tokens = [token for token in tokens if token not in self._russian_stopwords
                  and token != " "
                  and token.strip() not in punctuation]

        return " ".join(tokens)
