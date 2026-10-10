import re
from typing import List
from core.models import JDStructured
from utils.text_cleaner import clean_text


def parse_job_description(raw_text: str) -> JDStructured:
    """
    Parse raw job description text into structured format.
    """
    cleaned = clean_text(raw_text)

    return JDStructured(
        title=_extract_title(cleaned),
        company=_extract_company(cleaned),
        requirements=_extract_section(cleaned, 'requirements'),
        responsibilities=_extract_section(cleaned, 'responsibilities'),
        qualifications=_extract_section(cleaned, 'qualifications'),
        skills_required=_extract_skills(cleaned),
        experience_required=_extract_experience(cleaned),
        education_required=_extract_education(cleaned),
        raw_text=cleaned
    )


def _extract_title(text: str) -> str:
    """Extract job title from JD."""
    lines = text.strip().split('\n')
    for line in lines[:5]:
        line = line.strip()
        if line and len(line) < 80 and not re.search(r'[@.]', line):
            # Likely a title if it's short and at the top
            title_patterns = [
                r'(?i)(senior|junior|lead|staff|principal)?\s*'
                r'(software|data|product|project|devops|full.?stack|'
                r'front.?end|back.?end|machine learning|ai|cloud|'
                r'mobile|web|qa|test|security)\s*'
                r'(engineer|developer|scientist|analyst|manager|designer|architect)',
            ]
            for pattern in title_patterns:
                match = re.search(pattern, line)
                if match:
                    return line
    return ""


def _extract_company(text: str) -> str:
    """Extract company name from JD."""
    patterns = [
        r'(?i)(?:at|@|company:?)\s+([A-Z][A-Za-z0-9\s&.]+)',
        r'(?i)about\s+([A-Z][A-Za-z0-9\s&.]+?)(?:\n|\.)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            company = match.group(1).strip()
            if len(company) < 50:
                return company
    return ""


def _extract_section(text: str, section_type: str) -> List[str]:
    """Extract bullet points from a specific section."""
    section_patterns = {
        'requirements': r'(?i)(requirements?|what we.?re looking for|must have|you.?ll need)',
        'responsibilities': r'(?i)(responsibilities|what you.?ll do|role|duties|you will)',
        'qualifications': r'(?i)(qualifications?|preferred|nice to have|bonus|ideal)',
    }

    pattern = section_patterns.get(section_type, '')
    if not pattern:
        return []

    # Find the section start
    match = re.search(pattern, text)
    if not match:
        return []

    # Extract text from section start to next section or end
    start = match.end()
    next_section = re.search(
        r'\n\s*\n[A-Z][a-zA-Z\s]{5,30}:?\s*\n',
        text[start:]
    )
    end = start + next_section.start() if next_section else min(start + 2000, len(text))

    section_text = text[start:end]

    # Extract bullet points
    bullets = []
    for line in section_text.split('\n'):
        line = line.strip()
        # Remove bullet characters
        line = re.sub(r'^[\-\•\*\>\◦\▪\●\○]\s*', '', line)
        line = re.sub(r'^\d+[\.\)]\s*', '', line)
        if line and len(line) > 15:
            bullets.append(line)

    return bullets[:15]  # Cap at 15 items


def _extract_skills(text: str) -> List[str]:
    """Extract required skills/technologies from JD."""
    # Common tech skills to look for
    tech_skills = [
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C\\+\\+', 'C#',
        'Ruby', 'Go', 'Rust', 'Swift', 'Kotlin', 'PHP', 'Scala',
        'React', 'Angular', 'Vue', 'Next\\.js', 'Node\\.js', 'Express',
        'Django', 'Flask', 'FastAPI', 'Spring', 'Rails',
        'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch',
        'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform',
        'Git', 'CI/CD', 'Jenkins', 'GitHub Actions',
        'REST', 'GraphQL', 'gRPC', 'Microservices',
        'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision',
        'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy',
        'Agile', 'Scrum', 'Jira', 'Confluence',
        'Linux', 'Bash', 'Shell',
        'HTML', 'CSS', 'Tailwind', 'SASS',
        'Figma', 'Sketch',
        'Power BI', 'Tableau', 'Excel',
    ]

    found_skills = []
    for skill in tech_skills:
        if re.search(r'\b' + skill + r'\b', text, re.IGNORECASE):
            # Use the canonical form
            clean_skill = skill.replace('\\', '')
            if clean_skill not in found_skills:
                found_skills.append(clean_skill)

    return found_skills


def _extract_experience(text: str) -> str:
    """Extract years of experience required."""
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)',
        r'(?:experience|exp)\s*(?:of)?\s*(\d+)\+?\s*(?:years?|yrs?)',
        r'(?:minimum|at least|min)\s*(\d+)\s*(?:years?|yrs?)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            years = match.group(1)
            return f"{years}+ years"

    return ""


def _extract_education(text: str) -> str:
    """Extract education requirements."""
    patterns = [
        r"(?i)(bachelor'?s?|master'?s?|phd|doctorate|mba|"
        r"b\.?s\.?|m\.?s\.?|b\.?a\.?|m\.?a\.?)"
        r"\s*(?:degree)?\s*(?:in)?\s*([A-Za-z\s,]+)?",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            degree = match.group(0).strip()
            if len(degree) < 100:
                return degree

    return ""