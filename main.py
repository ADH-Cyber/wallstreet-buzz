import os
import praw
import re
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta  # Import datetime module

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

# Get stock ticker mentions
ticker_pattern = re.compile(r'\b[A-Z]{1,5}\b')  # Basic pattern for stock tickers
stock_mentions = {}

for post in posts:
    tickers = ticker_pattern.findall(post['title'] + ' ' + post['selftext'])
    for ticker in tickers:
        if ticker not in stock_mentions:
            stock_mentions[ticker] = []
        stock_mentions[ticker].append(post['created'])

# Get historical stock data for the last 30 days and visualize
for ticker, timestamps in stock_mentions.items():
    # Calculate start date as 30 days before the current date
    start_date = datetime.now() - timedelta(days=30)

    # Convert start_date to string in the format 'YYYY-MM-DD' required by yfinance
    start_date_str = start_date.strftime('%Y-%m-%d')

    # Fetch historical stock data for the last 30 days
    stock_data = yf.download(ticker, start=start_date_str, end=datetime.now().strftime('%Y-%m-%d'))

    # Plot stock data
    plt.figure(figsize=(10, 6))
    stock_data['Close'].plot(label='Close Price')
    plt.title(f'{ticker} Historical Data (Last 30 Days)')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()

    # Save plot to a folder in pwd
    output_folder = 'stock_visualizations'
    os.makedirs(output_folder, exist_ok=True)
    plt.savefig(os.path.join(output_folder, f'{ticker}_historical_data_last_30_days.png'))
    plt.close()  # Close the plot to release memory
