import praw
import os
import tweepy
import time
import coinsupply as coin
from discord import Webhook, RequestsWebhookAdapter
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
    user_agent = "<CrosspostBot1.0 by u/DonutGovernanceBot>",
    check_for_async=False
)

#Authenticate to Discord
discord_distribution = str(os.getenv('discord_distribution'))
discord_improvements = str(os.getenv('discord_improvements'))

webhookDistribution = Webhook.from_url(discord_distribution, adapter=RequestsWebhookAdapter())
webhookImprovements = Webhook.from_url(discord_improvements , adapter=RequestsWebhookAdapter())

subreddit = reddit.subreddit('ethtrader')
keywords = '[governance poll]', '[poll proposal]', '[governance proposal]', '[donut initiative]'
keyUser = 'CommunityPoints'
destination = 'u_DonutGovernanceBot'
prevPost = []

# Debug
# subreddit = reddit.subreddit('all')
# keywords = 'dog', 'friend', 'win', 'tomorrow'
# keyUser = 'go'

def clean_string(raw_string):
    cleaned_string = raw_string.lower()
    return cleaned_string

class RedditBot:
    def find_match(self, submission):
        for key in keywords:
            if key in clean_string(submission.title):
              self.make_post(submission)

        if keyUser in str(submission.author):
          self.make_post(submission)


    def make_post(self, submission):
      if submission.id in prevPost:
        print('duplicate: ' + submission.id)
        
      else:
        print(submission.id + ' - ' + str(submission.author))
        prevPost.append(submission.id)
        submission.crosspost(subreddit=destination, send_replies=False)
        self.comment_supply(submission)
    
    def comment_supply(self, submission):
        if keywords[0] in clean_string(submission.title):
          date = datetime.datetime.utcnow()
          supply = coin.coinHistory()
          print("[Total Donut Supply](https://www.coingecko.com/en/coins/donut) on " + date.strftime("%Y %b %d at %H:%M") + " UTC was " + str(supply) + "\n" + "\n" + "*I am a bot, and this was performed automatically to provide a record of the total donut supply at each governance poll.*")
          submission.reply("[Total Donut Supply](https://www.coingecko.com/en/coins/donut) on " + date.strftime("%Y %b %d at %H:%M") + " UTC was " + str(supply) + "\n" + "\n" + "*I am a bot, and this was performed automatically as a record of the total donut supply at each governance poll.*")
          self.tweet_poll(submission)

        elif keywords[1] in clean_string(submission.title):
          self.tweet_proposal(submission)

        elif keywords[2] in clean_string(submission.title):
          self.tweet_initiative(submission)

        elif keywords[3] in clean_string(submission.title):
          self.tweet_initiative(submission)  

        else:
          self.tweet_distribution(submission)
          

    def tweet_poll(self,submission):
        print("Beep boop! New r/Ethtrader Governance Poll: " + "\n" +  "https://redd.it/" + submission.id)
        api.update_status("Beep boop! New r/Ethtrader Governance Poll: " + "\n" +  "https://redd.it/" + submission.id)
        webhookImprovements.send("@everyone New r/Ethtrader Governance Poll: " + "\n" +  "https://redd.it/" + submission.id)
        

    def tweet_proposal(self,submission):
        print("Beep boop! New r/Ethtrader Poll Proposal: " + "\n" +  "https://redd.it/" + submission.id)
        api.update_status("Beep boop! New r/Ethtrader Poll Proposal: " + "\n" +  "https://redd.it/" + submission.id)
        webhookImprovements.send("@everyone New r/Ethtrader Poll Proposal: " + "\n" +  "https://redd.it/" + submission.id)
        

    def tweet_initiative(self,submission):
        print("Beep boop! New r/Ethtrader Donut Initiative: " + "\n" +  "https://redd.it/" + submission.id)
        api.update_status("Beep boop! New r/Ethtrader Donut Initiative: " + "\n" +  "https://redd.it/" + submission.id)
        webhookImprovements.send("@everyone New r/Ethtrader Donut Initiative: " + "\n" +  "https://redd.it/" + submission.id)

    def tweet_distribution(self, submission):
        print("Beep boop! New r/Ethtrader Donut Distribution: " + "\n" +  "https://redd.it/" + submission.id)
        api.update_status("Beep boop! New r/Ethtrader Donut Distribution: " + "\n" +  "https://redd.it/" + submission.id)
        webhookDistribution.send("@everyone New r/Ethtrader Donut Distribution: " + "\n" +  "https://redd.it/" + submission.id)
        
bot = RedditBot()

running = True
while running:
  try:
    print("u/DonutGovernanceBot reporting for duty!")
    for submission in subreddit.stream.submissions(skip_existing=True):
      bot.find_match(submission)
  except KeyboardInterrupt:
    running = False
  except Exception:
    print("Taking a breather...")
    time.sleep(30)
