import sys
import time
import numpy as np
import praw
import reddit_connect

n_sub = int(sys.argv[1]) if len(sys.argv) > 1 else 3


def get_up_and_down_vote(sub):
    ratio = sub.upvote_ratio
    ups = int(round((ratio*sub.score)/(2*ratio - 1))
              if ratio != 0.5 else round(sub.score/2))
    downs = ups - sub.score
    return ups, downs


client_id = reddit_connect.get_client_id()
client_secret = reddit_connect.get_client_secret()
username = reddit_connect.get_username()
password = reddit_connect.get_passwd()
user_agent = 'BayesHackersClient/0.1 by ' + username


reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password,
)
subreddit = reddit.subreddit("showerthoughts")

t_stamp = time.time()
save_npy_name = 'up_down_votes_t%d' % t_stamp
save_contents_name = 'contents_t%d.txt' % t_stamp
# go by timespan - 'hour', 'day', 'week', 'month', 'year', 'all'
# might need to go longer than an hour to get entries...
top_submissions = subreddit.top('hour', limit=5)
top_submissions = subreddit.top('all', limit=n_sub)

top_submission = next(top_submissions)
top_post = top_submission.title
u, d = get_up_and_down_vote(top_submission)

upvotes = [u]
downvotes = [d]
contents = [top_post]

for sub in top_submissions:
    try:
        u, d = get_up_and_down_vote(sub)
        upvotes.append(u)
        downvotes.append(d)
        contents.append(sub.title)
    except Exception as e:
        continue

votes = np.array([upvotes, downvotes]).T
np.save(save_npy_name, votes)
with open(save_contents_name, 'w') as f:
    for s in contents:
        f.write(s + '\n')

print('output files = {}, {}'.format(
    save_npy_name + '.npy', save_contents_name
))
