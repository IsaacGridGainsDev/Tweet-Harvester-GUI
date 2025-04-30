#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Twitter Data Miner - Remaining View Panels

This module implements the remaining view panels for the Twitter Data Miner GUI:
- Matrix Panel: For displaying co-occurrence matrix
- Map Panel: For displaying geolocation visualization
- Orientation Analyzer Panel: For displaying semantic orientation analysis
"""

import customtkinter as ctk
from ...styles.theme import ThemeColors, ThemeSettings


class MatrixPanel(ctk.CTkFrame):
    """
    Panel for displaying co-occurrence matrix visualization.
    """
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="transparent"
        )
        
        # Configure the grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Make the matrix area expandable
        
        # Create the panel content
        self._create_content()
    
    def _create_content(self):
        """
        Create the panel content.
        """
        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text="Co-occurrence Matrix",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_TITLE, "bold"),
            text_color=ThemeColors.PRIMARY_TEXT
        )
        self.title_label.grid(row=0, column=0, padx=0, pady=(0, ThemeSettings.PADDING_MEDIUM), sticky="w")
        
        # Matrix frame (placeholder for the actual matrix visualization)
        self.matrix_frame = ctk.CTkFrame(
            self, 
            fg_color=ThemeColors.BACKGROUND,
            corner_radius=ThemeSettings.CORNER_RADIUS
        )
        self.matrix_frame.grid(row=1, column=0, sticky="nsew", pady=(0, ThemeSettings.PADDING_MEDIUM))
        
        # Placeholder label for the matrix
        self.placeholder_label = ctk.CTkLabel(
            self.matrix_frame,
            text="Co-occurrence Matrix Visualization\n(Matrix will appear here)",
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
        
        # Term count slider
        self.terms_label = ctk.CTkLabel(
            self.controls_frame,
            text="Number of terms:",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            text_color=ThemeColors.PRIMARY_TEXT
        )
        self.terms_label.pack(side="left", padx=ThemeSettings.PADDING_MEDIUM, pady=ThemeSettings.PADDING_MEDIUM)
        
        self.terms_slider = ctk.CTkSlider(
            self.controls_frame,
            from_=5,
            to=30,
            number_of_steps=5,
            width=200
        )
        self.terms_slider.pack(side="left", padx=ThemeSettings.PADDING_SMALL, pady=ThemeSettings.PADDING_MEDIUM)
        self.terms_slider.set(10)  # Default value
        
        self.terms_value_label = ctk.CTkLabel(
            self.controls_frame,
            text="10",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            text_color=ThemeColors.PRIMARY_TEXT,
            width=30
        )
        self.terms_value_label.pack(side="left", padx=(0, ThemeSettings.PADDING_MEDIUM), pady=ThemeSettings.PADDING_MEDIUM)
        
        # Update button
        self.update_button = ctk.CTkButton(
            self.controls_frame,
            text="Generate Matrix",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            fg_color=ThemeColors.ACCENT,
            hover_color=ThemeColors.ACCENT_ALT,
            corner_radius=ThemeSettings.BUTTON_CORNER_RADIUS,
            height=ThemeSettings.BUTTON_HEIGHT,
            command=self._on_update
        )
        self.update_button.pack(side="right", padx=ThemeSettings.PADDING_MEDIUM, pady=ThemeSettings.PADDING_MEDIUM)
        
        # Bind the slider to update the value label
        self.terms_slider.configure(command=self._on_slider_change)
    
    def _on_slider_change(self, value):
        """
        Update the value label when the slider changes.
        
        Args:
            value: The new slider value
        """
        # Round to the nearest 5
        rounded_value = round(value / 5) * 5
        if rounded_value < 5:
            rounded_value = 5
        
        # Update the value label
        self.terms_value_label.configure(text=str(rounded_value))
    
    def _on_update(self):
        """
        Callback for the Generate Matrix button.
        This is a dummy implementation that will be replaced with actual functionality.
        """
        print("Generate Matrix button clicked")
        print(f"Number of terms: {self.terms_value_label.cget('text')}")


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


class OrientationAnalyzerPanel(ctk.CTkFrame):
    """
    Panel for displaying semantic orientation analysis.
    """
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="transparent"
        )
        
        # Configure the grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Make the chart area expandable
        
        # Create the panel content
        self._create_content()
    
    def _create_content(self):
        """
        Create the panel content.
        """
        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text="Semantic Orientation Analysis",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_TITLE, "bold"),
            text_color=ThemeColors.PRIMARY_TEXT
        )
        self.title_label.grid(row=0, column=0, padx=0, pady=(0, ThemeSettings.PADDING_MEDIUM), sticky="w")
        
        # Chart frame (placeholder for the actual chart)
        self.chart_frame = ctk.CTkFrame(
            self, 
            fg_color=ThemeColors.BACKGROUND,
            corner_radius=ThemeSettings.CORNER_RADIUS
        )
        self.chart_frame.grid(row=1, column=0, sticky="nsew", pady=(0, ThemeSettings.PADDING_MEDIUM))
        
        # Placeholder label for the chart
        self.placeholder_label = ctk.CTkLabel(
            self.chart_frame,
            text="Sentiment Analysis Chart\n(Visualization will appear here)",
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
        
        # Visualization type
        self.viz_type_label = ctk.CTkLabel(
            self.controls_frame,
            text="Visualization Type:",
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            text_color=ThemeColors.PRIMARY_TEXT
        )
        self.viz_type_label.pack(side="left", padx=ThemeSettings.PADDING_MEDIUM, pady=ThemeSettings.PADDING_MEDIUM)
        
        self.viz_type_var = ctk.StringVar(value="Pie Chart")
        self.viz_type_dropdown = ctk.CTkOptionMenu(
            self.controls_frame,
            values=["Pie Chart", "Bar Chart", "Time Series"],
            variable=self.viz_type_var,
            font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            dropdown_font=(ThemeSettings.FONT_FAMILY, ThemeSettings.FONT_SIZE_NORMAL),
            fg_color=ThemeColors.ACCENT,
            button_color=ThemeColors.ACCENT,
            button_hover_color=ThemeColors.ACCENT_ALT,
            dropdown_hover_color=ThemeColors.ACCENT_ALT
        )
        self.viz_type_dropdown.pack(side="left", padx=(0, ThemeSettings.PADDING_MEDIUM), pady=ThemeSettings.PADDING_MEDIUM)
        
        # Update button
        self.update_button = ctk.CTkButton(
            self.controls_frame,
            text="Generate Analysis",
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
        Callback for the Generate Analysis button.
        This is a dummy implementation that will be replaced with actual functionality.
        """
        print("Generate Analysis button clicked")
        print(f"Visualization type: {self.viz_type_var.get()}")