import praw
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()

reddit = praw.Reddit(
    client_id = os.getenv('client_id'),
    client_secret = os.getenv('client_secret'),
    username = os.getenv('username'),
    password = os.getenv('password'),
    user_agent = "<CrosspostBot1.0>"
)

subreddit = reddit.subreddit('all')
destination = 'u_DonutGovernanceBot'
# keyword = 'friend'
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
        print(submission.title)
        # submission.crosspost(subreddit=destination, send_replies=False)

keep_alive()
bot = RedditBot()
for submission in subreddit.stream.submissions(skip_existing=True):
    bot.find_match(submission)
