import praw
import os
import tweepy
from dotenv import load_dotenv
# from keep_alive import keep_alive

load_dotenv()

# Authenticate to Twitter
api_token = os.getenv['api_token']
api_secret = os.getenv['api_secret']
access_token = os.getenv['access_token']
access_secret = os.getenv['access_secret']

auth = tweepy.OAuthHandler(api_token, api_secret)
auth.set_access_token(access_token, access_secret)

# Create API object
api = tweepy.API(auth)


# Authenticate to Reddit
reddit = praw.Reddit(
    client_id = os.getenv('client_id'),
    client_secret = os.getenv('client_secret'),
    username = os.getenv('username'),
    password = os.getenv('password'),
    user_agent = "<CrosspostBot1.0>"
)

subreddit = reddit.subreddit('ethtrader')
destination = 'u_DonutGovernanceBot'
prevPost = []
keywords = '[governance poll]', '[poll proposal]'


def clean_string(raw_string):
    cleaned_string = raw_string.lower()
    return cleaned_string

class RedditBot:
    def find_match(self, submission):
        for key in keywords:
            if key in clean_string(submission.title):
              self.make_post(submission)

    def make_post(self, submission):
      if submission.id in prevPost:
        print('duplicate: ' + submission.id)
        
      else:
        print(submission.id + ' - ' + submission.title)
        prevPost.append(submission.id)
        # submission.crosspost(subreddit=destination, send_replies=False)
        self.tweet_post(submission)

    def tweet_post(self,submission):
        print("Beep boop! New r/Ethtrader Governance Poll: " + "\n" +  "https://redd.it/" + submission.id)
        # api.update_status("Beep boop! New r/Ethtrader Governance Poll: " + "\n" +  "https://redd.it/" + submission.id)

# keep_alive()
bot = RedditBot()
for submission in subreddit.stream.submissions(skip_existing=True):
    bot.find_match(submission)