from datetime import datetime
def clean_text(text):
    """Clean extracted text by removing extra whitespace and handling None values."""
    if text:
        return text.strip()
    return None

def format_date(date_str):
    """Format date string to a standard format (YYYY-MM-DD)."""
    date_str = clean_text(date_str)
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%B %d, %Y").strftime("%Y-%m-%d")
    except ValueError:
        return None



