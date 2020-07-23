import json
from string import punctuation

import nltk
import requests
from nltk.corpus import stopwords
from pymystem3 import Mystem

from notebooks.secret import access_token

base_url = 'https://api.vk.com/method/'

mystem = Mystem()
russian_stopwords = stopwords.words("russian")
nltk.download("stopwords")


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


def clean_text(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords
              and token != " "
              and token.strip() not in punctuation]

    return " ".join(tokens)
