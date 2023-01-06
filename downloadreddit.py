# !/usr/bin/python3

import praw
import requests
import os

reddit = praw.Reddit(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET', user_agent='YOUR_USER_AGENT')

subreddit = reddit.subreddit('SUBREDDIT_NAME')
after = None

while True:
    if after == None:
        submissions = subreddit.hot()
    else:
        submissions = subreddit.hot(params={'after': after})

    for submission in submissions:
        if submission.is_video:
            video_url = submission.media['reddit_video']['fallback_url']
            response = requests.get(video_url)
            with open(os.path.join('videos', submission.id + '.mp4'), 'wb') as f:
                f.write(response.content)

    after = submissions[-1].name
