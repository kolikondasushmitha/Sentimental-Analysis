import nltk
nltk.download('vader_lexicon')

import tweepy
from nltk.sentiment import SentimentIntensityAnalyzer
import re

# Twitter API credentials
API_KEY = 'dPZhGZGkZmC8M9P3PZO7XbS64'
API_SECRET = 'uCJ0TkAIXJJl3oPZhsL0pkY9pEuE06SRw0ba1jUjOz55WX7oNH'
ACCESS_TOKEN = '1864598798741458944-DiNcvy7vdu2QJzRdLX44gsWJVf9uTa'
ACCESS_TOKEN_SECRET = 'NR2m5qpQWc0SJjuo2mNXx2OXb0GYIEaturbPlQXN0jDCp'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAFB6xQEAAAAAuPWeSsktLh3HkdEzJESGQ12l1Hg%3DF6prE7UXBCB7zhV8LMjDuugOUI6xEfdguwvsu3RSuQzF9n1aiU'

# Authenticate with Twitter API
def authenticate_twitter():
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

# Clean tweets by removing URLs, mentions, hashtags, and special characters
def clean_tweet(tweet):
    tweet = re.sub(r"http\S+", "", tweet)  # Remove URLs
    tweet = re.sub(r"@\S+", "", tweet)    # Remove mentions
    tweet = re.sub(r"#\S+", "", tweet)    # Remove hashtags
    tweet = re.sub(r"[^A-Za-z0-9\s]", "", tweet)  # Remove special characters
    return tweet

# Analyze sentiment of tweets
def analyze_sentiment(api, query, max_tweets=100):
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en").items(max_tweets)
    sia = SentimentIntensityAnalyzer()
    
    sentiments = {'positive': 0, 'neutral': 0, 'negative': 0}
    total_tweets = 0

    for tweet in tweets:
        total_tweets += 1
        cleaned_tweet = clean_tweet(tweet.text)
        sentiment_score = sia.polarity_scores(cleaned_tweet)

        if sentiment_score['compound'] > 0.05:
            sentiments['positive'] += 1
        elif sentiment_score['compound'] < -0.05:
            sentiments['negative'] += 1
        else:
            sentiments['neutral'] += 1

    # Calculate percentages
    for sentiment in sentiments:
        sentiments[sentiment] = round((sentiments[sentiment] / total_tweets) * 100, 2) if total_tweets > 0 else 0
    
    return sentiments

# Main function
def main():
    api = authenticate_twitter()
    query = input("Enter a query (word/phrase): ")
    print("Fetching tweets...")
    
    try:
        sentiment_percentages = analyze_sentiment(api, query)
        print(f"Sentiment Analysis for '{query}':")
        print(f"Positive: {sentiment_percentages['positive']}%")
        print(f"Neutral: {sentiment_percentages['neutral']}%")
        print(f"Negative: {sentiment_percentages['negative']}%")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

