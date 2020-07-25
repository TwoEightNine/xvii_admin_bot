import time

import files
import hyperparam
import predictor

marker_leave_unread = '__UNREAD'
marker_mark_as_read = '__READ'

if __name__ == "__main__":
    responses = files.load_class_responses()
    pr = predictor.Predictor(files.load_pipeline(), files.load_classes())
    social = hyperparam.social
    while True:
        try:
            messages = social.wait_for_messages()
            for message in messages:
                message_class = pr.predict(message.text)
                print(f'{message.peer_id}: {message.text} ({message_class})')

                # find response
                if message_class in responses:
                    response = responses[message_class]
                else:
                    response = marker_leave_unread
                print(f'response: {response}')

                # perform action according to response
                if response == marker_mark_as_read:
                    social.mark_message_as_read(message.peer_id, message.id)
                elif response != marker_leave_unread:
                    social.send_message(message.peer_id, response)

                print('')
        except Exception as e:
            print(f'error occurred: {e}')
            time.sleep(5)
