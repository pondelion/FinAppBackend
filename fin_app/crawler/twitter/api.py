import tweepy

from utils.config import TwitterConfig

_auth = tweepy.OAuthHandler(
    TwitterConfig.CONSUMER_KEY,
    TwitterConfig.CONSUMER_SECRET
)
_auth.set_access_token(
    TwitterConfig.ACCESS_TOKEN_KEY,
    TwitterConfig.ACCESS_TOKEN_SECRET,
)

API = tweepy.API(_auth)
