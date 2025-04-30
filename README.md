# Twitter Data Miner

A comprehensive Python application for mining, analyzing, and visualizing Twitter data using both historical scraping and real-time streaming capabilities.

## Features

- **Keyword-based Tweet Scraping**: Extract historical tweets using tweepy (formerly snscrape)
- **Real-time Tweet Streaming**: Capture live tweets as they happen using astream
- **Advanced Text Processing**: Tokenization, stop word removal, and term extraction
- **Sentiment Analysis**: Analyze tweet sentiment using semantic orientation scoring
- **Data Visualization**: Generate charts for term frequency, time series analysis, and geolocation mapping
- **User-friendly GUI**: Easy-to-use interface built with CustomTkinter

## Project Structure

```
twitter_data_miner/
├── main.py                 # Main application entry point
├── data/                   # Data storage directory
│   └── tweets.json         # Collected tweets
├── gui/                    # GUI components
│   └── assets/              # Main GUI implementation
│   └── components/              # Main GUI implementation
│        └──  views/             # Main GUI implementation
│        └──  footer.py             # Main GUI implementation
│        └──  main_view.py             # Main GUI implementation
│        └──  side_nav.py             # Main GUI implementation
│        └──  top_bar.py             # Main GUI implementation
│   └── styles              # Main GUI implementation
│        └──  app_main.py             # Main GUI implementation
├── mining/                 # Data mining modules
│   ├── __init__.py
│   └── data_mining.py      # Tweet scraping and streaming
├── processing/             # Data preprocessing
│   └── preprocessing.py    # Text processing and tokenization
├── analytics/              # Data analysis
│   └── analysis.py         # Term frequency and sentiment analysis
├── visualization/          # Data visualization
│   └── visualization.py    # Charts and maps generation
├── utils/                  # Utility functions
│   └── helpers.py          # Helper functions
├── README.md               # Project documentation
└── requirements.txt        # Project dependencies
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/twitter_data_miner.git
   cd twitter_data_miner
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Twitter API Access (Required for historical data mining):
   - Apply for a Twitter Developer account at https://developer.twitter.com/
   - Create a project and app to get your API keys
   - Add your Twitter API credentials to the `.env` file in the project root:
   ```
   # Twitter API Credentials
   API_KEY=your_api_key_here
   API_KEY_SECRET=your_api_key_secret_here
   ACCESS_TOKEN=your_access_token_here
   ACCESS_TOKEN_SECRET=your_access_token_secret_here
   TWITTER_BEARER_TOKEN=your_bearer_token_here
   ```
   - The application will automatically load these credentials when it starts

4. Download NLTK data (required for text processing):
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

## Running the Application

1. Start the application:
   ```
   python main.py
   ```

2. Use the GUI to:
   - Enter keywords for tweet mining
   - Select data processing options
   - Choose visualization methods
   - Start/stop data collection
   - View analysis results

## Example Output

![Term Frequency Chart](placeholder_term_frequency.png)

![Sentiment Analysis](placeholder_sentiment.png)

![Geolocation Map](placeholder_geolocation.png)

## License

MIT

## Contributors

- Isaac Tolulope Akinladejo