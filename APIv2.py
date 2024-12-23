import nltk
nltk.download('vader_lexicon')

import tweepy
from nltk.sentiment import SentimentIntensityAnalyzer
import re

# Twitter API credentials
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAFB6xQEAAAAAWU7lSWL2fsmm5qE%2BTmHeErtKSME%3DlsBeRrJctJ45GhUdEJhJEj0Ciuq0GXaPG6z3CjpWN1vhP8myHI'

# Authenticate with Twitter API v2
def authenticate_twitter_v2():
    client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)
    return client

# Clean tweets by removing URLs, mentions, hashtags, and special characters
def clean_tweet(tweet):
    tweet = re.sub(r"http\S+", "", tweet)  # Remove URLs
    tweet = re.sub(r"@\S+", "", tweet)    # Remove mentions
    tweet = re.sub(r"#\S+", "", tweet)    # Remove hashtags
    tweet = re.sub(r"[^A-Za-z0-9\s]", "", tweet)  # Remove special characters
    return tweet

# Analyze sentiment of tweets
def analyze_sentiment(client, query, max_tweets=100):
    response = client.search_recent_tweets(query=query, max_results=min(max_tweets, 100), tweet_fields=["text", "lang"])
    tweets = [tweet.text for tweet in response.data if tweet.lang == "en"]

    sia = SentimentIntensityAnalyzer()
    sentiments = {'positive': 0, 'neutral': 0, 'negative': 0}

    for tweet in tweets:
        cleaned_tweet = clean_tweet(tweet)
        sentiment_score = sia.polarity_scores(cleaned_tweet)

        if sentiment_score['compound'] > 0.05:
            sentiments['positive'] += 1
        elif sentiment_score['compound'] < -0.05:
            sentiments['negative'] += 1
        else:
            sentiments['neutral'] += 1

    total_tweets = len(tweets)
    if total_tweets > 0:
        for sentiment in sentiments:
            sentiments[sentiment] = round((sentiments[sentiment] / total_tweets) * 100, 2)
    return sentiments

# Main function
def main():
    client = authenticate_twitter_v2()
    query = input("Enter a query (word/phrase): ")
    print("Fetching tweets...")
    
    try:
        sentiment_percentages = analyze_sentiment(client, query)
        print(f"Sentiment Analysis for '{query}':")
        print(f"Positive: {sentiment_percentages['positive']}%")
        print(f"Neutral: {sentiment_percentages['neutral']}%")
        print(f"Negative: {sentiment_percentages['negative']}%")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
