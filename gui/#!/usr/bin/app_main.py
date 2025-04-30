#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Twitter Data Miner - Main Application

This is the main entry point for the Twitter Data Miner GUI application.
It initializes the root window and manages the top-level frames.
"""

import os
import sys
import customtkinter as ctk
from gui.styles.theme import ThemeColors, ThemeSettings, setup_theme  # Modified import path

# Import components
from gui.components.top_bar import TopBar
from gui.components.side_nav import SideNav
from gui.components.main_view import MainView
from gui.components.footer import Footer
from mining.data_mining_new import TweetScraper, TweetStreamer
from gui.components.footer import Footer

class TwitterMinerApp(ctk.CTk):
    """
    Main application class for the Twitter Data Miner GUI.
    """
    def __init__(self):
        super().__init__()
        
        # Initialize mining components
        self.scraper = TweetScraper()
        self.streamer = TweetStreamer(callback=self.handle_new_tweet)
        
        # Setup UI components
        self.top_bar = TopBar(self)
        self.side_nav = SideNav(self, self)
        self.main_view = MainView(self)
        self.footer = Footer(self)
        
        # Configure layout
        self._setup_layout()
        
        # Set initial state
        self.running_process = None
        self._bind_callbacks()

    def _setup_layout(self):
        """Set up the grid layout for main application."""
        self.grid_columnconfigure(0, weight=0)  # Side nav
        self.grid_columnconfigure(1, weight=1)   # Main content
        self.grid_rowconfigure(1, weight=1)     # Main content row
        
        # Place components
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.side_nav.grid(row=1, column=0, sticky="nsew")
        self.main_view.grid(row=1, column=1, sticky="nsew")
        self.footer.grid(row=2, column=0, columnspan=2, sticky="nsew")

    def _bind_callbacks(self):
        """Bind navigation callbacks to mining operations."""
        self.side_nav.set_callbacks(
            start_mining=self.start_historical_mining,
            start_streaming=self.start_realtime_streaming
        )

    def start_historical_mining(self):
        """Handle historical mining button click."""
        try:
            self.top_bar.set_status("Mining")
            params = self.main_view.panels["search_input"].get_params()
            
            # Run in background to prevent UI freeze
            self.after(100, lambda: self._execute_historical_mining(
                params["keywords"],
                params["tweet_limit"],
                params["since"],
                params["until"]
            ))
        
        except Exception as e:
            self.top_bar.set_status("Error")
            self.footer.show_error(f"Mining failed: {str(e)}")

    def _execute_historical_mining(self, keywords, limit, since, until):
        """Execute historical mining with progress tracking."""
        try:
            results = self.scraper.scrape_tweets(
                keyword=keywords,
                limit=limit,
                since=since,
                until=until
            )
            self.footer.show_success(f"Mined {len(results)} tweets")
            self.top_bar.set_status("Idle")
        
        except Exception as e:
            self.top_bar.set_status("Error")
            self.footer.show_error(f"Mining error: {str(e)}")

    def start_realtime_streaming(self):
        """Handle real-time streaming button click."""
        try:
            if self.streamer.is_streaming:
                self.streamer.stop_stream()
                self.top_bar.set_status("Idle")
            else:
                keywords = self.main_view.panels["search_input"].get_params()["keywords"]
                self.streamer.start_stream(keywords.split(','))
                self.top_bar.set_status("Streaming")
                self.footer.show_info("Streaming started - click again to stop")
        
        except Exception as e:
            self.top_bar.set_status("Error")
            self.footer.show_error(f"Streaming error: {str(e)}")

    def handle_new_tweet(self, tweet):
        """Handle new tweet from streamer callback."""
        self.footer.update_counter()
        self.main_view.panels["chart_viewer"].add_data_point(tweet)
    
    # This method has been removed as it was a duplicate
    
    def _setup_callbacks(self):
        """
        Set up callback functions for the UI components.
        """
        # Set up additional callbacks for analysis and visualization features
        self.side_nav.set_callbacks(
            start_mining=self.start_historical_mining,
            start_streaming=self.start_realtime_streaming,
            view_frequency=self.view_frequency,
            view_matrix=self.view_matrix,
            view_map=self.view_map,
            view_orientation=self.view_orientation
        )

    def view_frequency(self):
        """Handle view frequency button click."""
        self.top_bar.set_status("Analyzing")
        # Add actual analysis call here
        # Placeholder for actual implementation
        self.main_view.show_panel("chart_viewer")
        self.footer.show_info("Displaying term frequency analysis...")

    def view_matrix(self):
        """Handle view matrix button click."""
        self.top_bar.set_status("Analyzing")
        self.footer.show_info("Loading co-occurrence matrix...")
        self.main_view.show_panel("matrix")
    
    def view_map(self):
        """Handle view map button click."""
        self.top_bar.set_status("Visualizing")
        self.footer.show_info("Loading geolocation map...")
        self.main_view.show_panel("map")
    
    def view_orientation(self):
        """Handle view orientation button click."""
        self.top_bar.set_status("Analyzing")
        self.footer.show_info("Loading semantic orientation analysis...")
        self.main_view.show_panel("orientation_analyzer")


def main():
    """
    Main entry point for the application.
    """
    app = TwitterMinerApp()
    app.mainloop()


if __name__ == "__main__":
    # Add the parent directory to sys.path if running the file directly
    if __package__ is None:
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, parent_dir)
    
    main()
