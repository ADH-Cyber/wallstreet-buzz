import os
import praw
import re
import yfinance as yf
import logging
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dotenv import load_dotenv


def setup_logging():
    """
    Sets up logging configuration based on environment variables.
    Logs are saved to a file with a timestamp in the 'logs' directory.
    Optionally logs to the console if enabled via environment variables.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Ensure the logs directory exists
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)

    # Get the current time and format it
    current_time = datetime.now().strftime('%Y%m%d%H%M')
    log_file = os.path.join(log_dir, f'wsbuzz_{current_time}.log')

    # Get console logging setting from environment variables
    console_logging = os.getenv('CONSOLE_LOGGING', 'False').lower() == 'true'

    # Get logging level setting from environment variables
    logging_level_str = os.getenv('LOGGING_LEVEL', 'INFO').upper()
    logging_level = getattr(logging, logging_level_str, logging.INFO)

    # Log to a file in the logs directory
    handlers = [logging.FileHandler(log_file)]
    if console_logging:
        # Log to the console if enabled
        handlers.append(logging.StreamHandler())

    # Set the logging level and add the handlers
    logging.basicConfig(level=logging_level,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=handlers)

    # Create a logger instance
    logger = logging.getLogger(__name__)
    return logger


def get_reddit_posts(logger):
    """
    Retrieves hot posts from the 'wallstreetbets' subreddit.
    Logs the number of posts retrieved.
    Returns a list of posts with relevant details.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Initialize Reddit instance with environment variables
    reddit = praw.Reddit(client_id=os.getenv("CLIENT_ID"),
                         client_secret=os.getenv("CLIENT_SECRET"),
                         user_agent=os.getenv("USER_AGENT"))

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
            'comments': [comment.body
                         for comment
                         in submission.comments
                         if isinstance(comment, praw.models.Comment)]
        }
        posts.append(post)

    # Log the number of posts retrieved
    logger.info(f'Retrieved {len(posts)} posts from r/wallstreetbets')

    return posts


def graph_stock_data(ticker, start_date_str, logger):
    """
    Fetches historical stock data for the given ticker and date range.
    Creates and saves a plot of the closing prices for the last 30 days.
    Logs the success or any errors that occur.
    """
    try:
        # Fetch historical stock data for the last 30 days
        stock_data = yf.download(
            ticker, start=start_date_str,
            end=datetime.now().strftime('%Y-%m-%d')
        )

        # Log successful data retrieval
        logger.info(f'Successfully retrieved data for {ticker}')

        # Plot stock data
        plt.figure(figsize=(10, 6))
        stock_data['Close'].plot(label='Close Price')
        plt.title(f'{ticker} Historical Data (Last 30 Days)')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.legend()

        # Save plot to a folder in pwd
        output_folder = 'graphs'
        os.makedirs(output_folder, exist_ok=True)
        plt.savefig(os.path.join(output_folder,
                                 f'{ticker}_historical_data_last_30_days.png'))
        plt.close()  # Close the plot to release memory

        # Log plot creation
        logger.info(f'Plot saved for {ticker}')

    except Exception as e:
        # Log any errors that occur
        logger.error(f'Failed to retrieve or plot data for {ticker}: {e}')


def main():
    """
    Main function that sets up logging, retrieves Reddit posts,
    extracts stock ticker mentions, and graphs the stock data for the last
    30 days.
    """
    logger = setup_logging()
    posts = get_reddit_posts(logger)

    # Get stock ticker mentions
    ticker_pattern = re.compile(r'\b[A-Z]{1,5}\b')
    stock_mentions = {}

    for post in posts:
        tickers = ticker_pattern.findall(post['title']
                                         + ' '
                                         + post['selftext'])
        for ticker in tickers:
            if ticker not in stock_mentions:
                stock_mentions[ticker] = []
            stock_mentions[ticker].append(post['created'])

    # Log the stock tickers found
    logger.info(f'Found {len(stock_mentions)} unique stock tickers mentioned')

    # Get historical stock data for the last 30 days and visualize
    for ticker, timestamps in stock_mentions.items():
        # Calculate start date as 30 days before the current date
        start_date = datetime.now() - timedelta(days=30)

        # Convert start_date to string in the format 'YYYY-MM-DD'
        start_date_str = start_date.strftime('%Y-%m-%d')

        # Graph stock data
        graph_stock_data(ticker, start_date_str, logger)


if __name__ == "__main__":
    main()
