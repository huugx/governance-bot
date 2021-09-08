import praw
import os
from dotenv import load_dotenv
# from keep_alive import keep_alive

load_dotenv()

reddit = praw.Reddit(
    client_id = os.getenv('client_id'),
    client_secret = os.getenv('client_secret'),
    username = os.getenv('username'),
    password = os.getenv('password'),
    user_agent = "<CrosspostBot1.0 by u/kohrts>"
)

subreddit_ = reddit.subreddit("ethtrader")
destination = 'u_DonutGovernanceBot'
sort = 'new'
# keyword = 'friend'
keyword = 'governance poll'
keywords = '[governance poll]', '[poll proposal]'

posts = []
        
def clean_string(raw_string):
    cleaned_string = raw_string.lower()
    return cleaned_string


for submission in subreddit_.search(keyword, sort, limit=150):
    for key in keywords:
            if key in clean_string(submission.title):
                posts.append(submission.id)
            
posts.reverse()

for post in posts:
    
    submission = reddit.submission(post)
    
    if hasattr(submission, "crosspost_parent"):
        print(post + ' - CROSSPOST - ' + submission.title)

    else:
        print(post + ' - ' + submission.title)
        submission.crosspost(subreddit=destination, send_replies=False)
