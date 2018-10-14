from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor

import tw_credentials

class TWClient():
    def __init__(self,tw_user=None):
        self.auth = TWAuthenticator().authenticate_twitter_app()
        self.tw_client = API(self.auth)
        self.tw_user = tw_user

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

if __name__ == "__main__":
    fetched_tweets_filename = "tweets_test.json"
    hashtag_list = ['tesla','microsoft']

    tw_client = TWClient('elonmusk')
    #print(tw_client.get_user_tl_tweets(1))
    print(tw_client.get_followers())

    #tw_streamer = TWStreamer()
    #tw_streamer.stream_tweets(fetched_tweets_filename,hashtag_list)