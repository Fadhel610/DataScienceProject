
## FLASK Libraries
from flask import Flask,render_template, request, send_file
from flask_navigation import Navigation

import tweepy
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import matplotlib.pyplot as plt
import re
from nltk.corpus import stopwords
from PIL import Image
import matplotlib
matplotlib.use('Agg')

consumer_key = 'hNrzglHJXJr8f0qhnno6A6kH4'
consumer_secret = 'Lgh8mtQDpWwzdxFu4kTVoBu2ApTp6ZxsAmNbwqx3r3lOgWjg7F'

access_token = '3424361054-JUZrbrddpzhTvS0iOLQGss71tDXRMus2az6flZc'
access_token_secret = 'JSCQwlLzLG4KNcOELnXEfYfGVao24fGxuxlCMM17wD8yq'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def get_raw_tweets(topic, number):
    print(f'{number} Tweets are being loaded about #{topic} ...')
    tw = []
    for tweet in tweepy.Cursor(api.search,q=f"#{topic} -filter:retweets",
                               lang="en",
                               since="2019-12-30",tweet_mode='extended').items(int(number)):
        tw.append(tweet.full_text)
    print(f'Raw tweets are received successfully!')
    return tw


def clean_tweets(tweets):
    print('Raw tweets are being cleaned ...')
    no_url = [" ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split()) for txt in tweets]
    print('Cleaning is done!')
    return ' '.join(no_url)

skipped_words = list(set(STOPWORDS)) + ['covid19', 'coronavirus', 'covid', 'cov', 'amp']

def plot_could(tweets_strings, topic, number):
    skipped_words = list(set(STOPWORDS)) + ['covid19', 'coronavirus', 'covid', 'cov', 'amp', topic]
    print('Data is being plotted')
    plt.figure(figsize=(15,10))
    wc = WordCloud(stopwords= skipped_words, width=1200, height=800).generate(tweets_strings)
    wc.to_file('static/'+topic+'.png')
    #imgg = Image.open('static/words.png')
  
    print(f'Here is the result of {number} tweets about #{topic}')


def run(topic, number):
    tweets = get_raw_tweets(topic, number)

    tweets_strings = clean_tweets(tweets)

    plot_could(tweets_strings, topic, number)




bio_app = Flask(__name__)
nav = Navigation(bio_app)

#endpoint means the name of the function as in def
nav.Bar('top', [
    nav.Item('Home', endpoint='index'),
    nav.Item('About Me', endpoint='resume')
])

@bio_app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@bio_app.route('/result',methods=['GET','POST'])
def query():
    if request.method == 'POST':
        topic = request.form['topic']
        number = request.form.get('number')
        run(topic, int(number))
        file_name = topic+'.png'
        return render_template('result.html',topic=topic,number=number, file_name = file_name)

@bio_app.route('/resume',methods=['GET','POST'])
def resume():
    return render_template('resume.html')
if __name__ == '__main__':
    bio_app.run(debug=True)