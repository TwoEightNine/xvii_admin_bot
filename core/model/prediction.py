class Prediction:

    class_undefined = 'undefined'
    class_mark_as_read = '__READ'
    class_leave_unread = '__UNREAD'

    def __init__(self, prediction_class: str, prediction_result: str):
        self.prediction_class = prediction_class
        self.prediction_result = prediction_result
