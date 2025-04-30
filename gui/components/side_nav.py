#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Twitter Data Miner - Side Navigation Component

This module implements the side navigation panel of the Twitter Data Miner GUI,
which provides buttons for accessing the main functionalities.
"""

import customtkinter as ctk
from ..styles.theme import ThemeColors, ThemeSettings

class SideNav(ctk.CTkFrame):
    """
    Side navigation component with buttons for the main functionalities.
    """
    def __init__(self, master, app):
        super().__init__(
            master, 
            fg_color=ThemeColors.PANEL,
            corner_radius=ThemeSettings.CORNER_RADIUS,
            width=200
        )
        
        # Store reference to the main app
        self.app = app
        
        # Make the frame maintain its width
        self.pack_propagate(False)
        
        # Configure the grid layout
        self.grid_columnconfigure(0, weight=1)
        
        # Create the navigation buttons
        self._create_buttons()
        
        # Initialize callbacks dictionary
        self.callbacks = {
            "start_mining": lambda: None,
            "start_streaming": lambda: None,
            "view_frequency": lambda: None,
            "view_matrix": lambda: None,
            "view_map": lambda: None,
            "view_orientation": lambda: None
        }
    
    def _create_buttons(self):
        """
        Create the navigation buttons.
        """
        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text="Navigation",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_LARGE, "bold"),
            text_color=ThemeColors.PRIMARY_TEXT
        )
        self.title_label.grid(row=0, column=0, padx=ThemeSettings.PADDING_MEDIUM, 
                             pady=(ThemeSettings.PADDING_MEDIUM, ThemeSettings.PADDING_LARGE), 
                             sticky="w")
        
        # Data Collection section
        self.collection_label = ctk.CTkLabel(
            self,
            text="Data Collection",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL, "bold"),
            text_color=ThemeColors.SECONDARY_TEXT
        )
        self.collection_label.grid(row=1, column=0, padx=ThemeSettings.PADDING_MEDIUM, 
                                  pady=(0, ThemeSettings.PADDING_SMALL), 
                                  sticky="w")
        
        # Start Keyword Mining button
        self.mining_button = self._create_nav_button(
            text="Start Keyword Mining",
            row=2,
            command=lambda: self.callbacks["start_mining"]()
        )
        
        # Start Real-time Streaming button
        self.streaming_button = self._create_nav_button(
            text="Start Real-time Streaming",
            row=3,
            command=lambda: self.callbacks["start_streaming"]()
        )
        
        # Analysis section
        self.analysis_label = ctk.CTkLabel(
            self,
            text="Analysis",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL, "bold"),
            text_color=ThemeColors.SECONDARY_TEXT
        )
        self.analysis_label.grid(row=4, column=0, padx=ThemeSettings.PADDING_MEDIUM, 
                               pady=(ThemeSettings.PADDING_LARGE, ThemeSettings.PADDING_SMALL), 
                               sticky="w")
        
        # View Term Frequency button
        self.frequency_button = self._create_nav_button(
            text="View Term Frequency",
            row=5,
            command=lambda: self.callbacks["view_frequency"]()
        )
        
        # Co-occurrence Matrix button
        self.matrix_button = self._create_nav_button(
            text="Co-occurrence Matrix",
            row=6,
            command=lambda: self.callbacks["view_matrix"]()
        )
        
        # Visualization section
        self.visualization_label = ctk.CTkLabel(
            self,
            text="Visualization",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL, "bold"),
            text_color=ThemeColors.SECONDARY_TEXT
        )
        self.visualization_label.grid(row=7, column=0, padx=ThemeSettings.PADDING_MEDIUM, 
                                     pady=(ThemeSettings.PADDING_LARGE, ThemeSettings.PADDING_SMALL), 
                                     sticky="w")
        
        # Map Visualization button
        self.map_button = self._create_nav_button(
            text="Map Visualization",
            row=8,
            command=lambda: self.callbacks["view_map"]()
        )
        
        # Semantic Orientation button
        self.orientation_button = self._create_nav_button(
            text="Semantic Orientation",
            row=9,
            command=lambda: self.callbacks["view_orientation"]()
        )
    
    def _create_nav_button(self, text, row, command=None):
        """
        Create a navigation button with consistent styling.
        
        Args:
            text: The button text
            row: The grid row to place the button
            command: The callback function for the button
            
        Returns:
            The created button
        """
        button = ctk.CTkButton(
            self,
            text=text,
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            fg_color=ThemeColors.BACKGROUND,
            text_color=ThemeColors.PRIMARY_TEXT,
            hover_color=ThemeColors.ACCENT,
            corner_radius=ThemeSettings.BUTTON_CORNER_RADIUS,
            height=ThemeSettings.BUTTON_HEIGHT,
            command=command
        )
        button.grid(row=row, column=0, padx=ThemeSettings.PADDING_MEDIUM, 
                   pady=ThemeSettings.PADDING_SMALL, sticky="ew")
        return button
    
    def set_callbacks(self, **callbacks):
        """
        Set the callback functions for the navigation buttons.
        
        Args:
            **callbacks: Keyword arguments for the callbacks
                (start_mining, start_streaming, view_frequency, view_matrix, view_map, view_orientation)
        """
        # Update the callbacks dictionary with the provided callbacks
        for key, callback in callbacks.items():
            if key in self.callbacks:
                self.callbacks[key] = callback