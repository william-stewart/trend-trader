from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import tw_credentials
import numpy as np
import pandas as pd

class TWClient():
    def __init__(self,tw_user=None):
        self.auth = TWAuthenticator().authenticate_twitter_app()
        self.tw_client = API(self.auth)
        self.tw_user = tw_user

    def get_tw_client_api(self):
        return self.tw_client

    def get_user_tl_tweets(self,num_tweets):
        tweets = []
        for tweet in Cursor(self.tw_client.user_timeline,id=self.tw_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self,num_friends):
        friend_list=[]
        for friend in Cursor(self.tw_client.friends,id=self.tw_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self,num_tweets):
        home_timeline_tweets=[]
        for tweet in Cursor(self.tw_client.home_timeline,id=self.tw_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

    #be wary of using this as it is easy to hit the rate limit exception very quickly
    def get_followers(self):
        followers=[]
        for follower in Cursor(self.tw_client.followers,id=self.tw_user).items():
            followers.append(follower)
        return followers

class TWAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(tw_credentials.CONSUMER_KEY, tw_credentials.CONSUMER_SECRET)
        auth.set_access_token(tw_credentials.ACCESS_TOKEN, tw_credentials.ACCESS_TOKEN_SECRET)
        return auth

class TWStreamer():
    """
    Stream live tweets
    """
    def __init__(self):
        self.tw_authenticator = TWAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hashtag_list):
        listener = TWListeneter(fetched_tweets_filename)
        auth = self.tw_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=hashtag_list)

class TWListeneter(StreamListener):
    """
    Standard listener
    """
    def __init__(self,fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self,data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            return False
        print(status)

class TWAnalysis():
    def tweets_to_data_frame(self,tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets],columns=['tweet'])

        #df['text']=np.array([tweet.text for tweet in tweets])
        df['user']=np.array([tweet.user.screen_name for tweet in tweets])
        df['id']=np.array([tweet.id for tweet in tweets])
        df['len']=np.array([len(tweet.text) for tweet in tweets])
        df['date']=np.array([tweet.created_at for tweet in tweets])
        df['source']=np.array([tweet.source for tweet in tweets])
        df['likes']=np.array([tweet.favorite_count for tweet in tweets])
        df['retweets']=np.array([tweet.retweet_count for tweet in tweets])
        df['replyto']=np.array([tweet.in_reply_to_screen_name for tweet in tweets])

        return df

if __name__ == "__main__":
    tw_client = TWClient()
    tw_analysis = TWAnalysis()
    api = tw_client.get_tw_client_api()

    tweets = api.user_timeline(screen_name='elonmusk',count=10)

    #print(dir(tweets[0]))
    df = tw_analysis.tweets_to_data_frame(tweets)
    #print(df.head(50))

    #text
    #print("Text: " + np.mean(df['text'])).encode('utf-8')

    #mean length
    print("Average length: " + str(np.mean(df['len'])))

    #most likes
    print('Most likes: ' + str(np.max(df['likes'])))

    #most retweets
    print('Most retweets: ' + str(np.max(df['retweets'])))