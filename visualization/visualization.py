#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Twitter Data Visualization Module

This module provides functionality for visualizing Twitter data including:
1. Bar charts of frequent terms using Vincent
2. Time series charts using Pandas
3. Geolocation maps using Folium
"""

import os
import json
import logging
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd
import matplotlib.pyplot as plt
import vincent
import folium
from folium.plugins import MarkerCluster

logger = logging.getLogger(__name__)


class TweetVisualizer:
    """
    A class for visualizing tweet data.
    """
    
    def __init__(self, output_dir: str = None):
        """
        Initialize the TweetVisualizer.
        
        Args:
            output_dir: Directory to save visualizations. If None, defaults to 'data'
        """
        self.output_dir = output_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """
        Ensure the output directory exists.
        """
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_term_frequency_chart(self, term_freq: Dict[str, int], top_n: int = 20, 
                                   title: str = 'Top Terms Frequency', 
                                   save_path: str = None) -> vincent.Chart:
        """
        Create a bar chart of term frequencies using Vincent (D3.js-based).
        
        Args:
            term_freq: Dictionary of terms and their frequencies
            top_n: Number of top terms to include
            title: Chart title
            save_path: Path to save the chart JSON. If None, uses default path
            
        Returns:
            Vincent chart object
        """
        # Sort and get top N terms
        sorted_terms = sorted(term_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
        labels = [term for term, _ in sorted_terms]
        values = [freq for _, freq in sorted_terms]
        
        # Create DataFrame for Vincent
        df = pd.DataFrame({
            'Term': labels,
            'Frequency': values
        })
        
        # Create Vincent bar chart
        chart = vincent.Bar(df, height=300, width=700)
        chart.axis_titles(x='Term', y='Frequency')
        chart.legend(title=title)
        
        # Save chart to file if path provided
        if save_path is None:
            save_path = os.path.join(self.output_dir, 'term_frequency_chart.json')
            
        chart.to_json(save_path)
        logger.info(f"Term frequency chart saved to {save_path}")
        
        return chart
    
    def create_time_series_chart(self, time_series_data: pd.DataFrame, 
                                title: str = 'Tweet Activity Over Time',
                                save_path: str = None) -> plt.Figure:
        """
        Create a time series chart using Pandas and Matplotlib.
        
        Args:
            time_series_data: DataFrame with time series data
            title: Chart title
            save_path: Path to save the chart. If None, uses default path
            
        Returns:
            Matplotlib figure
        """
        # Create figure and axes
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # Plot tweet count
        color = 'tab:blue'
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Tweet Count', color=color)
        ax1.plot(time_series_data.index, time_series_data['tweet_count'], color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        
        # Create second y-axis for sentiment
        if 'avg_sentiment' in time_series_data.columns:
            ax2 = ax1.twinx()
            color = 'tab:red'
            ax2.set_ylabel('Average Sentiment', color=color)
            ax2.plot(time_series_data.index, time_series_data['avg_sentiment'], color=color)
            ax2.tick_params(axis='y', labelcolor=color)
        
        # Set title and layout
        plt.title(title)
        fig.tight_layout()
        
        # Save chart to file if path provided
        if save_path is None:
            save_path = os.path.join(self.output_dir, 'time_series_chart.png')
            
        plt.savefig(save_path)
        logger.info(f"Time series chart saved to {save_path}")
        
        return fig
    
    def create_geolocation_map(self, tweets: List[Dict], 
                              title: str = 'Tweet Locations',
                              save_path: str = None) -> folium.Map:
        """
        Create an interactive map of tweet locations using Folium (Leaflet.js-based).
        
        Args:
            tweets: List of processed tweet dictionaries
            title: Map title
            save_path: Path to save the HTML map. If None, uses default path
            
        Returns:
            Folium map object
        """
        # Create a base map centered at (0, 0) with zoom level 2
        map_obj = folium.Map(location=[0, 0], zoom_start=2, tiles='OpenStreetMap')
        
        # Add title
        title_html = f'<h3 align="center" style="font-size:16px">{title}</h3>'
        map_obj.get_root().html.add_child(folium.Element(title_html))
        
        # Create a marker cluster for better performance with many points
        marker_cluster = MarkerCluster().add_to(map_obj)
        
        # Add markers for tweets with location data
        locations_added = 0
        
        for tweet in tweets:
            # Check if tweet has place data with coordinates
            if tweet.get('place') and tweet['place'].get('coordinates'):
                coords = tweet['place']['coordinates']
                if coords and isinstance(coords, list) and len(coords) == 2:
                    lat, lon = coords
                    
                    # Create popup content
                    popup_content = f"<b>@{tweet['user'].get('screen_name', 'unknown')}</b><br>"
                    popup_content += f"{tweet.get('text', '')[:100]}...<br>"
                    popup_content += f"Sentiment: {tweet.get('sentiment', 'unknown')}"
                    
                    # Add marker to cluster
                    folium.Marker(
                        location=[lat, lon],
                        popup=folium.Popup(popup_content, max_width=300),
                        icon=folium.Icon(color=self._get_sentiment_color(tweet.get('sentiment_score', 0)))
                    ).add_to(marker_cluster)
                    
                    locations_added += 1
            
            # Alternative: check user location field
            elif not locations_added and tweet.get('user', {}).get('location'):
                # Note: This would require geocoding the location string to coordinates
                # which is not implemented here but could be added with a geocoding service
                pass
        
        # Save map to file if path provided
        if save_path is None:
            save_path = os.path.join(self.output_dir, 'tweet_locations_map.html')
            
        map_obj.save(save_path)
        logger.info(f"Geolocation map saved to {save_path} with {locations_added} locations")
        
        return map_obj
    
    def _get_sentiment_color(self, sentiment_score: float) -> str:
        """
        Get color based on sentiment score.
        
        Args:
            sentiment_score: Sentiment score
            
        Returns:
            Color string for map marker
        """
        if sentiment_score > 0.2:
            return 'green'
        elif sentiment_score < -0.2:
            return 'red'
        else:
            return 'blue'
    
    def create_word_cloud(self, term_freq: Dict[str, int], 
                         title: str = 'Term Word Cloud',
                         save_path: str = None) -> plt.Figure:
        """
        Create a word cloud visualization of term frequencies.
        
        Args:
            term_freq: Dictionary of terms and their frequencies
            title: Chart title
            save_path: Path to save the word cloud. If None, uses default path
            
        Returns:
            Matplotlib figure
        """
        try:
            from wordcloud import WordCloud
            
            # Create figure
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Generate word cloud
            wordcloud = WordCloud(width=800, height=600, background_color='white',
                                 max_words=100, contour_width=3, contour_color='steelblue')
            wordcloud.generate_from_frequencies(term_freq)
            
            # Display word cloud
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.set_title(title)
            ax.axis('off')
            
            # Save word cloud to file if path provided
            if save_path is None:
                save_path = os.path.join(self.output_dir, 'word_cloud.png')
                
            plt.savefig(save_path)
            logger.info(f"Word cloud saved to {save_path}")
            
            return fig
            
        except ImportError:
            logger.warning("WordCloud package not installed. Install with 'pip install wordcloud'")
            return None
    
    def create_sentiment_distribution_chart(self, sentiment_dist: Dict[str, int],
                                           title: str = 'Sentiment Distribution',
                                           save_path: str = None) -> plt.Figure:
        """
        Create a pie chart of sentiment distribution.
        
        Args:
            sentiment_dist: Dictionary of sentiment categories and their counts
            title: Chart title
            save_path: Path to save the chart. If None, uses default path
            
        Returns:
            Matplotlib figure
        """
        # Create figure and axes
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Define colors for sentiment categories
        colors = {
            'positive': 'green',
            'neutral': 'gray',
            'negative': 'red',
            'unknown': 'lightgray'
        }
        
        # Extract labels and values
        labels = list(sentiment_dist.keys())
        values = list(sentiment_dist.values())
        chart_colors = [colors.get(label, 'blue') for label in labels]
        
        # Create pie chart
        ax.pie(values, labels=labels, colors=chart_colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        # Set title
        plt.title(title)
        
        # Save chart to file if path provided
        if save_path is None:
            save_path = os.path.join(self.output_dir, 'sentiment_distribution.png')
            
        plt.savefig(save_path)
        logger.info(f"Sentiment distribution chart saved to {save_path}")
        
        return fig
