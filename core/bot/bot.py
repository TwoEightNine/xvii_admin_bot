from core.predictor import Predictor
from core.model import Prediction
from core.social import AbsSocial
from core.logger import Logger


class Bot:

    def __init__(self, predictor: Predictor, social: AbsSocial, logger: Logger):
        self.predictor = predictor
        self.social = social
        self.logger = logger

    def start(self):
        while True:
            try:
                messages = self.social.wait_for_messages()
                for message in messages:
                    prediction = self.predictor.predict(message.text)
                    self.logger.log(f'{message.peer_id}: {message.text} ({prediction.prediction_class})')
                    self.logger.log(f'response: {prediction.prediction_result}')

                    # perform action according to response
                    if prediction.prediction_class == Prediction.class_mark_as_read:
                        self.social.mark_message_as_read(message.peer_id, message.id)
                    elif prediction.prediction_class != Prediction.class_leave_unread:
                        self.social.send_message(message.peer_id, prediction.prediction_result)

                    self.logger.log('')
            except Exception as e:
                self.logger.log('error occurred', e)
