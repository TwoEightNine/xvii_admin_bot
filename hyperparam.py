from sklearn.neighbors import KNeighborsClassifier
from social import VkSocial, AbsSocial

# globally defined random state to reproduce results
random_state = 289

# how many recent messages to fetch
peers_count = 800

# how many cluster do we want to find
clusters_count = 50

# n_components parameter for PCA (None if do not use PCA)
pca_n_components = 0.99

# final estimator
estimator = KNeighborsClassifier(n_neighbors=3, weights='distance', n_jobs=-1)

# delegate to work with specified social network
social: AbsSocial = VkSocial()


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
