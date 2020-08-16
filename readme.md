## russian answer bot for groups of vk (and not only)

this is ML-solution to create a bot for groups of vk social network 
(but you can easily create your own social network delegate).
the bot's behavior is based on real users' messages sent earlier. 
currently the bot supports only russian language

this bot was created to assist me with answering the most frequent questions in vk group's messages (see [xvii messenger for vk](https://github.com/TwoEightNine/XVII))

read further for more information about how it works

**this project is in state of baseline**

### installation

#### step 0. cloning and setup

clone this repository using git
```bash
git clone https://github.com/TwoEightNine/xvii_admin_bot.git
cd xvii_admin_bot
```

then install and activate a virtual environment

```bash
sudo apt install python3-venv
python3.6 -m venv admin_bot_env
source admin_bot_env/bin/activate
pip install -r requirements.txt
```

in the root directory you should create file `secret.py` with some sensitive information. the file should be like this:

```python
access_token = 'your token here'
no_fetch_users = [13371337228]
```

`access_token` is a token to access group messages (to obtain the token visit [this page](https://vk.com/dev/authcode_flow_group), do not forget to use `scope=messages,offline`).
`no_fetch_user` is a list of users' ids. if you want to ignore messages from a user, put here his id

#### step 1. fetching messages

to fetch messages run
```bash
python3 fetcher.py --count COUNT --social SOCIAL [-h]
```

where `COUNT` is how many dialogs to fetch to get messages from, 
`SOCIAL` is which social network to use. request `-h` help
to see which social networks are supported

the script will load messages into `data/messages.csv`

#### step 2. find clusters

to perform semi-automatic labelling here goes this step. 
fetched messages are being lemmatized and cleaned, then converted to tf-idf vectors.
spectral clustering is used. to perform clustering run:

```bash
python3 clusterizer.py [--search] [--clusters_count CL_COUNT] --random_state RND_ST [-h]
```

where `--search` is an optional flag to perform search for better clusters count,
`--clusters_count` is required to perform final clustering, 
defines preferred number of clusters,
`--random_state` is a random int for better reproducibility

you may want to run search (with `--search` flag) to calculate clustering metrics
for different number of clusters. in this case the script will print this information

after search you have already defined 'good' clusters count for your task.
now run this script again but with `--clusters_count YOUR_VALUE` and 
the script will create `data/model_explanation.txt` 
with information about the most frequent words in every cluster.
if you think that the result of clustering is not so good,
you can rerun clustering with other number of cluster or other random state


using the data you are going to create `classes.json` in next format:

```json
{
  "your_class_1": {
    "clusters": [3, 7, 11],
    "response": "your_response_for_class_1"
  },
  "your_class_2": {
    "clusters": [2],
    "response": "__UNREAD"
  },
  "your_class_3": {
    "clusters": [16],
    "response": "your_response_for_class_3"
  }
}
```

this will help to convert clusters into needed classes.
using these classes the model will train. 

`clusters` are indexes of clusters that matches your class
`response` is an answer to user. this field may contain special markers 
like `__UNREAD` and `__READ`. in these cases the response will not be sent
but the conversation will be left read (no answer needed) or unread 
(human attention needed)

all not mentioned clusters implicitly belong to class `undefined` 
with response `__UNREAD`

#### step 3. find and train a model

after you created `classes.json` you can start to search for and train a model to
perform predictions. 

to search execute

```bash
python3 modeller.py --search [--cv CV] [--sort_by METRIC]
```

where `--search` is an optional flag that indicates that you want to
perform search (using sklearn's `GridSearch`), 
`CV` is how many k-folds to use in cross validation,
`METRIC` is a metric alias to sort by

you can use default search params (like estimators and parameters) 
or define own in `hyperparams.py` (variable `search_estimators`)

after search you can see 5 best results (according to `--sort_by`)
and explore all configurations in `data/search_results.csv`. best model
should be set in `hyperparams.py` as `final_estimator`

to train a model run

```bash
python3 modeller.py [--cv CV] [--pca_n_components N_COM]
```

where `N_COM` is an argument for `PCA()`'s `n_components` value,
if not set, PCA is not used

`data/model_pipeline.pkl` and `data/model_classes.pkl` will be created

**optionally**, you can interactively check the model using

```bash
python3 predictor.py
```

enter russian message and see which class the model thinks it belongs to

#### step 4. run and chill

the bot is ready to start. to launch it enter

```bash
python3 bot.py --social SOCIAL
```

in stdout you will see status messages, incoming messages and 
predicted answers

###### twoeightnine, 2020