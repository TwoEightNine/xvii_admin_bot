import collections

from .models import MakerParams, MakerResults
from core.model import ClusteringMetrics
from core.transformers import CleanTextTransformer

from sklearn.cluster import SpectralClustering
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score


class ClusterMaker:

    def __init__(self, params: MakerParams):
        self.params = params
        self.results = None

    def make_clusters(self, messages: list):
        clean_messages = CleanTextTransformer().fit_transform(messages)
        tfidf_vectors = TfidfVectorizer().fit_transform(clean_messages)
        tfidf_dense = tfidf_vectors.todense()

        sc_model = SpectralClustering(
            n_clusters=self.params.clusters_count,
            random_state=self.params.random_state,
            n_jobs=-1
        ).fit(tfidf_vectors)

        metrics = ClusteringMetrics(
            silhouette_score(tfidf_dense, sc_model.labels_),
            davies_bouldin_score(tfidf_dense, sc_model.labels_),
            calinski_harabasz_score(tfidf_dense, sc_model.labels_)
        )
        self.results = MakerResults(metrics, sc_model.labels_)

        for cl_i in range(self.params.clusters_count):
            cluster_messages = []
            for i in range(len(clean_messages)):
                if sc_model.labels_[i] == cl_i:
                    cluster_messages += clean_messages[i].split(' ')

            count = collections.Counter(cluster_messages)
            total = len(cluster_messages)

            frequent_words = []
            for word, cnt in count.items():
                if cnt > total * 0.05:
                    frequent_words.append((word, cnt / total))

            self.results.explanation.append(MakerResults.ClusterExplanation(cl_i, total, frequent_words))
