#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Twitter Data Preprocessing Module

This module provides functionality for preprocessing Twitter data including:
1. Text extraction and cleaning
2. Tokenization using NLTK
3. Stop word removal
4. Term extraction
"""

import re
import string
import logging
from typing import Dict, List, Set, Tuple, Union

# NLTK for text processing
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams

# Ensure NLTK data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

logger = logging.getLogger(__name__)


class TweetPreprocessor:
    """
    A class for preprocessing tweet data.
    """
    
    def __init__(self, language: str = 'english'):
        """
        Initialize the TweetPreprocessor.
        
        Args:
            language: Language for stop words (default: 'english')
        """
        self.language = language
        self.stop_words = set(stopwords.words(language))
        
        # Add Twitter-specific stop words
        self.stop_words.update(['rt', 'via', 'amp', '&amp;'])
    
    def extract_tweet_attributes(self, tweet: Dict) -> Dict:
        """
        Extract relevant attributes from a tweet.
        
        Args:
            tweet: Raw tweet dictionary
            
        Returns:
            Dictionary with extracted attributes
        """
        extracted = {
            'text': tweet.get('text', ''),
            'created_at': tweet.get('created_at', ''),
            'lang': tweet.get('lang', ''),
            'favorite_count': tweet.get('favorite_count', 0),
            'favorited': tweet.get('favorited', False),
            'retweeted': tweet.get('retweeted', False),
            'id': tweet.get('id', ''),
            'place': tweet.get('place', {}),
            'user': tweet.get('user', {}),
            'entities': tweet.get('entities', {}),
            'in_reply_to_user_id': tweet.get('in_reply_to_user_id'),
            'in_reply_to_status_id': tweet.get('in_reply_to_status_id')
        }
        return extracted
    
    def clean_text(self, text: str) -> str:
        """
        Clean tweet text by removing URLs, mentions, hashtags, and special characters.
        
        Args:
            text: Raw tweet text
            
        Returns:
            Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        # Remove mentions (@username)
        text = re.sub(r'@\w+', '', text)
        
        # Remove hashtags (#topic) - keep the topic text
        text = re.sub(r'#(\w+)', r'\1', text)
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words.
        
        Args:
            text: Cleaned tweet text
            
        Returns:
            List of tokens
        """
        return word_tokenize(text)
    
    def remove_stop_words(self, tokens: List[str]) -> List[str]:
        """
        Remove stop words from tokens.
        
        Args:
            tokens: List of tokens
            
        Returns:
            List of tokens without stop words
        """
        return [token for token in tokens if token.lower() not in self.stop_words]
    
    def extract_terms(self, tokens: List[str], min_length: int = 3) -> List[str]:
        """
        Extract meaningful terms from tokens.
        
        Args:
            tokens: List of tokens without stop words
            min_length: Minimum length of terms to include
            
        Returns:
            List of extracted terms
        """
        # Filter out short terms and non-alphabetic terms
        return [token for token in tokens if len(token) >= min_length and token.isalpha()]
    
    def extract_unique_terms(self, tokens: List[str]) -> Set[str]:
        """
        Extract unique terms from tokens.
        
        Args:
            tokens: List of tokens
            
        Returns:
            Set of unique terms
        """
        return set(tokens)
    
    def extract_bigrams(self, tokens: List[str]) -> List[Tuple[str, str]]:
        """
        Extract bigrams (pairs of adjacent words) from tokens.
        
        Args:
            tokens: List of tokens
            
        Returns:
            List of bigrams
        """
        return list(nltk.bigrams(tokens))
    
    def process_tweet(self, tweet: Dict) -> Dict:
        """
        Process a tweet by extracting attributes, cleaning text, and tokenizing.
        
        Args:
            tweet: Raw tweet dictionary
            
        Returns:
            Processed tweet with additional NLP attributes
        """
        try:
            # Extract attributes
            processed = self.extract_tweet_attributes(tweet)
            
            # Clean and tokenize text
            cleaned_text = self.clean_text(processed['text'])
            tokens = self.tokenize(cleaned_text)
            tokens_no_stop = self.remove_stop_words(tokens)
            terms = self.extract_terms(tokens_no_stop)
            unique_terms = self.extract_unique_terms(terms)
            bigrams = self.extract_bigrams(terms)
            
            # Add NLP attributes to processed tweet
            processed.update({
                'cleaned_text': cleaned_text,
                'tokens': tokens,
                'tokens_no_stop': tokens_no_stop,
                'terms': terms,
                'unique_terms': list(unique_terms),  # Convert set to list for JSON serialization
                'bigrams': [{'term1': bg[0], 'term2': bg[1]} for bg in bigrams]  # Convert tuples to dicts for JSON
            })
            
            return processed
            
        except Exception as e:
            logger.error(f"Error processing tweet: {str(e)}")
            return tweet  # Return original tweet if processing fails
    
    def process_tweets(self, tweets: List[Dict]) -> List[Dict]:
        """
        Process a list of tweets.
        
        Args:
            tweets: List of raw tweet dictionaries
            
        Returns:
            List of processed tweets
        """
        return [self.process_tweet(tweet) for tweet in tweets]
