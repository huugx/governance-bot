import praw
import os
import tweepy
import coinsupply as coin
import datetime
from dotenv import load_dotenv



load_dotenv()

# Authenticate to Twitter
api_token = os.getenv('api_token')
api_secret = os.getenv('api_secret')
access_token = os.getenv('access_token')
access_secret = os.getenv('access_secret')

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

# subreddit = reddit.subreddit('ethtrader')
# keywords = '[governance poll]', '[poll proposal]'
destination = 'u_DonutGovernanceBot'
prevPost = []

# Debug
subreddit = reddit.subreddit('all')
keywords = 'dog', 'friend'

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
        # prevPost.append(submission.id)
        # submission.crosspost(subreddit=destination, send_replies=False)
        self.comment_supply(submission)
    
    def comment_supply(self, submission):
        if keywords[0] in clean_string(submission.title):
          date = datetime.datetime.utcnow()
          supply = coin.coinHistory()
          print("[Total Donut Supply](https://www.coingecko.com/en/coins/donut) on " + date.strftime("%Y %b %d at %H:%M") + " UTC was " + str(supply) + "\n" + "\n" + "*I am a bot, and this was performed automatically as a record of the total donut supply at governance polls.*")
          # submission.reply("[Total Donut Supply](https://www.coingecko.com/en/coins/donut) on " + date.strftime("%Y %b %d at %H:%M") + " UTC was " + str(supply) + "\n" + "\n" + "*I am a bot, and this was performed automatically as a record of the total donut supply at governance polls.*")
          self.tweet_poll(submission)

        else:
          self.tweet_proposal(submission)

    def tweet_poll(self,submission):
        print("Beep boop! New r/Ethtrader Governance Poll: " + "\n" +  "https://redd.it/" + submission.id)
        # api.update_status("Beep boop! New r/Ethtrader Governance Poll: " + "\n" +  "https://redd.it/" + submission.id)

    def tweet_proposal(self,submission):
        print("Beep boop! New r/Ethtrader Poll Proposal: " + "\n" +  "https://redd.it/" + submission.id)
        # api.update_status("Beep boop! New r/Ethtrader Governance Poll: " + "\n" +  "https://redd.it/" + submission.id)

# keep_alive()
bot = RedditBot()
for submission in subreddit.stream.submissions(skip_existing=True):
    bot.find_match(submission)