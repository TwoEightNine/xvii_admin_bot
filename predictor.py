from sklearn.pipeline import Pipeline
import numpy as np
import dumper

class_undefined = 'undefined'


class Predictor:

    def __init__(self, pipeline: Pipeline, classes):
        self._pipeline = pipeline
        self._classes = classes

    def predict(self, message):
        pred = self._pipeline.predict([message])
        return self.__ohe_to_label(pred)

    def __ohe_to_label(self, pred):
        if np.sum(pred, axis=1) == 0:
            return class_undefined
        else:
            return self._classes[np.argmax(pred)].replace('class_', '')


if __name__ == "__main__":

    p = Predictor(dumper.load_pipeline(), dumper.load_classes())
    while True:

        input_message = input('>>> ')
        if input_message == '':
            break
        print(f'class: \'{p.predict(input_message)}\'')
