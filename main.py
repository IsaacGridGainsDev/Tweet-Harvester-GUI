#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Twitter Data Miner - Main Application

This is the main entry point for the Twitter Data Miner application.
It initializes the GUI and sets up the data mining pipeline.
"""

import os
import sys
import logging
from dotenv import load_dotenv
from gui.app_main import TwitterMinerApp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """
    Main function to initialize and run the Twitter Data Miner application.
    """
    logger.info("Starting Twitter Data Miner application")
    
    # Load environment variables from .env file
    load_dotenv()
    logger.info("Loaded environment variables from .env file")
    
    # Create data directory if it doesn't exist
    os.makedirs(os.path.join(os.path.dirname(__file__), 'data'), exist_ok=True)
    
    # Initialize and run the GUI
    app = TwitterMinerApp()
    app.mainloop()


if __name__ == "__main__":
    main()