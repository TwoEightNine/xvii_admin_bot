class ClusteringMetrics:

    def __init__(self, silhouette: float, davis_bouldin: float, calinski_harabasz: float):
        self.silhouette = silhouette
        self.davis_bouldin = davis_bouldin
        self.calinski_harabasz = calinski_harabasz


class ClassificationMetrics:

    def __init__(self,
                 f1_micro: float, f1_macro: float,
                 precision_micro: float, precision_macro: float,
                 recall_micro: float, recall_macro: float):
        self.f1_micro = f1_micro
        self.f1_macro = f1_macro
        self.precision_micro = precision_micro
        self.precision_macro = precision_macro
        self.recall_micro = recall_micro
        self.recall_macro = recall_macro
