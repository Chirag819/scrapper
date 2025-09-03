#!/usr/bin/env python3
"""
Demo script for SaaS Review Scraper
This script demonstrates the capabilities of the review scraper with sample data.
"""

import json
import os
from datetime import datetime, timedelta
from main import ReviewScraperManager

def run_demo():
    """Run a demonstration of the SaaS Review Scraper"""
    
    print("🚀 SaaS Review Scraper Demo")
    print("=" * 50)
    
    # Demo companies
    demo_companies = [
        "Slack",
        "HubSpot", 
        "Salesforce"
    ]
    
    # Date range (last 2 years)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    
    print(f"📅 Date Range: {start_date_str} to {end_date_str}")
    print(f"🎯 Demo Companies: {', '.join(demo_companies)}")
    print()
    
    # Create output directory
    os.makedirs("demo_output", exist_ok=True)
    
    for company in demo_companies:
        print(f"🔍 Scraping reviews for: {company}")
        print("-" * 30)
        
        try:
            # Initialize scraper
            scraper = ReviewScraperManager()
            
            # Scrape reviews
            results = scraper.scrape_reviews(
                company_name=company,
                start_date=start_date_str,
                end_date=end_date_str,
                sources=["capterra", "trustpilot"]  # Skip G2 for demo
            )
            
            # Save results
            output_file = f"demo_output/{company.lower()}_demo_results.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            # Display summary
            total_reviews = 0
            for source, data in results.get("sources", {}).items():
                if isinstance(data, dict) and "total_reviews" in data:
                    count = data["total_reviews"]
                    total_reviews += count
                    print(f"  ✅ {source.upper()}: {count} reviews")
            
            print(f"  📊 Total: {total_reviews} reviews")
            print(f"  💾 Saved to: {output_file}")
            print()
            
        except Exception as e:
            print(f"  ❌ Error scraping {company}: {str(e)}")
            print()
    
    print("🎉 Demo completed!")
    print("📁 Check the 'demo_output' folder for results")
    print("📖 See README.md for detailed usage instructions")

def show_sample_output():
    """Display sample output format"""
    
    print("\n📋 Sample Output Format:")
    print("=" * 50)
    
    sample = {
        "company_name": "Slack",
        "date_range": {
            "start": "2024-01-01",
            "end": "2025-12-31"
        },
        "scraping_timestamp": "2025-09-03T17:25:15.123456",
        "sources": {
            "capterra": {
                "total_reviews": 2,
                "reviews": [
                    {
                        "reviewer": "John Doe",
                        "title": "Great collaboration tool",
                        "date": "2024-06-15",
                        "rating": "5.0",
                        "text": "Full review content...",
                        "pros": "What I liked most...",
                        "cons": "Areas for improvement...",
                        "source": "Capterra"
                    }
                ]
            }
        }
    }
    
    print(json.dumps(sample, indent=2))
    print("\n💡 Each review includes:")
    print("  • Reviewer name and title")
    print("  • Publication date and rating")
    print("  • Full review text")
    print("  • Pros and cons (Capterra)")
    print("  • Source platform")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--sample":
        show_sample_output()
    else:
        run_demo()
