"""
Configuration settings for the review scraper
"""

import os
from pathlib import Path

# Application settings
APP_NAME = "Review Scraper"
VERSION = "1.0.0"
AUTHOR = "Review Scraper Team"

# Default settings
DEFAULT_DELAY = 2.0  # seconds between requests
DEFAULT_TIMEOUT = 30  # request timeout in seconds
DEFAULT_MAX_RETRIES = 3
DEFAULT_MAX_PAGES = 50  # maximum pages to scrape per source

# Output settings
DEFAULT_OUTPUT_DIR = Path("output")
DEFAULT_LOG_DIR = Path("logs")
DEFAULT_OUTPUT_FORMAT = "json"

# Date settings
MIN_DATE = "2010-01-01"  # Minimum allowed start date
DATE_FORMAT = "%Y-%m-%d"
DEFAULT_DATE_RANGE_YEARS = 1

# Supported sources
SUPPORTED_SOURCES = ["g2", "capterra", "trustpilot", "all"]
DEFAULT_SOURCE = "all"

# Review validation settings
MIN_REVIEW_LENGTH = 10  # minimum characters for a valid review
MAX_REVIEW_LENGTH = 10000  # maximum characters for a review
MIN_TITLE_LENGTH = 3  # minimum characters for a valid title
MAX_TITLE_LENGTH = 200  # maximum characters for a title

# Network settings
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

# Request headers
DEFAULT_HEADERS = {
    'User-Agent': DEFAULT_USER_AGENT,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_LOG_LEVEL = "INFO"

# File naming patterns
OUTPUT_FILENAME_PATTERN = "reviews_{company}_{timestamp}.json"
LOG_FILENAME_PATTERN = "review_scraper_{timestamp}.log"

# Platform-specific settings
PLATFORM_CONFIGS = {
    "g2": {
        "base_url": "https://www.g2.com",
        "search_path": "/search",
        "delay": DEFAULT_DELAY,
        "max_pages": DEFAULT_MAX_PAGES,
        "timeout": DEFAULT_TIMEOUT
    },
    "capterra": {
        "base_url": "https://www.capterra.com", 
        "search_path": "/software-search",
        "delay": DEFAULT_DELAY,
        "max_pages": DEFAULT_MAX_PAGES,
        "timeout": DEFAULT_TIMEOUT
    },
    "trustpilot": {
        "base_url": "https://www.trustpilot.com",
        "search_path": "/search",
        "delay": DEFAULT_DELAY,
        "max_pages": DEFAULT_MAX_PAGES,
        "timeout": DEFAULT_TIMEOUT
    }
}

# Error handling settings
MAX_CONSECUTIVE_ERRORS = 5  # Stop scraping after this many consecutive errors
RETRY_DELAYS = [1, 2, 4, 8, 16]  # Exponential backoff delays for retries

# Environment variable overrides
def get_config_value(key, default):
    """Get configuration value from environment variable or use default"""
    env_key = f"REVIEW_SCRAPER_{key.upper()}"
    return os.getenv(env_key, default)

# Apply environment overrides
DEFAULT_DELAY = float(get_config_value("delay", DEFAULT_DELAY))
DEFAULT_TIMEOUT = int(get_config_value("timeout", DEFAULT_TIMEOUT))
DEFAULT_MAX_RETRIES = int(get_config_value("max_retries", DEFAULT_MAX_RETRIES))
DEFAULT_LOG_LEVEL = get_config_value("log_level", DEFAULT_LOG_LEVEL)

# Create directories if they don't exist
DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_LOG_DIR.mkdir(parents=True, exist_ok=True)