## russian answer bot for vk groups

this is ML-solution to create a bot for vk groups. the bot's behavior is based on real users' messages sent earlier. currently the bot supports only russian language

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
python3 fetcher.py
```

the script will load messages into `data/messages.csv`

#### step 2. find clusters

to perform semi-automatic labelling here goes this step. 
fetched messages are being lemmatized and cleaned, then converted to tf-idf vectors.
spectral clustering is used. to perform clustering run:

```bash
python3 clusterizer.py
```

this script will create `data/model_explanation.txt` 
with information about the most frequent words in every cluster.
if you think that the result of clustering is not so good,
you can rerun clustering with other number of cluster or other random state.
just update related fields in file `hyperparam.py` and rerun the script


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

#### step 3. train model

after you created `classes.json` you can train a model to
perform predictions. currently the model uses pca and knn.
(in future i want to add kind of search through different models)

to train a model run

```bash
python3 modeller.py
```

`data/model_pipeline.pkl` and `data/model_classes.pkl` will be created

**optionally**, you can interactively check the model using

```bash
python3 predictor.py
```

enter russian message and see which class the model thinks it belongs to

#### step 4. run and chill

the bot is ready to start. to launch it enter

```bash
python3 bot.py
```

in stdout you will see status messages, incoming messages and 
predicted answers

###### twoeightnine, 2020