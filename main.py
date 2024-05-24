import os
import praw
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Reddit instance with environment variables
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

# Point to the subreddit
subreddit = reddit.subreddit('wallstreetbets')

posts = []
# Convert MAX_POSTS to integer
max_posts = int(os.getenv("MAX_POSTS"))
for submission in subreddit.hot(limit=max_posts):
    post = {
        'title': submission.title,
        'selftext': submission.selftext,
        'created': submission.created_utc,
        'upvotes': submission.ups,
        'comments': [comment.body for comment in submission.comments if isinstance(comment, praw.models.Comment)]
    }
    posts.append(post)

# Print fetched data nicely
for post in posts:
    print("Title:", post['title'])
    print("Selftext:", post['selftext'])
    print("Created:", post['created'])
    print("Upvotes:", post['upvotes'])
    print("Comments:", post['comments'])
    print()
