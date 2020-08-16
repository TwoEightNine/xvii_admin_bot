import argparse
import time

import files
import social
import predictor

marker_leave_unread = '__UNREAD'
marker_mark_as_read = '__READ'

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='final bot that sends predicted answers to users')
    parser.add_argument('--social', required=True,
                        help=f'which social network to use (supported values: {social.supported_socials})')
    args = parser.parse_args()

    social_network = social.create_social(args.social)
    if not social_network:
        print(f'incorrect social network passed: {args.social}. use -h to see help')
        exit(0)

    responses = files.load_class_responses()
    pr = predictor.Predictor(files.load_pipeline(), files.load_classes())
    while True:
        try:
            messages = social_network.wait_for_messages()
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
                    social_network.mark_message_as_read(message.peer_id, message.id)
                elif response != marker_leave_unread:
                    social_network.send_message(message.peer_id, response)

                print('')
        except Exception as e:
            print(f'error occurred: {e}')
            time.sleep(5)
