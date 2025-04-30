#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Twitter Data Analytics Module

This module provides functionality for analyzing Twitter data including:
1. Term frequency analysis
2. Co-occurrence matrix generation
3. Sentiment analysis using semantic orientation
"""

import logging
import math
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple, Union

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class TweetAnalyzer:
    """
    A class for analyzing tweet data.
    """
    
    def __init__(self):
        """
        Initialize the TweetAnalyzer.
        """
        # Default positive and negative terms for sentiment analysis
        self.positive_terms = set([
            'good', 'great', 'awesome', 'excellent', 'happy', 'love', 'best',
            'amazing', 'wonderful', 'fantastic', 'positive', 'perfect', 'nice',
            'beautiful', 'brilliant', 'enjoy', 'fun', 'glad', 'exciting', 'win'
        ])
        
        self.negative_terms = set([
            'bad', 'awful', 'terrible', 'horrible', 'sad', 'hate', 'worst',
            'poor', 'negative', 'disappointing', 'fail', 'failure', 'sucks',
            'boring', 'annoying', 'angry', 'upset', 'disaster', 'wrong', 'lose'
        ])
    
    def compute_term_frequency(self, tweets: List[Dict], top_n: int = 50) -> Dict[str, int]:
        """
        Compute the frequency of terms across all tweets.
        
        Args:
            tweets: List of processed tweet dictionaries
            top_n: Number of top terms to return
            
        Returns:
            Dictionary of terms and their frequencies
        """
        # Collect all terms from all tweets
        all_terms = []
        for tweet in tweets:
            if 'terms' in tweet:
                all_terms.extend(tweet['terms'])
        
        # Count term frequencies
        term_counter = Counter(all_terms)
        
        # Get the top N terms
        top_terms = dict(term_counter.most_common(top_n))
        
        logger.info(f"Computed frequencies for {len(top_terms)} terms")
        return top_terms
    
    def build_co_occurrence_matrix(self, tweets: List[Dict]) -> pd.DataFrame:
        """
        Build a co-occurrence matrix to track term pairings.
        
        Args:
            tweets: List of processed tweet dictionaries
            
        Returns:
            DataFrame representing the co-occurrence matrix
        """
        # Initialize co-occurrence dictionary
        co_occurrence = defaultdict(lambda: defaultdict(int))
        
        # Count co-occurrences within each tweet
        for tweet in tweets:
            if 'terms' in tweet:
                terms = tweet['terms']
                # Count each pair of terms
                for i, term1 in enumerate(terms):
                    for term2 in terms[i+1:]:
                        co_occurrence[term1][term2] += 1
                        co_occurrence[term2][term1] += 1
        
        # Convert to DataFrame
        unique_terms = sorted(set(term for tweet in tweets if 'terms' in tweet for term in tweet['terms']))
        matrix = pd.DataFrame(0, index=unique_terms, columns=unique_terms)
        
        # Fill the matrix
        for term1 in unique_terms:
            for term2 in unique_terms:
                matrix.loc[term1, term2] = co_occurrence[term1][term2]
        
        logger.info(f"Built co-occurrence matrix of size {len(unique_terms)}x{len(unique_terms)}")
        return matrix
    
    def compute_semantic_orientation(self, tweets: List[Dict], 
                                     positive_terms: Set[str] = None, 
                                     negative_terms: Set[str] = None) -> Dict[str, float]:
        """
        Compute semantic orientation scores for terms based on their co-occurrence with
        positive and negative reference terms.
        
        Args:
            tweets: List of processed tweet dictionaries
            positive_terms: Set of positive reference terms
            negative_terms: Set of negative reference terms
            
        Returns:
            Dictionary of terms and their semantic orientation scores
        """
        # Use default terms if not provided
        positive_terms = positive_terms or self.positive_terms
        negative_terms = negative_terms or self.negative_terms
        
        # Build co-occurrence matrix
        co_occurrence_matrix = self.build_co_occurrence_matrix(tweets)
        
        # Calculate semantic orientation for each term
        semantic_scores = {}
        
        for term in co_occurrence_matrix.index:
            # Skip if term is in reference sets
            if term in positive_terms or term in negative_terms:
                continue
                
            # Calculate association with positive terms
            pos_assoc = sum(co_occurrence_matrix.loc[term, pos_term] 
                           for pos_term in positive_terms if pos_term in co_occurrence_matrix.columns)
            
            # Calculate association with negative terms
            neg_assoc = sum(co_occurrence_matrix.loc[term, neg_term] 
                           for neg_term in negative_terms if neg_term in co_occurrence_matrix.columns)
            
            # Calculate semantic orientation
            # Add small epsilon to avoid division by zero
            epsilon = 0.1
            semantic_scores[term] = math.log2((pos_assoc + epsilon) / (neg_assoc + epsilon))
        
        logger.info(f"Computed semantic orientation scores for {len(semantic_scores)} terms")
        return semantic_scores
    
    def analyze_tweet_sentiment(self, tweet: Dict, semantic_scores: Dict[str, float] = None) -> float:
        """
        Analyze the sentiment of a single tweet using semantic orientation scores.
        
        Args:
            tweet: Processed tweet dictionary
            semantic_scores: Dictionary of terms and their semantic orientation scores
            
        Returns:
            Sentiment score (positive values indicate positive sentiment)
        """
        if 'terms' not in tweet or not tweet['terms']:
            return 0.0
            
        # If semantic scores not provided, use simple lexicon-based approach
        if semantic_scores is None:
            pos_count = sum(1 for term in tweet['terms'] if term in self.positive_terms)
            neg_count = sum(1 for term in tweet['terms'] if term in self.negative_terms)
            return (pos_count - neg_count) / (pos_count + neg_count + 1)  # +1 to avoid division by zero
        
        # Use semantic orientation scores
        scores = [semantic_scores.get(term, 0.0) for term in tweet['terms'] if term in semantic_scores]
        if not scores:
            return 0.0
            
        return sum(scores) / len(scores)
    
    def analyze_tweets_sentiment(self, tweets: List[Dict], semantic_scores: Dict[str, float] = None) -> List[Dict]:
        """
        Analyze the sentiment of multiple tweets.
        
        Args:
            tweets: List of processed tweet dictionaries
            semantic_scores: Dictionary of terms and their semantic orientation scores
            
        Returns:
            List of tweets with added sentiment scores
        """
        # Compute semantic scores if not provided
        if semantic_scores is None:
            semantic_scores = self.compute_semantic_orientation(tweets)
        
        # Add sentiment scores to tweets
        for tweet in tweets:
            tweet['sentiment_score'] = self.analyze_tweet_sentiment(tweet, semantic_scores)
            
            # Add sentiment label for easier categorization
            if tweet['sentiment_score'] > 0.2:
                tweet['sentiment'] = 'positive'
            elif tweet['sentiment_score'] < -0.2:
                tweet['sentiment'] = 'negative'
            else:
                tweet['sentiment'] = 'neutral'
        
        logger.info(f"Analyzed sentiment for {len(tweets)} tweets")
        return tweets
    
    def get_sentiment_distribution(self, tweets: List[Dict]) -> Dict[str, int]:
        """
        Get the distribution of sentiment labels across tweets.
        
        Args:
            tweets: List of processed tweet dictionaries with sentiment labels
            
        Returns:
            Dictionary with counts for each sentiment category
        """
        sentiments = [tweet.get('sentiment', 'unknown') for tweet in tweets]
        return dict(Counter(sentiments))
    
    def get_time_series_data(self, tweets: List[Dict], freq: str = 'H') -> pd.DataFrame:
        """
        Get time series data for tweet frequency and sentiment.
        
        Args:
            tweets: List of processed tweet dictionaries
            freq: Frequency for time series ('H' for hourly, 'D' for daily, etc.)
            
        Returns:
            DataFrame with time series data
        """
        # Convert created_at to datetime and create DataFrame
        df = pd.DataFrame(tweets)
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Set created_at as index
        df.set_index('created_at', inplace=True)
        
        # Resample by frequency
        tweet_counts = df.resample(freq).size()
        sentiment_avg = df.resample(freq)['sentiment_score'].mean()
        
        # Combine into a single DataFrame
        time_series = pd.DataFrame({
            'tweet_count': tweet_counts,
            'avg_sentiment': sentiment_avg
        })
        
        return time_series
