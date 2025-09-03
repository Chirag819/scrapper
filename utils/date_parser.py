"""
Date Parser Utility
Handles parsing of various date formats from review sites
"""

import re
from datetime import datetime, timedelta
from dateutil import parser as dateutil_parser
import logging


logger = logging.getLogger(__name__)


def parse_review_date(date_string):
    """
    Parse date string from various review sites into datetime object
    
    Args:
        date_string (str): Date string in various formats
        
    Returns:
        datetime or None: Parsed datetime object or None if parsing fails
    """
    if not date_string or not isinstance(date_string, str):
        return None
    
    date_string = date_string.strip()
    
    if not date_string:
        return None
    
    # Try different parsing strategies
    parsers = [
        parse_iso_date,
        parse_relative_date,
        parse_common_formats,
        parse_with_dateutil,
        parse_timestamp
    ]
    
    for parser_func in parsers:
        try:
            result = parser_func(date_string)
            if result:
                return result
        except Exception as e:
            logger.debug(f"Parser {parser_func.__name__} failed for '{date_string}': {str(e)}")
            continue
    
    logger.warning(f"Could not parse date string: '{date_string}'")
    return None


def parse_iso_date(date_string):
    """Parse ISO format dates (YYYY-MM-DD, YYYY-MM-DDTHH:MM:SS)"""
    iso_patterns = [
        r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})',
        r'(\d{4}-\d{2}-\d{2})'
    ]
    
    for pattern in iso_patterns:
        match = re.search(pattern, date_string)
        if match:
            try:
                parsed_date = datetime.fromisoformat(match.group(1).replace('T', ' '))
                # Convert to timezone-naive datetime to avoid comparison issues
                if parsed_date.tzinfo is not None:
                    parsed_date = parsed_date.replace(tzinfo=None)
                return parsed_date
            except:
                return datetime.strptime(match.group(1)[:10], '%Y-%m-%d')
    
    return None


def parse_relative_date(date_string):
    """Parse relative date strings (e.g., '2 days ago', 'yesterday')"""
    date_string_lower = date_string.lower()
    current_time = datetime.now()
    
    # Today/yesterday patterns
    if 'today' in date_string_lower or 'just now' in date_string_lower:
        return current_time
    
    if 'yesterday' in date_string_lower:
        return current_time - timedelta(days=1)
    
    # Relative time patterns
    relative_patterns = [
        (r'(\d+)\s*(?:second|sec)s?\s*ago', 'seconds'),
        (r'(\d+)\s*(?:minute|min)s?\s*ago', 'minutes'),
        (r'(\d+)\s*(?:hour|hr)s?\s*ago', 'hours'),
        (r'(\d+)\s*days?\s*ago', 'days'),
        (r'(\d+)\s*weeks?\s*ago', 'weeks'),
        (r'(\d+)\s*months?\s*ago', 'months'),
        (r'(\d+)\s*years?\s*ago', 'years'),
        (r'a\s*(?:second|sec)\s*ago', 'seconds', 1),
        (r'a\s*(?:minute|min)\s*ago', 'minutes', 1),
        (r'an?\s*hour\s*ago', 'hours', 1),
        (r'a\s*day\s*ago', 'days', 1),
        (r'a\s*week\s*ago', 'weeks', 1),
        (r'a\s*month\s*ago', 'months', 1),
        (r'a\s*year\s*ago', 'years', 1)
    ]
    
    for pattern_info in relative_patterns:
        if len(pattern_info) == 3:
            pattern, unit, value = pattern_info
        else:
            pattern, unit = pattern_info
            match = re.search(pattern, date_string_lower)
            if not match:
                continue
            value = int(match.group(1))
        
        if re.search(pattern, date_string_lower):
            if unit == 'seconds':
                return current_time - timedelta(seconds=value)
            elif unit == 'minutes':
                return current_time - timedelta(minutes=value)
            elif unit == 'hours':
                return current_time - timedelta(hours=value)
            elif unit == 'days':
                return current_time - timedelta(days=value)
            elif unit == 'weeks':
                return current_time - timedelta(weeks=value)
            elif unit == 'months':
                return current_time - timedelta(days=value * 30)  # Approximate
            elif unit == 'years':
                return current_time - timedelta(days=value * 365)  # Approximate
    
    return None


