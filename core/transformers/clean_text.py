from sklearn.base import TransformerMixin, BaseEstimator

from core import utils


class CleanTextTransformer(TransformerMixin, BaseEstimator):
    """
    transformer to lemmatize and clean text. uses method from utils
    because of pymystem3 that is not serializable and cannot be
    pickled inside a pipeline
    """

    def __init__(self) -> None:
        super().__init__()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return [self.__clean_text(text) for text in X]

    def fit_transform(self, X, y=None, **fit_params):
        return [self.__clean_text(text) for text in X]

    def __clean_text(self, text):
        return utils.clean_text(text)
