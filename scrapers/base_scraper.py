# 


"""
Base Scraper Module
Provides base functionality for all scrapers
"""

import requests
import time
import logging
from abc import ABC, abstractmethod
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseScraper(ABC):
    """Base class for all scrapers with common functionality"""
    
    def __init__(self, delay=2, max_retries=3, timeout=30):
        """
        Initialize base scraper
        
        Args:
            delay (float): Delay between requests in seconds
            max_retries (int): Maximum number of retries for failed requests
            timeout (int): Request timeout in seconds
        """
        self.delay = delay
        self.max_retries = max_retries
        self.timeout = timeout
        
        # Setup logging
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Setup session with retry strategy
        self.session = requests.Session()
        
        # Configure retry strategy (fix for newer urllib3 versions)
        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],  # Updated parameter name
            backoff_factor=1
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # Set timeout
        self.session.timeout = timeout
    
    @abstractmethod
    def search_product(self, company_name):
        """
        Search for a product/company on the platform
        
        Args:
            company_name (str): Name of the company/product
            
        Returns:
            str: URL to the product/company page
        """
        pass
    
    @abstractmethod
    def scrape_reviews(self, company_name, start_date, end_date):
        """
        Scrape reviews for a specific company and date range
        
        Args:
            company_name (str): Name of the company
            start_date (str): Start date (YYYY-MM-DD)
            end_date (str): End date (YYYY-MM-DD)
            
        Returns:
            list: List of review dictionaries
        """
        pass
    
    @abstractmethod
    def extract_review_data(self, container):
        """
        Extract review data from a review container
        
        Args:
            container: BeautifulSoup element containing review
            
        Returns:
            dict: Review data dictionary
        """
        pass
    
    def safe_request(self, url, **kwargs):
        """
        Make a safe HTTP request with error handling
        
        Args:
            url (str): URL to request
            **kwargs: Additional arguments for requests
            
        Returns:
            requests.Response: Response object or None if failed
        """
        try:
            response = self.session.get(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed for {url}: {str(e)}")
            return None
    
    def wait(self):
        """Wait for the specified delay between requests"""
        time.sleep(self.delay)
    
    def close(self):
        """Close the session"""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()