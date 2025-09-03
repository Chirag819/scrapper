#!/usr/bin/env python3
"""
Review Scraper Main Script
Scrapes product reviews from Capterra and Trustpilot
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from scrapers.g2_scraper import G2Scraper
from scrapers.capterra_scraper import CapterraScraper
from scrapers.trustpilot_scraper import TrustpilotScraper
from utils.validators import validate_date_range, validate_company_name, validate_source
from utils.logger import setup_logger


class ReviewScraperManager:
    """Main class for managing review scraping operations"""
    
    SUPPORTED_SOURCES = ['g2', 'capterra', 'trustpilot', 'all']
    
    def __init__(self):
        self.logger = setup_logger()
        self.scrapers = {
            'g2': G2Scraper(),
            'capterra': CapterraScraper(),
            'trustpilot': TrustpilotScraper()
        }
    
    def scrape_reviews(self, company_name, start_date, end_date, source='all'):
        """
        Scrape reviews from specified source(s)
        
        Args:
            company_name (str): Name of the company
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            source (str): Source to scrape from ('g2', 'capterra', 'trustpilot', 'all')
        
        Returns:
            dict: Dictionary containing reviews from all sources
        """
        # Validate inputs
        validate_company_name(company_name)
        validate_date_range(start_date, end_date)
        validate_source(source, self.SUPPORTED_SOURCES)
        
        self.logger.info(f"Starting review scraping for {company_name}")
        self.logger.info(f"Date range: {start_date} to {end_date}")
        self.logger.info(f"Source(s): {source}")
        
        results = {
            'company_name': company_name,
            'date_range': {
                'start': start_date,
                'end': end_date
            },
            'scraping_timestamp': datetime.now().isoformat(),
            'sources': {}
        }
        
        # Determine which sources to scrape
        sources_to_scrape = self.SUPPORTED_SOURCES[:-1] if source == 'all' else [source]
        
        for src in sources_to_scrape:
            try:
                self.logger.info(f"Scraping {src.upper()}...")
                scraper = self.scrapers[src]
                reviews = scraper.scrape_reviews(company_name, start_date, end_date)
                
                results['sources'][src] = {
                    'total_reviews': len(reviews),
                    'reviews': reviews,
                    'status': 'success'
                }
                
                self.logger.info(f"Successfully scraped {len(reviews)} reviews from {src.upper()}")
                
            except Exception as e:
                self.logger.error(f"Failed to scrape {src.upper()}: {str(e)}")
                results['sources'][src] = {
                    'total_reviews': 0,
                    'reviews': [],
                    'status': 'failed',
                    'error': str(e)
                }
        
        return results
    
    def save_results(self, results, output_file=None):
        """
        Save results to JSON file
        
        Args:
            results (dict): Results dictionary
            output_file (str): Output file path (optional)
        
        Returns:
            str: Path to saved file
        """
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            company = results['company_name'].replace(' ', '_').lower()
            output_file = f"output/{company}_{timestamp}.json"
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Results saved to {output_path}")
        return str(output_path)


def main():
    """Main function to handle command line arguments and execute scraping"""
    parser = argparse.ArgumentParser(
        description='Scrape product reviews from Capterra and Trustpilot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --company "Slack" --start-date "2023-01-01" --end-date "2023-12-31" --source "g2"
  python main.py --company "Zoom" --start-date "2023-06-01" --end-date "2023-12-31" --source "all"
  python main.py --company "HubSpot" --start-date "2023-01-01" --end-date "2023-12-31" --output "hubspot_reviews.json"
        """
    )
    
    parser.add_argument(
        '--company',
        required=True,
        help='Company name to search for reviews'
    )
    
    parser.add_argument(
        '--start-date',
        required=True,
        help='Start date for review search (YYYY-MM-DD format)'
    )
    
    parser.add_argument(
        '--end-date',
        required=True,
        help='End date for review search (YYYY-MM-DD format)'
    )
    
    parser.add_argument(
        '--source',
        default='all',
        choices=['g2', 'capterra', 'trustpilot', 'all'],
        help='Source to scrape reviews from (default: all)'
    )
    
    parser.add_argument(
        '--output',
        help='Output JSON file path (optional)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize scraper manager
        scraper_manager = ReviewScraperManager()
        
        # Scrape reviews
        results = scraper_manager.scrape_reviews(
            company_name=args.company,
            start_date=args.start_date,
            end_date=args.end_date,
            source=args.source
        )
        
        # Save results
        output_path = scraper_manager.save_results(results, args.output)
        
        # Print summary
        total_reviews = sum(
            src_data.get('total_reviews', 0) 
            for src_data in results['sources'].values()
        )
        
        print(f"\n{'='*50}")
        print(f"SCRAPING SUMMARY")
        print(f"{'='*50}")
        print(f"Company: {results['company_name']}")
        print(f"Date Range: {results['date_range']['start']} to {results['date_range']['end']}")
        print(f"Total Reviews Found: {total_reviews}")
        print(f"Output File: {output_path}")
        print(f"{'='*50}")
        
        for source, data in results['sources'].items():
            status = "✓" if data['status'] == 'success' else "✗"
            print(f"{status} {source.upper()}: {data['total_reviews']} reviews")
        
        print(f"{'='*50}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


# /usr/bin/env python3
# """
# Review Scraper Main Script
# Scrapes product reviews from Capterra and Trustpilot
# """

# import argparse
# import json
# import sys
# from datetime import datetime
# from pathlib import Path

# import os
# import sys

# # Add current directory to Python path for imports
# current_dir = os.path.dirname(os.path.abspath(__file__))
# if current_dir not in sys.path:
#     sys.path.insert(0, current_dir)

# try:
#     from scrapers.capterra_scraper import CapterraScraper
#     from scrapers.trustpilot_scraper import TrustpilotScraper
#     from utils.validators import validate_date_range, validate_company_name, validate_source
#     from utils.logger import setup_logger
# except ImportError as e:
#     print(f"Import error: {e}")
#     print("Make sure all required files are present and dependencies are installed.")
#     print("Try running: pip install requests beautifulsoup4 lxml python-dateutil")
#     sys.exit(1)


# class ReviewScraperManager:
#     """Main class for managing review scraping operations"""
    
#     SUPPORTED_SOURCES = ['g2', 'capterra', 'trustpilot', 'all']
    
#     def __init__(self):
#         self.logger = setup_logger()
#         self.scrapers = {
#             'capterra': CapterraScraper(),
#             'trustpilot': TrustpilotScraper()
#         }
    
#     def scrape_reviews(self, company_name, start_date, end_date, source='all'):
#         """
#         Scrape reviews from specified source(s)
        
#         Args:
#             company_name (str): Name of the company
#             start_date (str): Start date in YYYY-MM-DD format
#             end_date (str): End date in YYYY-MM-DD format
#             source (str): Source to scrape from ('g2', 'capterra', 'trustpilot', 'all')
        
#         Returns:
#             dict: Dictionary containing reviews from all sources
#         """
#         # Validate inputs
#         validate_company_name(company_name)
#         validate_date_range(start_date, end_date)
#         validate_source(source, self.SUPPORTED_SOURCES)
        
#         self.logger.info(f"Starting review scraping for {company_name}")
#         self.logger.info(f"Date range: {start_date} to {end_date}")
#         self.logger.info(f"Source(s): {source}")
        
#         results = {
#             'company_name': company_name,
#             'date_range': {
#                 'start': start_date,
#                 'end': end_date
#             },
#             'scraping_timestamp': datetime.now().isoformat(),
#             'sources': {}
#         }
        
#         # Determine which sources to scrape
#         sources_to_scrape = self.SUPPORTED_SOURCES[:-1] if source == 'all' else [source]
        
#         for src in sources_to_scrape:
#             try:
#                 self.logger.info(f"Scraping {src.upper()}...")
#                 scraper = self.scrapers[src]
#                 reviews = scraper.scrape_reviews(company_name, start_date, end_date)
                
#                 results['sources'][src] = {
#                     'total_reviews': len(reviews),
#                     'reviews': reviews,
#                     'status': 'success'
#                 }
                
#                 self.logger.info(f"Successfully scraped {len(reviews)} reviews from {src.upper()}")
                
#             except Exception as e:
#                 self.logger.error(f"Failed to scrape {src.upper()}: {str(e)}")
#                 results['sources'][src] = {
#                     'total_reviews': 0,
#                     'reviews': [],
#                     'status': 'failed',
#                     'error': str(e)
#                 }
        
#         return results
    
#     def save_results(self, results, output_file=None):
#         """
#         Save results to JSON file
        
#         Args:
#             results (dict): Results dictionary
#             output_file (str): Output file path (optional)
        
#         Returns:
#             str: Path to saved file
#         """
#         if not output_file:
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             company = results['company_name'].replace(' ', '_').lower()
#             output_file = f"reviews_{company}_{timestamp}.json"
        
#         output_path = Path(output_file)
#         output_path.parent.mkdir(parents=True, exist_ok=True)
        
#         with open(output_path, 'w', encoding='utf-8') as f:
#             json.dump(results, f, indent=2, ensure_ascii=False)
        
#         self.logger.info(f"Results saved to {output_path}")
#         return str(output_path)


# def main():
#     """Main function to handle command line arguments and execute scraping"""
#     parser = argparse.ArgumentParser(
#         description='Scrape product reviews from G2, Capterra, and Trustpilot',
#         formatter_class=argparse.RawDescriptionHelpFormatter,
#         epilog="""
# Examples:
#   python main.py --company "Slack" --start-date "2023-01-01" --end-date "2023-12-31" --source "g2"
#   python main.py --company "Zoom" --start-date "2023-06-01" --end-date "2023-12-31" --source "all"
#   python main.py --company "HubSpot" --start-date "2023-01-01" --end-date "2023-12-31" --output "hubspot_reviews.json"
#         """
#     )
    
#     parser.add_argument(
#         '--company',
#         required=True,
#         help='Company name to search for reviews'
#     )
    
#     parser.add_argument(
#         '--start-date',
#         required=True,
#         help='Start date for review search (YYYY-MM-DD format)'
#     )
    
#     parser.add_argument(
#         '--end-date',
#         required=True,
#         help='End date for review search (YYYY-MM-DD format)'
#     )
    
#     parser.add_argument(
#         '--source',
#         default='all',
#         choices=['g2', 'capterra', 'trustpilot', 'all'],
#         help='Source to scrape reviews from (default: all)'
#     )
    
#     parser.add_argument(
#         '--output',
#         help='Output JSON file path (optional)'
#     )
    
#     parser.add_argument(
#         '--verbose',
#         action='store_true',
#         help='Enable verbose logging'
#     )
    
#     args = parser.parse_args()
    
#     try:
#         # Initialize scraper manager
#         scraper_manager = ReviewScraperManager()
        
#         # Scrape reviews
#         results = scraper_manager.scrape_reviews(
#             company_name=args.company,
#             start_date=args.start_date,
#             end_date=args.end_date,
#             source=args.source
#         )
        
#         # Save results
#         output_path = scraper_manager.save_results(results, args.output)
        
#         # Print summary
#         total_reviews = sum(
#             src_data.get('total_reviews', 0) 
#             for src_data in results['sources'].values()
#         )
        
#         print(f"\n{'='*50}")
#         print(f"SCRAPING SUMMARY")
#         print(f"{'='*50}")
#         print(f"Company: {results['company_name']}")
#         print(f"Date Range: {results['date_range']['start']} to {results['date_range']['end']}")
#         print(f"Total Reviews Found: {total_reviews}")
#         print(f"Output File: {output_path}")
#         print(f"{'='*50}")
        
#         for source, data in results['sources'].items():
#             status = "✓" if data['status'] == 'success' else "✗"
#             print(f"{status} {source.upper()}: {data['total_reviews']} reviews")
        
#         print(f"{'='*50}")
        
#     except Exception as e:
#         print(f"Error: {str(e)}", file=sys.stderr)
#         sys.exit(1)


# if __name__ == "__main__":
#     main()