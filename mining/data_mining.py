#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Twitter Data Mining Module

This module provides functionality for mining Twitter data through:
1. Historical scraping using snscrape
2. Real-time streaming using astream
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Union

# For historical scraping
import snscrape.modules.twitter as sntwitter

# For real-time streaming
import astream

logger = logging.getLogger(__name__)


class TweetScraper:
    """
    A class for scraping historical tweets using snscrape.
    """
    
    def __init__(self, output_file: str = None):
        """
        Initialize the TweetScraper.
        
        Args:
            output_file: Path to the output JSON file. If None, defaults to 'data/tweets.json'
        """
        self.output_file = output_file or os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'tweets.json')
        self._ensure_output_dir()
        
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
        query = keyword
        
        # Add date range to query if provided
        if since:
            query += f" since:{since}"
        if until:
            query += f" until:{until}"
            
        logger.info(f"Scraping tweets with query: {query}")
        
        tweets = []
        try:
            # Using snscrape to get tweets
            for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
                if i >= limit:
                    break
                    
                # Convert tweet to dictionary
                tweet_dict = {
                    'id': tweet.id,
                    'text': tweet.content,
                    'created_at': tweet.date.isoformat(),
                    'lang': tweet.lang,
                    'favorite_count': tweet.likeCount,
                    'favorited': tweet.likeCount > 0,
                    'retweeted': tweet.retweetCount > 0,
                    'retweet_count': tweet.retweetCount,
                    'user': {
                        'id': tweet.user.id,
                        'name': tweet.user.displayname,
                        'screen_name': tweet.user.username,
                        'location': tweet.user.location,
                        'description': tweet.user.description,
                        'followers_count': tweet.user.followersCount,
                        'friends_count': tweet.user.friendsCount
                    },
                    'entities': {
                        'hashtags': [{'text': hashtag} for hashtag in tweet.hashtags] if tweet.hashtags else [],
                        'user_mentions': [{'screen_name': mention} for mention in tweet.mentionedUsers] if tweet.mentionedUsers else []
                    },
                    'in_reply_to_user_id': tweet.inReplyToUser.id if tweet.inReplyToUser else None,
                    'in_reply_to_status_id': tweet.inReplyToTweetId,
                    'place': {
                        'full_name': tweet.place.fullName if tweet.place else None,
                        'country': tweet.place.country if tweet.place else None,
                        'coordinates': tweet.coordinates
                    } if tweet.place else None
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