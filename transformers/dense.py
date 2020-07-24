from sklearn.base import TransformerMixin


class DenseTransformer(TransformerMixin):
    """
    transformer to convert sparse array into dense array
    """

    def __init__(self) -> None:
        super().__init__()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return X.todense()

    def fit_transform(self, X, y=None, **fit_params):
        return X.todense()
