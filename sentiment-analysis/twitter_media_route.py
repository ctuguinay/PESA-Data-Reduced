import tweepy
from dotenv import load_dotenv
import os
import csv
import datetime
import string
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_score



def remove_punctuation(text):
    if type(text) != str:
        return ''
    return text.translate(str.maketrans('', '', string.punctuation))

if __name__ == "__main__":
    # Load device's environment.
    dotenv_path = os.path.abspath('twitter.env')
    load_dotenv(dotenv_path)

    # Get tokens.
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
    BEARER_TOKEN = os.environ['BEARER_TOKEN']

    # Authentication with Twitter.
    Client = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=CONSUMER_KEY, 
    consumer_secret=CONSUMER_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

    f = open('naive_labeled_data.csv', 'w+', encoding='UTF8', newline='')
    writer = csv.writer(f)
    writer.writerow(['text', 'sentiment'])

    HASHTAG = '#MarcosNotAHero'
    NUM_TWEETS = 100
    START_TIME = datetime.datetime(2022, 9, 7)

    tweets = Client.search_recent_tweets(query = HASHTAG, max_results = NUM_TWEETS, tweet_fields=['lang'])[0]

    # Only include English Tweets
    for tweet in tweets:
        if tweet.lang == 'en':
            writer.writerow([tweet.text, '0'])

    HASHTAG = '#BongBongMarcos' #MarcosTheRealHero

    tweets = Client.search_recent_tweets(query = HASHTAG, max_results = NUM_TWEETS, tweet_fields=['lang'])[0]

    for tweet in tweets:
        if tweet.lang == 'en':
            writer.writerow([tweet.text, '1'])

    f.close()

    print(data.head())
    data = data.convert_dtypes()
    print(data.info())

    data.sentiment.hist()
    print(data.shape)

    data.drop_duplicates(inplace=True)
    print(data.shape)

    data.sentiment.hist()

    data['clean_text'] = data['text'].apply(remove_punctuation)
    print(data.head())

    data = data.astype({'sentiment': 'int', 'clean_text': 'string'})

    vectorizer = TfidfVectorizer(max_df=0.95, lowercase=True)  # ignore words with very high doc frequency
    tf_idf = vectorizer.fit_transform(data['clean_text'])
    words = vectorizer.get_feature_names_out()

    tf_idf = normalize(tf_idf)

    tf_idf = tf_idf.toarray()
    print(tf_idf.shape)

    y = data.sentiment
    print(y.shape)

    X_train, X_test, y_train, y_test = train_test_split(tf_idf, y, test_size= .2)

    print(y_test)

    print(1- np.mean(y_train)) # naive accuracy baseline

    svc = SVC(kernel='sigmoid', gamma=1.0)
    knc = KNeighborsClassifier(n_neighbors=2)
    mnb = MultinomialNB(alpha=0.2)
    dtc = DecisionTreeClassifier(min_samples_split=2)
    lrc = LogisticRegression(solver='liblinear', penalty='l1')
    rfc = RandomForestClassifier(n_estimators=31)
    ada = AdaBoostClassifier()

    classifiers = {'SVC' : svc,'KNeighborsClassifier' : knc, 
        'Multinomial Naive Bayes': mnb, 'Decision Tree': dtc, 
        'Logistic Regression': lrc, 'Random Forest': rfc, 'AdaBoost': ada}

    model_pred_scores = []
    for k, m in classifiers.items():
        m.fit(X_train, y_train)
        y_hat = m.predict(X_test)
        model_pred_scores.append((k, [accuracy_score(y_test , y_hat)]))
    
    cross_val_model_pred_scores = []
    for k, m in classifiers.items():
        scores = cross_val_score(m, X_test, y_test, cv=2)
        cross_val_model_pred_scores.append((k, scores.mean()))
    
    print(model_pred_scores)
    print(cross_val_model_pred_scores)