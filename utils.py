import requests
import json
from notebooks.secret import access_token

base_url = 'https://api.vk.com/method/'


def execute(method, params):
    url = base_url + method + '?'
    for k, v in params.items():
        url += k + '=' + str(v) + '&'
    url += f'access_token={access_token}&v=5.103'
    r = requests.get(url).text
    response = None
    err = None
    try:
        response = json.loads(r)
    except Exception as e:
        err = str(e)
    try:
        if 'response' not in response:
            err = response['error']
            err = str(err['error_code']) + ': ' + err['error_msg']
            response = None
        else:
            response = response['response']
    except Exception as e:
        err = f'error while parsing: {e}'
    return err, response

