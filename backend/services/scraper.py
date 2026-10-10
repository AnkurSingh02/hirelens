from urllib.error import URLError
from urllib.request import Request, urlopen
from html.parser import HTMLParser
import re
from utils.text_cleaner import clean_text


class _Element:
    """Minimal HTML element supporting the operations used below."""

    def __init__(self, tag: str = '', attrs=None):
        self.tag = tag
        self.attrs = dict(attrs or [])
        self.children = []

    def get_text(self, separator: str = '') -> str:
        parts = []
        for child in self.children:
            if isinstance(child, str):
                parts.append(child)
            else:
                text = child.get_text(separator)
                if text:
                    parts.append(text)
        return separator.join(parts) if separator else ''.join(parts)

    def decompose(self):
        self.children.clear()

    def _matches(self, selector: str) -> bool:
        if selector.startswith('.'):
            return selector[1:] in self.attrs.get('class', '').split()
        if selector.startswith('#'):
            return self.attrs.get('id') == selector[1:]
        attr_match = re.fullmatch(r'\[([^*\]=]+)\*=["\']([^"\']+)["\']\]', selector)
        if attr_match:
            return attr_match.group(2) in self.attrs.get(attr_match.group(1), '')
        return self.tag == selector

    def find_all(self, tags):
        if isinstance(tags, str):
            tags = [tags]
        found = []
        for child in self.children:
            if not isinstance(child, str):
                if child.tag in tags:
                    found.append(child)
                found.extend(child.find_all(tags))
        return found

    def select_one(self, selector: str):
        for child in self.children:
            if not isinstance(child, str):
                if child._matches(selector):
                    return child
                result = child.select_one(selector)
                if result:
                    return result
        return None

    def find(self, tag: str):
        return self.select_one(tag)

    def __call__(self, tags):
        return self.find_all(tags)


class _TreeParser(HTMLParser):
    _void_tags = {
        'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
        'meta', 'param', 'source', 'track', 'wbr'
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = _Element('[document]')
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = _Element(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in self._void_tags:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(_Element(tag, attrs))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


class BeautifulSoup(_Element):
    """Standard-library replacement for the small subset of bs4 used here."""

    def __init__(self, markup: str, parser: str = 'html.parser'):
        super().__init__('[document]')
        tree = _TreeParser()
        tree.feed(markup)
        self.children = tree.root.children


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
        request = Request(url, headers=headers)
        with urlopen(request, timeout=15) as response:
            encoding = response.headers.get_content_charset() or 'utf-8'
            html = response.read().decode(encoding, errors='replace')
    except (URLError, TimeoutError, OSError, ValueError) as e:
        raise ValueError(
            f"Could not fetch URL: {str(e)}. "
            "Try pasting the job description text directly."
        )

    soup = BeautifulSoup(html, 'html.parser')

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