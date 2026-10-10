import requests
from bs4 import BeautifulSoup
import re
from utils.text_cleaner import clean_text


def scrape_job_url(url: str) -> str:
    """
    Scrape job description text from a URL.

    Supports: LinkedIn, Indeed, generic job pages.
    """
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(
            f"Could not fetch URL: {str(e)}. "
            "Try pasting the job description text directly."
        )

    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove script and style elements
    for element in soup(['script', 'style', 'nav', 'footer', 'header']):
        element.decompose()

    # Try platform-specific selectors first
    jd_text = _try_linkedin(soup)
    if not jd_text:
        jd_text = _try_indeed(soup)
    if not jd_text:
        jd_text = _try_generic(soup)

    if not jd_text or len(jd_text.strip()) < 100:
        raise ValueError(
            "Could not extract job description from URL. "
            "The page may require login. "
            "Try pasting the job description text directly."
        )

    return clean_text(jd_text)


def _try_linkedin(soup: BeautifulSoup) -> str:
    """Extract JD from LinkedIn job posting."""
    # LinkedIn job description container
    selectors = [
        '.description__text',
        '.show-more-less-html__markup',
        '[class*="description"]',
        '.jobs-description'
    ]

    for selector in selectors:
        element = soup.select_one(selector)
        if element and len(element.get_text()) > 100:
            return element.get_text(separator='\n')

    return ""


def _try_indeed(soup: BeautifulSoup) -> str:
    """Extract JD from Indeed job posting."""
    selectors = [
        '#jobDescriptionText',
        '.jobsearch-jobDescriptionText',
        '[class*="jobDescription"]'
    ]

    for selector in selectors:
        element = soup.select_one(selector)
        if element and len(element.get_text()) > 100:
            return element.get_text(separator='\n')

    return ""


def _try_generic(soup: BeautifulSoup) -> str:
    """Generic extraction for any job posting page."""
    # Strategy: Find the largest text block that looks like a JD
    candidates = []

    # Look for common job description containers
    for tag in soup.find_all(['div', 'section', 'article']):
        text = tag.get_text(separator='\n')
        if len(text) > 200:
            # Score based on job-related keywords
            score = 0
            jd_keywords = [
                'responsibilities', 'requirements', 'qualifications',
                'experience', 'skills', 'about the role', 'what you',
                'we are looking', 'job description', 'must have',
                'nice to have', 'benefits', 'salary', 'apply'
            ]
            for kw in jd_keywords:
                if kw.lower() in text.lower():
                    score += 1

            if score >= 3:
                candidates.append((score, text))

    if candidates:
        # Return the highest-scoring candidate
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]

    # Fallback: just get all body text
    body = soup.find('body')
    if body:
        return body.get_text(separator='\n')

    return ""