def parse_common_formats(date_string):
    """Parse common date formats"""
    # Remove common prefixes/suffixes
    cleaned = re.sub(r'(on\s+|posted\s+|reviewed\s+|updated\s+)', '', date_string, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s*\([^)]*\)\s*', '', cleaned)  # Remove parentheses content
    cleaned = cleaned.strip()
    
    # Common date formats
    formats = [
        '%B %d, %Y',        # January 1, 2023
        '%b %d, %Y',        # Jan 1, 2023
        '%d %B %Y',         # 1 January 2023
        '%d %b %Y',         # 1 Jan 2023
        '%m/%d/%Y',         # 01/01/2023
        '%d/%m/%Y',         # 01/01/2023
        '%m-%d-%Y',         # 01-01-2023
        '%d-%m-%Y',         # 01-01-2023
        '%Y/%m/%d',         # 2023/01/01
        '%Y-%m-%d',         # 2023-01-01
        '%m/%d/%y',         # 01/01/23
        '%d/%m/%y',         # 01/01/23
        '%b %d',            # Jan 1 (assume current year)
        '%B %d',            # January 1 (assume current year)
    ]
    
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(cleaned, fmt)
            # If year is missing, assume current year
            if parsed_date.year == 1900:
                parsed_date = parsed_date.replace(year=datetime.now().year)
            return parsed_date
        except ValueError:
            continue
    
    return None


def parse_with_dateutil(date_string):
    """Parse date using dateutil parser (more flexible)"""
    try:
        # Remove common review site specific text
        cleaned = re.sub(r'(reviewed|posted|updated|on|at|•|\|)', ' ', date_string, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # Try to parse with dateutil
        parsed_date = dateutil_parser.parse(cleaned, fuzzy=True)
        
        # Convert to timezone-naive datetime to avoid comparison issues
        if parsed_date.tzinfo is not None:
            parsed_date = parsed_date.replace(tzinfo=None)
        
        return parsed_date
    except:
        return None


def parse_timestamp(date_string):
    """Parse timestamp formats"""
    # Unix timestamp
    timestamp_match = re.search(r'(\d{10,13})', date_string)
    if timestamp_match:
        try:
            timestamp = int(timestamp_match.group(1))
            # Handle milliseconds
            if timestamp > 10**10:
                timestamp = timestamp / 1000
            return datetime.fromtimestamp(timestamp)
        except:
            pass
    
    return None


def normalize_date_format(date_obj):
    """
    Normalize datetime object to standard format
    
    Args:
        date_obj (datetime): Datetime object to normalize
        
    Returns:
        str: Normalized date string in YYYY-MM-DD format
    """
    if not isinstance(date_obj, datetime):
        return None
    
    return date_obj.strftime('%Y-%m-%d')


def is_date_in_range(date_obj, start_date, end_date):
    """
    Check if date is within the specified range
    
    Args:
        date_obj (datetime): Date to check
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        
    Returns:
        bool: True if date is in range, False otherwise
    """
    if not isinstance(date_obj, datetime):
        return False
    
    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        return start_dt <= date_obj <= end_dt
    except:
        return False


def get_date_variations(date_string):
    """
    Generate possible date variations from a string
    
    Args:
        date_string (str): Original date string
        
    Returns:
        list: List of possible date variations
    """
    variations = [date_string]
    
    # Add variations with different separators
    if '-' in date_string:
        variations.append(date_string.replace('-', '/'))
        variations.append(date_string.replace('-', ' '))
    
    if '/' in date_string:
        variations.append(date_string.replace('/', '-'))
        variations.append(date_string.replace('/', ' '))
    
    # Add variations with different month formats
    month_mappings = {
        'January': 'Jan', 'February': 'Feb', 'March': 'Mar',
        'April': 'Apr', 'May': 'May', 'June': 'Jun',
        'July': 'Jul', 'August': 'Aug', 'September': 'Sep',
        'October': 'Oct', 'November': 'Nov', 'December': 'Dec'
    }
    
    for full_month, short_month in month_mappings.items():
        if full_month in date_string:
            variations.append(date_string.replace(full_month, short_month))
        elif short_month in date_string:
            variations.append(date_string.replace(short_month, full_month))
    
    return list(set(variations))  # Remove duplicates