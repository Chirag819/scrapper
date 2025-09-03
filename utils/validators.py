"""
Validation Utilities
Input validation functions for the review scraper
"""

import re
from datetime import datetime


def validate_company_name(company_name):
    """
    Validate company name input
    
    Args:
        company_name (str): Company name to validate
        
    Raises:
        ValueError: If company name is invalid
    """
    if not company_name or not isinstance(company_name, str):
        raise ValueError("Company name must be a non-empty string")
    
    if len(company_name.strip()) < 2:
        raise ValueError("Company name must be at least 2 characters long")
    
    if len(company_name.strip()) > 100:
        raise ValueError("Company name must be less than 100 characters long")
    
    # Check for potentially harmful characters
    if re.search(r'[<>"\'\{\}\[\]]', company_name):
        raise ValueError("Company name contains invalid characters")


def validate_date_range(start_date, end_date):
    """
    Validate date range inputs
    
    Args:
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        
    Raises:
        ValueError: If dates are invalid or range is invalid
    """
    # Validate date format
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    
    if not re.match(date_pattern, start_date):
        raise ValueError("Start date must be in YYYY-MM-DD format")
    
    if not re.match(date_pattern, end_date):
        raise ValueError("End date must be in YYYY-MM-DD format")
    
    # Parse dates
    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError as e:
        raise ValueError(f"Invalid date format: {str(e)}")
    
    # Validate date range
    if start_dt > end_dt:
        raise ValueError("Start date must be before or equal to end date")
    
    # Check if dates are reasonable (not too far in the past or future)
    current_date = datetime.now()
    min_date = datetime(2010, 1, 1)  # Assume no reviews before 2010
    
    if start_dt < min_date:
        raise ValueError(f"Start date cannot be before {min_date.strftime('%Y-%m-%d')}")
    
    # Allow future dates up to 1 year in the future (for reviews that might be dated in the future)
    max_future_date = current_date.replace(year=current_date.year + 1)
    if end_dt > max_future_date:
        raise ValueError(f"End date cannot be more than 1 year in the future (max: {max_future_date.strftime('%Y-%m-%d')})")
    
    # Check if date range is reasonable (not more than 10 years)
    if (end_dt - start_dt).days > 3650:
        raise ValueError("Date range cannot exceed 10 years")


def validate_source(source, supported_sources):
    """
    Validate source input
    
    Args:
        source (str): Source name to validate
        supported_sources (list): List of supported sources
        
    Raises:
        ValueError: If source is invalid
    """
    if not source or not isinstance(source, str):
        raise ValueError("Source must be a non-empty string")
    
    source = source.lower().strip()
    
    if source not in [s.lower() for s in supported_sources]:
        raise ValueError(f"Unsupported source '{source}'. Supported sources: {', '.join(supported_sources)}")


def validate_output_path(output_path):
    """
    Validate output file path
    
    Args:
        output_path (str): Output file path to validate
        
    Raises:
        ValueError: If output path is invalid
    """
    if not output_path or not isinstance(output_path, str):
        raise ValueError("Output path must be a non-empty string")
    
    # Check file extension
    if not output_path.lower().endswith('.json'):
        raise ValueError("Output file must have .json extension")
    
    # Check for invalid characters in filename
    invalid_chars = r'[<>:"|?*]'
    if re.search(invalid_chars, output_path):
        raise ValueError("Output path contains invalid characters")
    
    # Check path length
    if len(output_path) > 260:  # Windows path limit
        raise ValueError("Output path is too long")


def sanitize_filename(filename):
    """
    Sanitize filename by removing/replacing invalid characters
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"|?*\\\/]', '_', filename)
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Remove multiple consecutive underscores
    filename = re.sub(r'_{2,}', '_', filename)
    
    # Remove leading/trailing underscores and dots
    filename = filename.strip('_.')
    
    # Ensure minimum length
    if len(filename) < 1:
        filename = 'reviews'
    
    # Ensure maximum length
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename


def validate_review_data(review_data):
    """
    Validate review data structure
    
    Args:
        review_data (dict): Review data dictionary to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(review_data, dict):
        return False
    
    # Required fields
    required_fields = ['title', 'review', 'date']
    for field in required_fields:
        if field not in review_data:
            return False
        if not isinstance(review_data[field], str):
            return False
    
    # Check if at least title or review has content
    if not review_data['title'].strip() and not review_data['review'].strip():
        return False
    
    # Optional field validations
    if 'rating' in review_data:
        if not isinstance(review_data['rating'], (int, float)):
            return False
        if not (0 <= review_data['rating'] <= 5):
            return False
    
    return True