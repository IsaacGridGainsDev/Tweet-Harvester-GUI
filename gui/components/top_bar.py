#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Twitter Data Miner - Top Bar Component

This module implements the top bar of the Twitter Data Miner GUI,
which displays the application name and status indicator.
"""

import customtkinter as ctk
from ..styles.theme import ThemeColors, ThemeSettings

class TopBar(ctk.CTkFrame):
    """
    Top bar component displaying the application name and status.
    """
    def __init__(self, master):
        super().__init__(
            master, 
            fg_color=ThemeColors.PANEL,
            corner_radius=ThemeSettings.CORNER_RADIUS,
            height=60
        )
        
        # Make the frame maintain its height
        self.pack_propagate(False)
        
        # Configure the grid layout
        self.grid_columnconfigure(0, weight=1)  # App name expands
        self.grid_columnconfigure(1, weight=0)  # Status indicator fixed width
        
        # App name label
        self.app_name_label = ctk.CTkLabel(
            self,
            text="Twitter Data Miner",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_TITLE, "bold"),
            text_color=ThemeColors.PRIMARY_TEXT
        )
        self.app_name_label.grid(row=0, column=0, padx=ThemeSettings.PADDING_MEDIUM, 
                                pady=ThemeSettings.PADDING_MEDIUM, sticky="w")
        
        # Status frame (contains indicator and text)
        self.status_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.status_frame.grid(row=0, column=1, padx=ThemeSettings.PADDING_MEDIUM, 
                              pady=ThemeSettings.PADDING_MEDIUM, sticky="e")
        
        # Status indicator (colored circle)
        self.status_indicator = ctk.CTkCanvas(
            self.status_frame,
            width=12,
            height=12,
            bg=ThemeColors.PANEL,
            highlightthickness=0
        )
        self.status_indicator.grid(row=0, column=0, padx=(0, 5))
        
        # Draw the initial indicator (gray circle for idle)
        self.indicator_id = self.status_indicator.create_oval(2, 2, 10, 10, fill=ThemeColors.SECONDARY_TEXT, outline="")
        
        # Status text
        self.status_text = ctk.CTkLabel(
            self.status_frame,
            text="Idle",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            text_color=ThemeColors.SECONDARY_TEXT
        )
        self.status_text.grid(row=0, column=1, padx=(0, 5))
        
        # Status color mapping
        self.status_colors = {
            "Idle": ThemeColors.SECONDARY_TEXT,
            "Mining": ThemeColors.ACCENT,
            "Streaming": ThemeColors.ACCENT_ALT,
            "Analyzing": ThemeColors.SUCCESS,
            "Visualizing": ThemeColors.SUCCESS,
            "Error": ThemeColors.ERROR
        }
    
    def set_status(self, status):
        """
        Update the status indicator and text.
        
        Args:
            status: The new status ("Idle", "Mining", "Streaming", "Analyzing", "Visualizing", "Error")
        """
        # Update the status text
        self.status_text.configure(text=status)
        
        # Get the color for the status (default to secondary text if not found)
        color = self.status_colors.get(status, ThemeColors.SECONDARY_TEXT)
        
        # Update the status text color
        self.status_text.configure(text_color=color)
        
        # Update the indicator color
        self.status_indicator.itemconfig(self.indicator_id, fill=color)