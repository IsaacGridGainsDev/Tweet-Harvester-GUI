#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Twitter Data Miner - View Panels Package

This package contains all the view panels for the Twitter Data Miner GUI.
"""

# Import all panels to make them available when importing the package
from .search_input_panel import SearchInputPanel
from .chart_viewer_panel import ChartViewerPanel
from .matrix_panel import MatrixPanel
from .map_panel import MapPanel
from .orientation_analyzer_panel import OrientationAnalyzerPanel

__all__ = [
    'SearchInputPanel',
    'ChartViewerPanel',
    'MatrixPanel',
    'MapPanel',
    'OrientationAnalyzerPanel'
]
