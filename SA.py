import re
import tweepy
from textblob import TextBlob

class TwitterClient:
    '''
    Generic Twitter Class for sentiment analysis using Twitter API v2.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # Replace with your own Bearer Token from the Twitter Developer Portal
        bearer_token = "AAAAAAAAAAAAAAAAAAAAAFB6xQEAAAAAXYAyULRCLP9B7b2E3KVHugNwTok%3D0qFNUCjObuoHMpsDkvt3ipykIBE1hEdJki3GOazg4zl1wdolet"

        try:
            self.client = tweepy.Client(bearer_token=bearer_token)
        except tweepy.errors.TweepyException as e:
            print(f"Error: Authentication Failed - {str(e)}")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub(r"(@\w+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them using Twitter API v2.
        '''
        tweets = []

        try:
            response = self.client.search_recent_tweets(
                query=query, max_results=min(count, 100), tweet_fields=['text']
            )

            if not response.data:
                print("No tweets found for the query.")
                return tweets

            for tweet in response.data:
                parsed_tweet = {
                    'text': tweet.text,
                    'sentiment': self.get_tweet_sentiment(tweet.text)
                }
                tweets.append(parsed_tweet)

            return tweets

        except tweepy.errors.TweepyException as e:
            print(f"Error: {str(e)}")
            return []

def main():
    # Create an object of the TwitterClient class
    api = TwitterClient()

    # Fetch tweets
    query = "@AI"
    tweets = api.get_tweets(query=query, count=1000)

    if not tweets:
        print("No tweets fetched. Please check your query or API limits.")
        return

    # Classify tweets by sentiment
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    # Calculate percentages
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    print("Neutral tweets percentage: {} %".format(
        100 * (len(tweets) - len(ptweets) - len(ntweets)) / len(tweets)
    ))

    # Display some tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:5]:
        print(tweet['text'])

    print("\n\nNegative tweets:")
    for tweet in ntweets[:5]:
        print(tweet['text'])

if __name__ == "__main__":
    main()

