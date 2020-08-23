import json

from core.exploremodels import ExplorerResult
from core.model import ClassificationMetrics
from usecase.datasource import ModelsExplorerDataSource


class JsonModelsExplorerDataSource(ModelsExplorerDataSource):
    key_results = 'results'
    key_model_name = 'model_name'
    key_params = 'params'
    key_metrics = 'metrics'
    key_metric_f1_micro = 'f1_micro'
    key_metric_f1_macro = 'f1_macro'
    key_metric_precision_micro = 'precision_micro'
    key_metric_precision_macro = 'precision_macro'
    key_metric_recall_micro = 'recall_micro'
    key_metric_recall_macro = 'recall_macro'

    def __init__(self, file_name: str):
        self.file_name = file_name

    def save_results(self, results: ExplorerResult):
        with open(self.file_name, 'w') as fp:
            result_list = []
            for model, metrics in results.get_results().items():
                model_name, params = model
                result_list.append({
                    self.key_model_name: model_name,
                    self.key_params: params,
                    self.key_metrics: {
                        self.key_metric_f1_macro: metrics.f1_macro,
                        self.key_metric_f1_micro: metrics.f1_micro,
                        self.key_metric_precision_macro: metrics.precision_macro,
                        self.key_metric_precision_micro: metrics.precision_micro,
                        self.key_metric_recall_macro: metrics.recall_macro,
                        self.key_metric_recall_micro: metrics.recall_micro,
                    }
                })
            json.dump({self.key_results: result_list}, fp)

    def get_results(self) -> ExplorerResult:
        with open(self.file_name, 'r') as fp:
            explorer_result = ExplorerResult()
            result_list = json.load(fp)[self.key_results]
            for result in result_list:
                result_metrics = result[self.key_metrics]
                model = result[self.key_model_name], result[self.key_params]
                metrics = ClassificationMetrics(
                    f1_micro=result_metrics[self.key_metric_f1_micro],
                    f1_macro=result_metrics[self.key_metric_f1_macro],
                    precision_micro=result_metrics[self.key_metric_precision_micro],
                    precision_macro=result_metrics[self.key_metric_precision_macro],
                    recall_micro=result_metrics[self.key_metric_recall_micro],
                    recall_macro=result_metrics[self.key_metric_recall_macro],
                )
                explorer_result.add_result(model, metrics)
            return explorer_result
