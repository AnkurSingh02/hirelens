import re
from typing import Optional


def clean_text(text: str) -> str:
    """Remove extra whitespace, special characters, and normalize text."""
    if not text:
        return ""

    # Replace multiple newlines with single newline
    text = re.sub(r'\n\s*\n', '\n\n', text)

    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)

    # Remove non-printable characters but keep newlines
    text = re.sub(r'[^\x20-\x7E\n]', '', text)

    return text.strip()


def extract_email(text: str) -> Optional[str]:
    """Extract first email address from text."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """Extract first phone number from text."""
    pattern = r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\./0-9]{7,15}'
    match = re.search(pattern, text)
    return match.group(0).strip() if match else None


def extract_name(text: str) -> Optional[str]:
    """Extract name from first line of resume (heuristic)."""
    lines = text.strip().split('\n')
    for line in lines[:3]:  # Check first 3 lines
        line = line.strip()
        # Name is usually the first non-empty, short line without special chars
        if line and len(line) < 50 and not re.search(r'[@|•·]', line):
            # Check it's not an address or phone
            if not re.search(r'\d{3}[-.]?\d{3}', line):
                if not re.search(r'@', line):
                    return line
    return None


def truncate_text(text: str, max_length: int = 5000) -> str:
    """Truncate text to max length while keeping complete sentences."""
    if len(text) <= max_length:
        return text

    truncated = text[:max_length]
    # Find last sentence boundary
    last_period = truncated.rfind('.')
    if last_period > max_length * 0.8:
        return truncated[:last_period + 1]
    return truncated + "..."