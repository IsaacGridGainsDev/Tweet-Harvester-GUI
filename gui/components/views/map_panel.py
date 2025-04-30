#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Twitter Data Miner - Map Panel

This module implements the map panel for displaying geolocation map visualization.
"""

import customtkinter as ctk
from ...styles.theme import ThemeColors, ThemeSettings

class MapPanel(ctk.CTkFrame):
    """
    Panel for displaying geolocation map visualization.
    """
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="transparent"
        )
        
        # Configure the grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Make the map area expandable
        
        # Create the panel content
        self._create_content()
    
    def _create_content(self):
        """
        Create the panel content.
        """
        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text="Geolocation Map Visualization",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_TITLE, "bold"),
            text_color=ThemeColors.PRIMARY_TEXT
        )
        self.title_label.grid(row=0, column=0, padx=0, pady=(0, ThemeSettings.PADDING_MEDIUM), sticky="w")
        
        # Map frame (placeholder for the actual map)
        self.map_frame = ctk.CTkFrame(
            self, 
            fg_color=ThemeColors.BACKGROUND,
            corner_radius=ThemeSettings.CORNER_RADIUS
        )
        self.map_frame.grid(row=1, column=0, sticky="nsew", pady=(0, ThemeSettings.PADDING_MEDIUM))
        
        # Placeholder label for the map
        self.placeholder_label = ctk.CTkLabel(
            self.map_frame,
            text="Geolocation Map\n(Map will appear here)",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_LARGE),
            text_color=ThemeColors.SECONDARY_TEXT
        )
        self.placeholder_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Controls frame
        self.controls_frame = ctk.CTkFrame(
            self, 
            fg_color=ThemeColors.BACKGROUND,
            corner_radius=ThemeSettings.CORNER_RADIUS
        )
        self.controls_frame.grid(row=2, column=0, sticky="ew")
        
        # Map type dropdown
        self.map_type_label = ctk.CTkLabel(
            self.controls_frame,
            text="Map Type:",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            text_color=ThemeColors.PRIMARY_TEXT
        )
        self.map_type_label.pack(side="left", padx=ThemeSettings.PADDING_MEDIUM, pady=ThemeSettings.PADDING_MEDIUM)
        
        self.map_type_var = ctk.StringVar(value="Heatmap")
        self.map_type_dropdown = ctk.CTkOptionMenu(
            self.controls_frame,
            values=["Heatmap", "Markers", "Choropleth"],
            variable=self.map_type_var,
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            dropdown_font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            fg_color=ThemeColors.ACCENT,
            button_color=ThemeColors.ACCENT,
            button_hover_color=ThemeColors.ACCENT_ALT,
            dropdown_hover_color=ThemeColors.ACCENT_ALT
        )
        self.map_type_dropdown.pack(side="left", padx=(0, ThemeSettings.PADDING_MEDIUM), pady=ThemeSettings.PADDING_MEDIUM)
        
        # Update button
        self.update_button = ctk.CTkButton(
            self.controls_frame,
            text="Generate Map",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            fg_color=ThemeColors.ACCENT,
            hover_color=ThemeColors.ACCENT_ALT,
            corner_radius=ThemeSettings.BUTTON_CORNER_RADIUS,
            height=ThemeSettings.BUTTON_HEIGHT,
            command=self._on_update
        )
        self.update_button.pack(side="right", padx=ThemeSettings.PADDING_MEDIUM, pady=ThemeSettings.PADDING_MEDIUM)
    
    def _on_update(self):
        """
        Callback for the Generate Map button.
        This is a dummy implementation that will be replaced with actual functionality.
        """
        print("Generate Map button clicked")
        print(f"Map type: {self.map_type_var.get()}")