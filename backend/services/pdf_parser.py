import pdfplumber
import re
import io
from typing import Optional
from core.models import ResumeSection
from utils.text_cleaner import clean_text, extract_email, extract_phone, extract_name


# Section headers we look for in resumes
SECTION_PATTERNS = {
    'summary': r'(?i)(summary|objective|profile|about\s*me|professional\s*summary)',
    'experience': r'(?i)(experience|work\s*history|employment|professional\s*experience|work\s*experience)',
    'education': r'(?i)(education|academic|qualification|degree)',
    'skills': r'(?i)(skills|technical\s*skills|competencies|technologies|tech\s*stack|proficiency)',
    'projects': r'(?i)(projects|portfolio|personal\s*projects|key\s*projects)',
    'certifications': r'(?i)(certifications?|licenses?|credentials|accreditations?)',
}


def parse_pdf(file_bytes: bytes) -> ResumeSection:
    """
    Parse a PDF resume into structured sections.

    Args:
        file_bytes: Raw bytes of the PDF file

    Returns:
        ResumeSection with classified content
    """
    # Extract raw text from PDF
    raw_text = _extract_text_from_pdf(file_bytes)

    if not raw_text or len(raw_text.strip()) < 50:
        raise ValueError(
            "Could not extract text from PDF. "
            "The file may be image-based or corrupted."
        )

    # Clean the text
    cleaned_text = clean_text(raw_text)

    # Classify into sections
    sections = _classify_sections(cleaned_text)

    # Extract contact info
    email = extract_email(cleaned_text)
    phone = extract_phone(cleaned_text)
    name = extract_name(cleaned_text)

    contact_info = ""
    if name:
        contact_info += f"Name: {name}\n"
    if email:
        contact_info += f"Email: {email}\n"
    if phone:
        contact_info += f"Phone: {phone}\n"

    return ResumeSection(
        contact=contact_info if contact_info else None,
        summary=sections.get('summary'),
        experience=sections.get('experience'),
        education=sections.get('education'),
        skills=sections.get('skills'),
        projects=sections.get('projects'),
        certifications=sections.get('certifications'),
        raw_text=cleaned_text
    )


def _extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF using pdfplumber."""
    text_parts = []

    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")

    return '\n'.join(text_parts)


def _classify_sections(text: str) -> dict:
    """
    Split resume text into sections based on header detection.

    Strategy:
    1. Find all section headers and their positions
    2. Extract text between consecutive headers
    3. Assign to appropriate section
    """
    sections = {}
    header_positions = []

    lines = text.split('\n')

    # Find section headers and their line numbers
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue

        for section_name, pattern in SECTION_PATTERNS.items():
            if re.match(pattern, stripped) and len(stripped) < 60:
                header_positions.append({
                    'section': section_name,
                    'line_num': i,
                    'header_text': stripped
                })
                break

    # If no headers found, try to do basic classification
    if not header_positions:
        return _fallback_classification(text)

    # Extract text between headers
    for idx, header in enumerate(header_positions):
        start_line = header['line_num'] + 1

        if idx + 1 < len(header_positions):
            end_line = header_positions[idx + 1]['line_num']
        else:
            end_line = len(lines)

        section_text = '\n'.join(lines[start_line:end_line]).strip()

        if section_text:
            sections[header['section']] = section_text

    # Everything before the first header is likely contact/summary
    if header_positions:
        first_header_line = header_positions[0]['line_num']
        pre_header_text = '\n'.join(lines[:first_header_line]).strip()
        if pre_header_text and 'summary' not in sections:
            # Check if it's long enough to be a summary
            if len(pre_header_text) > 100:
                sections['summary'] = pre_header_text

    return sections


def _fallback_classification(text: str) -> dict:
    """
    When no clear section headers are found,
    use heuristics to classify content.
    """
    sections = {}

    # Look for skill-like patterns (comma-separated technical terms)
    skill_pattern = r'(?:Python|Java|JavaScript|React|SQL|AWS|Docker|Git|Node|TypeScript|C\+\+|Ruby|Go|Rust|Kubernetes|MongoDB|PostgreSQL)'
    skill_matches = re.findall(skill_pattern, text, re.IGNORECASE)
    if skill_matches:
        sections['skills'] = ', '.join(list(set(skill_matches)))

    # Look for education patterns
    edu_pattern = r'(?:Bachelor|Master|PhD|B\.S\.|M\.S\.|B\.A\.|M\.A\.|MBA|University|College|Institute|Degree)'
    if re.search(edu_pattern, text, re.IGNORECASE):
        # Find the paragraph containing education
        paragraphs = text.split('\n\n')
        for para in paragraphs:
            if re.search(edu_pattern, para, re.IGNORECASE):
                sections['education'] = para
                break

    # The rest is likely experience
    sections['experience'] = text

    return sections


def get_pdf_metadata(file_bytes: bytes) -> dict:
    """Extract PDF metadata for ATS simulation."""
    metadata = {
        'page_count': 0,
        'has_images': False,
        'has_tables': False,
        'file_size_kb': len(file_bytes) / 1024
    }

    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            metadata['page_count'] = len(pdf.pages)

            for page in pdf.pages:
                if page.images:
                    metadata['has_images'] = True
                if page.extract_tables():
                    metadata['has_tables'] = True
    except Exception:
        pass

    return metadata