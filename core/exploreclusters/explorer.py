from .models import ExplorerParams, ExplorerResults
from .explore_progress import ExploreProgress
from core.transformers import CleanTextTransformer
from core.model import ClusteringMetrics

from sklearn.cluster import SpectralClustering
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score


class ClusterExplorer:

    def __init__(self, params: ExplorerParams, progress: ExploreProgress):
        self.params = params
        self.progress = progress
        self.results = None

    def explore(self, messages: list):
        self.progress.on_exploration_started()
        clean_messages = CleanTextTransformer().fit_transform(messages)
        tfidf_vectors = TfidfVectorizer().fit_transform(clean_messages)
        tfidf_dense = tfidf_vectors.todense()

        sil_scores = []
        dav_scores = []
        cal_scores = []
        cluster_counts = []
        max_sil_score = 0
        clusters = 2
        while len(sil_scores) == 0 or sil_scores[-1] > 0.8 * max_sil_score:
            self.progress.on_explored_clusters(clusters)
            model = SpectralClustering(
                n_clusters=clusters,
                random_state=self.params.random_state,
                n_jobs=-1
            ).fit(tfidf_vectors)
            labels = model.labels_

            sil_score = silhouette_score(tfidf_dense, labels)
            dav_score = davies_bouldin_score(tfidf_dense, labels)
            cal_score = calinski_harabasz_score(tfidf_dense, labels)

            if sil_score > max_sil_score:
                max_sil_score = sil_score
            cluster_counts.append(clusters)

            sil_scores.append(sil_score)
            dav_scores.append(dav_score)
            cal_scores.append(cal_score)

            clusters += max(2, int(round(clusters * 0.1)))

        self.results = ExplorerResults()
        for i in range(len(cluster_counts)):
            self.results.add_metrics(cluster_counts[i], ClusteringMetrics(
                sil_scores[i],
                dav_scores[i],
                cal_scores[i]
            ))
        self.progress.on_results_ready()
