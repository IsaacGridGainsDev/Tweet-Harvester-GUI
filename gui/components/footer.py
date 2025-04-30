#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Twitter Data Miner - Footer Component

This module implements the footer of the Twitter Data Miner GUI,
which displays status messages and logs.
"""

import customtkinter as ctk
from ..styles.theme import ThemeColors, ThemeSettings
from datetime import datetime

class Footer(ctk.CTkFrame):
    """
    Footer component displaying status messages and logs.
    """
    def __init__(self, master):
        super().__init__(
            master, 
            fg_color=ThemeColors.PANEL,
            corner_radius=ThemeSettings.CORNER_RADIUS,
            height=100
        )
        
        # Make the frame maintain its height
        self.pack_propagate(False)
        
        # Configure the grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text="Activity Log",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL, "bold"),
            text_color=ThemeColors.PRIMARY_TEXT
        )
        self.title_label.grid(row=0, column=0, padx=ThemeSettings.PADDING_MEDIUM, 
                             pady=(ThemeSettings.PADDING_MEDIUM, ThemeSettings.PADDING_SMALL), 
                             sticky="w")
        
        # Log text box
        self.log_textbox = ctk.CTkTextbox(
            self,
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_SMALL),
            text_color=ThemeColors.SECONDARY_TEXT,
            fg_color=ThemeColors.BACKGROUND,
            corner_radius=ThemeSettings.CORNER_RADIUS // 2,
            border_width=0,
            height=50
        )
        self.log_textbox.grid(row=1, column=0, padx=ThemeSettings.PADDING_MEDIUM, 
                            pady=(0, ThemeSettings.PADDING_MEDIUM), 
                            sticky="nsew")
        
        # Make the text box read-only
        self.log_textbox.configure(state="disabled")
        
        # Initialize with a welcome message
        self.log_message("Welcome to Twitter Data Miner!")
    
    def log_message(self, message):
        """
        Add a message to the log with a timestamp.
        
        Args:
            message: The message to log
        """
        # Get the current timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Format the log entry
        log_entry = f"[{timestamp}] {message}\n"
        
        # Enable the text box for editing
        self.log_textbox.configure(state="normal")
        
        # Insert the log entry at the end
        self.log_textbox.insert("end", log_entry)
        
        # Scroll to the end
        self.log_textbox.see("end")
        
        # Disable the text box again
        self.log_textbox.configure(state="disabled")
    
    def show_error(self, message):
        """
        Display an error message in the log.
        
        Args:
            message: The error message to display
        """
        self.log_message(f"ERROR: {message}")
    
    def show_success(self, message):
        """
        Display a success message in the log.
        
        Args:
            message: The success message to display
        """
        self.log_message(f"SUCCESS: {message}")
    
    def show_info(self, message):
        """
        Display an informational message in the log.
        
        Args:
            message: The info message to display
        """
        self.log_message(f"INFO: {message}")
    
    def update_counter(self):
        """
        Update the tweet counter in the log.
        """
        self.log_message("Received new tweet")
