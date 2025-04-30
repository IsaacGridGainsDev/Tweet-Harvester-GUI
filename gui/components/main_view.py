#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Twitter Data Miner - Main View Component

This module implements the main view area of the Twitter Data Miner GUI,
which dynamically displays different panels based on user selection.
"""

import customtkinter as ctk
from ..styles.theme import ThemeColors, ThemeSettings

# Import view panels
from .views.search_input_panel import SearchInputPanel
from .views.chart_viewer_panel import ChartViewerPanel
from .views.matrix_panel import MatrixPanel
from .views.map_panel import MapPanel
from .views.orientation_analyzer_panel import OrientationAnalyzerPanel

class MainView(ctk.CTkFrame):
    """
    Main view component that displays different panels based on user selection.
    """
    def __init__(self, master):
        super().__init__(
            master, 
            fg_color=ThemeColors.PANEL,
            corner_radius=ThemeSettings.CORNER_RADIUS
        )
        
        # Configure the grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Initialize panels dictionary
        self.panels = {}
        
        # Create all panels
        self._create_panels()
        
        # Show the default panel (search input)
        self.show_panel("search_input")
    
    def _create_panels(self):
        """
        Create all panels that can be displayed in the main view.
        """
        # Search Input Panel
        self.panels["search_input"] = SearchInputPanel(self)
        
        # Chart Viewer Panel
        self.panels["chart_viewer"] = ChartViewerPanel(self)
        
        # Matrix Panel
        self.panels["matrix"] = MatrixPanel(self)
        
        # Map Panel
        self.panels["map"] = MapPanel(self)
        
        # Orientation Analyzer Panel
        self.panels["orientation_analyzer"] = OrientationAnalyzerPanel(self)
        
        # Place all panels in the same grid cell but only show one at a time
        for panel in self.panels.values():
            panel.grid(row=0, column=0, sticky="nsew", padx=ThemeSettings.PADDING_MEDIUM, 
                      pady=ThemeSettings.PADDING_MEDIUM)
            panel.grid_remove()  # Hide all panels initially
    
    def show_panel(self, panel_name):
        """
        Show the specified panel and hide all others.
        
        Args:
            panel_name: The name of the panel to show
        """
        if panel_name in self.panels:
            # Hide all panels
            for name, panel in self.panels.items():
                panel.grid_remove()
            
            # Show the selected panel
            self.panels[panel_name].grid()
        else:
            print(f"Panel '{panel_name}' not found")