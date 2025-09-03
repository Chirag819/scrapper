"""
Logger Utility
Setup and configuration for logging throughout the application
"""

import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(name='ReviewScraper', level=logging.INFO, log_file=None):
    """
    Setup logger with console and optional file output
    
    Args:
        name (str): Logger name
        level (int): Logging level
        log_file (str): Optional log file path
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Don't add handlers if they already exist
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_default_log_filename():
    """
    Generate default log filename with timestamp
    
    Returns:
        str: Default log filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"logs/review_scraper_{timestamp}.log"


class ScrapingProgressLogger:
    """Logger for tracking scraping progress"""
    
    def __init__(self, logger, total_sources=3):
        self.logger = logger
        self.total_sources = total_sources
        self.completed_sources = 0
        self.total_reviews = 0
        self.start_time = datetime.now()
    
    def log_source_start(self, source_name):
        """Log start of scraping a source"""
        self.logger.info(f"Starting to scrape {source_name}...")
    
    def log_source_complete(self, source_name, review_count, success=True):
        """Log completion of scraping a source"""
        self.completed_sources += 1
        
        if success:
            self.total_reviews += review_count
            self.logger.info(f"✓ Completed {source_name}: {review_count} reviews")
        else:
            self.logger.error(f"✗ Failed to scrape {source_name}")
        
        progress = (self.completed_sources / self.total_sources) * 100
        self.logger.info(f"Progress: {progress:.1f}% ({self.completed_sources}/{self.total_sources} sources)")
    
    def log_page_progress(self, source_name, page, reviews_found):
        """Log progress for pagination"""
        self.logger.info(f"{source_name} - Page {page}: {reviews_found} reviews found")
    
    def log_final_summary(self):
        """Log final scraping summary"""
        duration = datetime.now() - self.start_time
        self.logger.info(f"Scraping completed in {duration}")
        self.logger.info(f"Total reviews collected: {self.total_reviews}")
        self.logger.info(f"Sources processed: {self.completed_sources}/{self.total_sources}")


def log_review_extraction_error(logger, source, error, review_container=None):
    """
    Log review extraction errors with context
    
    Args:
        logger: Logger instance
        source (str): Source name
        error (Exception): Error that occurred
        review_container: Optional BeautifulSoup element for debugging
    """
    logger.warning(f"Failed to extract review from {source}: {str(error)}")
    
    if review_container and logger.isEnabledFor(logging.DEBUG):
        # Log container HTML for debugging (truncated)
        container_html = str(review_container)[:500]
        logger.debug(f"Review container HTML: {container_html}...")


def log_network_error(logger, url, error):
    """
    Log network-related errors
    
    Args:
        logger: Logger instance
        url (str): URL that failed
        error (Exception): Network error
    """
    logger.error(f"Network error accessing {url}: {str(error)}")


def log_parsing_error(logger, source, field, value, error):
    """
    Log data parsing errors
    
    Args:
        logger: Logger instance
        source (str): Source name
        field (str): Field being parsed
        value: Value that failed to parse
        error (Exception): Parsing error
    """
    logger.warning(f"Failed to parse {field} from {source}. Value: '{value}', Error: {str(error)}")


def create_scraping_session_log(company_name, sources, date_range):
    """
    Create a log entry for the start of a scraping session
    
    Args:
        company_name (str): Company being scraped
        sources (list): List of sources to scrape
        date_range (tuple): Start and end dates
        
    Returns:
        str: Formatted log message
    """
    return (f"Starting scraping session for '{company_name}' "
            f"from {sources} between {date_range[0]} and {date_range[1]}")


def setup_debug_logging():
    """Setup detailed debug logging"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Reduce noise from external libraries
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('bs4').setLevel(logging.WARNING)