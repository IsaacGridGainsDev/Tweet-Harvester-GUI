#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Twitter Data Miner - Search Input Panel

This module implements the search input panel for entering keywords
and parameters for tweet mining and streaming.
"""

import customtkinter as ctk
from ...styles.theme import ThemeColors, ThemeSettings

class SearchInputPanel(ctk.CTkFrame):
    """
    Panel for entering search keywords and parameters for tweet mining and streaming.
    """
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="transparent"
        )
        
        # Configure the grid layout
        self.grid_columnconfigure(0, weight=1)
        
        # Create the panel content
        self._create_content()
    
    def _create_content(self):
        """
        Create the panel content.
        """
        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text="Search Parameters",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_TITLE, "bold"),
            text_color=ThemeColors.PRIMARY_TEXT
        )
        self.title_label.grid(row=0, column=0, padx=0, pady=(0, ThemeSettings.PADDING_LARGE), sticky="w")
        
        # Search frame (contains all search inputs)
        self.search_frame = ctk.CTkFrame(self, fg_color=ThemeColors.BACKGROUND, corner_radius=ThemeSettings.CORNER_RADIUS)
        self.search_frame.grid(row=1, column=0, sticky="ew", pady=(0, ThemeSettings.PADDING_MEDIUM))
        self.search_frame.grid_columnconfigure(0, weight=1)
        
        # Keywords label and entry
        self.keywords_label = ctk.CTkLabel(
            self.search_frame,
            text="Keywords (comma separated):",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            text_color=ThemeColors.PRIMARY_TEXT
        )
        self.keywords_label.grid(row=0, column=0, padx=ThemeSettings.PADDING_MEDIUM, 
                                pady=(ThemeSettings.PADDING_MEDIUM, ThemeSettings.PADDING_SMALL), sticky="w")
        
        self.keywords_entry = ctk.CTkEntry(
            self.search_frame,
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            placeholder_text="Enter keywords (e.g., python, data science, AI)",
            height=ThemeSettings.BUTTON_HEIGHT
        )
        self.keywords_entry.grid(row=1, column=0, padx=ThemeSettings.PADDING_MEDIUM, 
                               pady=(0, ThemeSettings.PADDING_MEDIUM), sticky="ew")
        
        # Options frame (contains date range and limit)
        self.options_frame = ctk.CTkFrame(self, fg_color=ThemeColors.BACKGROUND, corner_radius=ThemeSettings.CORNER_RADIUS)
        self.options_frame.grid(row=2, column=0, sticky="ew", pady=(0, ThemeSettings.PADDING_MEDIUM))
        self.options_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Date range label
        self.date_label = ctk.CTkLabel(
            self.options_frame,
            text="Date Range:",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            text_color=ThemeColors.PRIMARY_TEXT
        )
        self.date_label.grid(row=0, column=0, padx=ThemeSettings.PADDING_MEDIUM, 
                           pady=(ThemeSettings.PADDING_MEDIUM, ThemeSettings.PADDING_SMALL), sticky="w")
        
        # Since date entry
        self.since_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
        self.since_frame.grid(row=1, column=0, padx=ThemeSettings.PADDING_MEDIUM, 
                            pady=(0, ThemeSettings.PADDING_SMALL), sticky="ew")
        
        self.since_label = ctk.CTkLabel(
            self.since_frame,
            text="Since:",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_SMALL),
            text_color=ThemeColors.SECONDARY_TEXT,
            width=50
        )
        self.since_label.grid(row=0, column=0, padx=(0, ThemeSettings.PADDING_SMALL))
        
        self.since_entry = ctk.CTkEntry(
            self.since_frame,
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            placeholder_text="YYYY-MM-DD",
            height=ThemeSettings.BUTTON_HEIGHT
        )
        self.since_entry.grid(row=0, column=1, sticky="ew")
        self.since_frame.grid_columnconfigure(1, weight=1)
        
        # Until date entry
        self.until_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
        self.until_frame.grid(row=1, column=1, padx=ThemeSettings.PADDING_MEDIUM, 
                            pady=(0, ThemeSettings.PADDING_SMALL), sticky="ew")
        
        self.until_label = ctk.CTkLabel(
            self.until_frame,
            text="Until:",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_SMALL),
            text_color=ThemeColors.SECONDARY_TEXT,
            width=50
        )
        self.until_label.grid(row=0, column=0, padx=(0, ThemeSettings.PADDING_SMALL))
        
        self.until_entry = ctk.CTkEntry(
            self.until_frame,
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            placeholder_text="YYYY-MM-DD",
            height=ThemeSettings.BUTTON_HEIGHT
        )
        self.until_entry.grid(row=0, column=1, sticky="ew")
        self.until_frame.grid_columnconfigure(1, weight=1)
        
        # Limit label and entry
        self.limit_label = ctk.CTkLabel(
            self.options_frame,
            text="Tweet Limit:",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            text_color=ThemeColors.PRIMARY_TEXT
        )
        self.limit_label.grid(row=2, column=0, padx=ThemeSettings.PADDING_MEDIUM, 
                            pady=(ThemeSettings.PADDING_MEDIUM, ThemeSettings.PADDING_SMALL), sticky="w")
        
        self.limit_entry = ctk.CTkEntry(
            self.options_frame,
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            placeholder_text="100",
            height=ThemeSettings.BUTTON_HEIGHT,
            width=100
        )
        self.limit_entry.grid(row=3, column=0, padx=ThemeSettings.PADDING_MEDIUM, 
                            pady=(0, ThemeSettings.PADDING_MEDIUM), sticky="w")
        self.limit_entry.insert(0, "100")  # Default value
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=3, column=0, sticky="ew", pady=(ThemeSettings.PADDING_MEDIUM, 0))
        
        # Start button
        self.start_button = ctk.CTkButton(
            self.buttons_frame,
            text="Start Mining",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            fg_color=ThemeColors.ACCENT,
            hover_color=ThemeColors.ACCENT_ALT,
            corner_radius=ThemeSettings.BUTTON_CORNER_RADIUS,
            height=ThemeSettings.BUTTON_HEIGHT,
            command=self._on_start
        )
        self.start_button.pack(side="left", padx=(0, ThemeSettings.PADDING_MEDIUM))
        
        # Cancel button
        self.cancel_button = ctk.CTkButton(
            self.buttons_frame,
            text="Cancel",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            fg_color=ThemeColors.BACKGROUND,
            text_color=ThemeColors.PRIMARY_TEXT,
            hover_color=ThemeColors.BORDER,
            corner_radius=ThemeSettings.BUTTON_CORNER_RADIUS,
            height=ThemeSettings.BUTTON_HEIGHT,
            command=self._on_cancel
        )
        self.cancel_button.pack(side="left")
    
    def _on_start(self):
        """
        Callback for the Start button.
        This is a dummy implementation that will be replaced with actual functionality.
        """
        print("Start button clicked")
        print(f"Keywords: {self.keywords_entry.get()}")
        print(f"Since: {self.since_entry.get()}")
        print(f"Until: {self.until_entry.get()}")
        print(f"Limit: {self.limit_entry.get()}")
    
    def _on_cancel(self):
        """
        Callback for the Cancel button.
        This is a dummy implementation that will be replaced with actual functionality.
        """
        print("Cancel button clicked")
        # Clear all entries
        self.keywords_entry.delete(0, "end")
        self.since_entry.delete(0, "end")
        self.until_entry.delete(0, "end")
        self.limit_entry.delete(0, "end")
        self.limit_entry.insert(0, "100")  # Reset to default value
    
    def get_params(self):
        """
        Retrieve search parameters from the input fields.
    
        Returns:
            dict: A dictionary containing keywords, date range, and tweet limit.
        """
        return {
            'keywords': self.keywords_entry.get(),
            'since': self.since_entry.get(),
            'until': self.until_entry.get(),
            'tweet_limit': int(self.limit_entry.get())
        }