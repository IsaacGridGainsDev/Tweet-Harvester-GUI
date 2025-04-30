#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Twitter Data Mining Module

This module provides functionality for mining Twitter data through:
1. Historical scraping using tweepy (replacing snscrape)
2. Real-time streaming using astream
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# For historical scraping - using tweepy instead of snscrape
import tweepy

# For real-time streaming
import astream

# Prevent snscrape from being imported
import sys
sys.modules['snscrape'] = None
sys.modules['snscrape.modules'] = None
sys.modules['snscrape.modules.twitter'] = None

logger = logging.getLogger(__name__)


class TweetScraper:
    """
    A class for scraping historical tweets using tweepy (replacing snscrape).
    """
    
    def __init__(self, output_file: str = None, bearer_token: str = None):
        """
        Initialize the TweetScraper.
        
        Args:
            output_file: Path to the output JSON file. If None, defaults to 'data/tweets.json'
            bearer_token: Twitter API bearer token. If None, uses environment variable TWITTER_BEARER_TOKEN
        """
        self.output_file = output_file or os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'tweets.json')
        self._ensure_output_dir()
        
        # Initialize tweepy client
        self.bearer_token = bearer_token or os.environ.get('TWITTER_BEARER_TOKEN')
        if not self.bearer_token:
            logger.warning("No Twitter API bearer token provided. Please set TWITTER_BEARER_TOKEN environment variable.")
        else:
            self.client = tweepy.Client(bearer_token=self.bearer_token)
            
        # Store other credentials for potential use
        self.api_key = os.environ.get('API_KEY')
        self.api_key_secret = os.environ.get('API_KEY_SECRET')
        self.access_token = os.environ.get('ACCESS_TOKEN')
        self.access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
        
    def _ensure_output_dir(self):
        """
        Ensure the output directory exists.
        """
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
    
    def scrape_tweets(self, keyword: str, limit: int = 100, since: str = None, until: str = None) -> List[Dict]:
        """
        Scrape tweets based on keyword and optional date range.
        
        Args:
            keyword: The search keyword or query
            limit: Maximum number of tweets to scrape
            since: Start date in YYYY-MM-DD format
            until: End date in YYYY-MM-DD format
            
        Returns:
            List of tweet dictionaries
        """
        if not hasattr(self, 'client'):
            logger.error("Twitter API client not initialized. Please provide a bearer token.")
            return []
            
        query = keyword
        
        # Convert date strings to datetime objects
        start_time = None
        end_time = None
        
        if since:
            try:
                start_time = datetime.strptime(since, "%Y-%m-%d")
            except ValueError:
                logger.warning(f"Invalid 'since' date format: {since}. Expected YYYY-MM-DD.")
        
        if until:
            try:
                end_time = datetime.strptime(until, "%Y-%m-%d")
            except ValueError:
                logger.warning(f"Invalid 'until' date format: {until}. Expected YYYY-MM-DD.")
            
        logger.info(f"Scraping tweets with query: {query}")
        
        tweets = []
        try:
            # Using tweepy to get tweets
            # Note: Free Twitter API v2 has limitations on historical data
            response = self.client.search_recent_tweets(
                query=query,
                max_results=min(limit, 100),  # API limit is 100 per request
                start_time=start_time.isoformat() + "Z" if start_time else None,
                end_time=end_time.isoformat() + "Z" if end_time else None,
                tweet_fields=['created_at', 'lang', 'public_metrics', 'entities', 'geo', 'in_reply_to_user_id'],
                user_fields=['name', 'username', 'location', 'description', 'public_metrics'],
                expansions=['author_id', 'referenced_tweets.id', 'geo.place_id']
            )
            
            if not response.data:
                logger.info("No tweets found matching the criteria")
                return []
                
            # Process tweets and users
            users = {user.id: user for user in response.includes.get('users', [])}
            places = {place.id: place for place in response.includes.get('places', [])} if 'places' in response.includes else {}
            
            for tweet in response.data:
                user = users.get(tweet.author_id)
                place = None
                if hasattr(tweet, 'geo') and tweet.geo and 'place_id' in tweet.geo:
                    place = places.get(tweet.geo['place_id'])
                
                # Convert tweet to dictionary
                tweet_dict = {
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at.isoformat(),
                    'lang': tweet.lang,
                    'favorite_count': tweet.public_metrics.get('like_count', 0) if hasattr(tweet, 'public_metrics') else 0,
                    'favorited': tweet.public_metrics.get('like_count', 0) > 0 if hasattr(tweet, 'public_metrics') else False,
                    'retweeted': tweet.public_metrics.get('retweet_count', 0) > 0 if hasattr(tweet, 'public_metrics') else False,
                    'retweet_count': tweet.public_metrics.get('retweet_count', 0) if hasattr(tweet, 'public_metrics') else 0,
                    'user': {
                        'id': user.id if user else None,
                        'name': user.name if user else None,
                        'screen_name': user.username if user else None,
                        'location': user.location if user and hasattr(user, 'location') else None,
                        'description': user.description if user and hasattr(user, 'description') else None,
                        'followers_count': user.public_metrics.get('followers_count', 0) if user and hasattr(user, 'public_metrics') else 0,
                        'friends_count': user.public_metrics.get('following_count', 0) if user and hasattr(user, 'public_metrics') else 0
                    } if user else {},
                    'entities': {
                        'hashtags': [{'text': tag['tag']} for tag in tweet.entities.get('hashtags', [])] if hasattr(tweet, 'entities') and 'hashtags' in tweet.entities else [],
                        'user_mentions': [{'screen_name': mention['username']} for mention in tweet.entities.get('mentions', [])] if hasattr(tweet, 'entities') and 'mentions' in tweet.entities else []
                    } if hasattr(tweet, 'entities') else {},
                    'in_reply_to_user_id': tweet.in_reply_to_user_id,
                    'in_reply_to_status_id': None,  # Not directly available in v2 API
                    'place': {
                        'full_name': place.full_name if place and hasattr(place, 'full_name') else None,
                        'country': place.country if place and hasattr(place, 'country') else None,
                        'coordinates': None  # Not directly available in v2 API
                    } if place else None
                }
                
                tweets.append(tweet_dict)
                
            logger.info(f"Scraped {len(tweets)} tweets")
            
            # Save tweets to file
            self.save_tweets(tweets)
            
            return tweets
            
        except Exception as e:
            logger.error(f"Error scraping tweets: {str(e)}")
            return []
    
    def save_tweets(self, tweets: List[Dict]):
        """
        Save tweets to the output file.
        
        Args:
            tweets: List of tweet dictionaries to save
        """
        try:
            # Load existing tweets if file exists
            existing_tweets = []
            if os.path.exists(self.output_file):
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    try:
                        existing_tweets = json.load(f)
                    except json.JSONDecodeError:
                        logger.warning(f"Could not decode existing tweets file: {self.output_file}")
            
            # Combine existing and new tweets, avoiding duplicates
            existing_ids = {tweet['id'] for tweet in existing_tweets}
            unique_new_tweets = [tweet for tweet in tweets if tweet['id'] not in existing_ids]
            all_tweets = existing_tweets + unique_new_tweets
            
            # Write combined tweets to file
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(all_tweets, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Saved {len(unique_new_tweets)} new tweets to {self.output_file}")
            
        except Exception as e:
            logger.error(f"Error saving tweets: {str(e)}")


class TweetStreamer:
    """
    A class for streaming real-time tweets using astream.
    """
    
    def __init__(self, output_file: str = None, callback=None):
        """
        Initialize the TweetStreamer.
        
        Args:
            output_file: Path to the output JSON file. If None, defaults to 'data/tweets.json'
            callback: Optional callback function to process each tweet
        """
        self.output_file = output_file or os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'tweets.json')
        self._ensure_output_dir()
        self.callback = callback
        self.stream = None
        self.is_streaming = False
        
        # Load Twitter API credentials from environment variables
        self.api_key = os.environ.get('API_KEY')
        self.api_key_secret = os.environ.get('API_KEY_SECRET')
        self.access_token = os.environ.get('ACCESS_TOKEN')
        self.access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
        self.bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')
        
    def _ensure_output_dir(self):
        """
        Ensure the output directory exists.
        """
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
    
    def start_stream(self, keywords: List[str]):
        """
        Start streaming tweets based on keywords.
        
        Args:
            keywords: List of keywords to track
        """
        if self.is_streaming:
            logger.warning("Stream is already running. Stop it first.")
            return
            
        try:
            logger.info(f"Starting tweet stream with keywords: {keywords}")
            
            # Initialize the stream
            self.stream = astream.Stream()
            
            # Set up the stream with keywords
            self.stream.filter(track=keywords)
            
            # Start the stream with a callback
            self.is_streaming = True
            self.stream.sample(self._process_tweet)
            
        except Exception as e:
            logger.error(f"Error starting tweet stream: {str(e)}")
            self.is_streaming = False
    
    def stop_stream(self):
        """
        Stop the tweet stream.
        """
        if not self.is_streaming or not self.stream:
            logger.warning("No active stream to stop.")
            return
            
        try:
            logger.info("Stopping tweet stream")
            self.stream.disconnect()
            self.is_streaming = False
            
        except Exception as e:
            logger.error(f"Error stopping tweet stream: {str(e)}")
    
    def _process_tweet(self, tweet):
        """
        Process a tweet from the stream.
        
        Args:
            tweet: Tweet object from the stream
        """
        try:
            # Convert tweet to dictionary format similar to scraped tweets
            tweet_dict = {
                'id': tweet.id,
                'text': tweet.text,
                'created_at': tweet.created_at.isoformat() if hasattr(tweet, 'created_at') else datetime.now().isoformat(),
                'lang': tweet.lang if hasattr(tweet, 'lang') else None,
                'favorite_count': tweet.favorite_count if hasattr(tweet, 'favorite_count') else 0,
                'favorited': tweet.favorited if hasattr(tweet, 'favorited') else False,
                'retweeted': tweet.retweeted if hasattr(tweet, 'retweeted') else False,
                'retweet_count': tweet.retweet_count if hasattr(tweet, 'retweet_count') else 0,
                'user': {
                    'id': tweet.user.id if hasattr(tweet, 'user') else None,
                    'name': tweet.user.name if hasattr(tweet, 'user') else None,
                    'screen_name': tweet.user.screen_name if hasattr(tweet, 'user') else None,
                    'location': tweet.user.location if hasattr(tweet, 'user') else None,
                    'description': tweet.user.description if hasattr(tweet, 'user') else None,
                    'followers_count': tweet.user.followers_count if hasattr(tweet, 'user') else 0,
                    'friends_count': tweet.user.friends_count if hasattr(tweet, 'user') else 0
                } if hasattr(tweet, 'user') else {},
                'entities': {
                    'hashtags': tweet.entities.get('hashtags', []) if hasattr(tweet, 'entities') else [],
                    'user_mentions': tweet.entities.get('user_mentions', []) if hasattr(tweet, 'entities') else []
                } if hasattr(tweet, 'entities') else {},
                'in_reply_to_user_id': tweet.in_reply_to_user_id if hasattr(tweet, 'in_reply_to_user_id') else None,
                'in_reply_to_status_id': tweet.in_reply_to_status_id if hasattr(tweet, 'in_reply_to_status_id') else None,
                'place': {
                    'full_name': tweet.place.full_name if hasattr(tweet.place, 'full_name') else None,
                    'country': tweet.place.country if hasattr(tweet.place, 'country') else None,
                    'coordinates': tweet.coordinates if hasattr(tweet, 'coordinates') else None
                } if hasattr(tweet, 'place') and tweet.place else None
            }
            
            # Save the tweet
            self._save_tweet(tweet_dict)
            
            # Call the callback if provided
            if self.callback:
                self.callback(tweet_dict)
                
        except Exception as e:
            logger.error(f"Error processing tweet: {str(e)}")
    
    def _save_tweet(self, tweet: Dict):
        """
        Save a single tweet to the output file.
        
        Args:
            tweet: Tweet dictionary to save
        """
        try:
            # Load existing tweets if file exists
            existing_tweets = []
            if os.path.exists(self.output_file):
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    try:
                        existing_tweets = json.load(f)
                    except json.JSONDecodeError:
                        logger.warning(f"Could not decode existing tweets file: {self.output_file}")
            
            # Add new tweet if it doesn't exist
            existing_ids = {t['id'] for t in existing_tweets}
            if tweet['id'] not in existing_ids:
                existing_tweets.append(tweet)
                
                # Write updated tweets to file
                with open(self.output_file, 'w', encoding='utf-8') as f:
                    json.dump(existing_tweets, f, ensure_ascii=False, indent=2)
                    
        except Exception as e:
            logger.error(f"Error saving tweet: {str(e)}")