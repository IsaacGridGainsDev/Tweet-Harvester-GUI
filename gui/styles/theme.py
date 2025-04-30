#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Twitter Data Miner - Theme Configuration

This module defines the global theme settings for the Twitter Data Miner GUI.
"""

class ThemeColors:
    """
    Color palette for the Twitter Data Miner GUI.
    """
    BACKGROUND = "#F0F0F5"  # Light background
    PANEL = "#FFFFFF"       # White panel/container
    PRIMARY_TEXT = "#1C1C1E"  # Dark text
    ACCENT = "#0A84FF"      # Blue accent
    ACCENT_ALT = "#3B82F6"  # Alternative blue accent
    SUCCESS = "#34C759"    # Green for success messages
    ERROR = "#FF3B30"      # Red for error messages
    SECONDARY_TEXT = "#6E6E73"  # Gray for secondary text
    BORDER = "#E5E5EA"     # Light border color


class ThemeSettings:
    """
    General theme settings for the Twitter Data Miner GUI.
    """
    CORNER_RADIUS = 12      # Rounded corners (10-16px)
    BUTTON_CORNER_RADIUS = 8  # Slightly smaller for buttons
    PADDING_SMALL = 10      # Small padding
    PADDING_MEDIUM = 15     # Medium padding
    PADDING_LARGE = 20      # Large padding
    FONT_FAMILY = "Segoe UI"  # Primary font
    FONT_FAMILY_ALT = "Arial"  # Alternative font if Segoe UI is not available
    FONT_SIZE_SMALL = 10    # Small font size
    FONT_SIZE_NORMAL = 12   # Normal font size
    FONT_SIZE_LARGE = 14    # Large font size
    FONT_SIZE_TITLE = 18    # Title font size
    BUTTON_HEIGHT = 36      # Standard button height
    ICON_SIZE = 20          # Standard icon size


def setup_theme(ctk):
    """
    Configure the CustomTkinter theme.
    
    Args:
        ctk: The CustomTkinter module
    """
    # Set the appearance mode and default color theme
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    #ctk.configure(background=ThemeColors.BACKGROUND)
    # You can further customize the theme here if needed
    # For example, setting specific widget colors, etc.
