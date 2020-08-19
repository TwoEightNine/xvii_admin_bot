from core.model import ClusteringMetrics


class MakerParams:

    def __init__(self, clusters_count: int, random_state: int):
        self.clusters_count = clusters_count
        self.random_state = random_state


class MakerResults:

    def __init__(self, metrics: ClusteringMetrics, message_labels: list):
        self.metrics = metrics
        self.message_labels = message_labels
        self.explanation = []

    class ClusterExplanation:

        def __init__(self, cluster_index: int, words_count: int, frequent_words: list):
            self.cluster_index = cluster_index
            self.words_count = words_count
            self.frequent_words = frequent_words
