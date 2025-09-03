"""
Scrapers package
Contains all review scraper implementations
"""

from .base_scraper import BaseScraper
from .g2_scraper import G2Scraper
from .capterra_scraper import CapterraScraper
from .trustpilot_scraper import TrustpilotScraper

__all__ = [
    'BaseScraper',
    'G2Scraper', 
    'CapterraScraper',
    'TrustpilotScraper'
]