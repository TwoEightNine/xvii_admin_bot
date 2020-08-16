from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

# list of tuples (estimator, params) to perform GridSearch
search_estimators = [
    (KNeighborsClassifier(), {
        'n_neighbors': [3, 5, 7, 9],
        'weights': ['distance', 'uniform'],
        'n_jobs': [-1]
    }),
    (RandomForestClassifier(), {
        'n_estimators': [100, 300],
        'max_depth': [None, 1, 2, 3],
        'random_state': [289],
        'n_jobs': [-1]
    })
]

# final estimator
estimator = KNeighborsClassifier(n_neighbors=3, weights='distance', n_jobs=-1)


# filters non-informative messages
def is_text_informative(text):
    """
    defines if text is going to be informative for model
    :param text: message to check
    :return: true if message is informative, false if deny the message
    """
    return len(text) != 0 \
           and 'CRASH REPORT' not in text \
           and 'android.' not in text \
           and '[service]' not in text \
           and 'DEVICE INFORMATION' not in text \
           and 'com.twoeightnine.root.xvii.' not in text \
           and 'okhttp3.internal.' not in text \
           and '[longpoll]' not in text
