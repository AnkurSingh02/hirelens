import re
from core.models import ATSSimulation, ATSSection
from utils.text_cleaner import extract_email, extract_phone, extract_name


def simulate_ats_parsing(
    raw_text: str,
    pdf_metadata: dict,
    sections: dict
) -> ATSSimulation:
    """
    Simulate how an ATS system would parse this resume.
    Identifies what would break and what parses correctly.
    """
    # Extract contact info
    name = extract_name(raw_text) or ""
    email = extract_email(raw_text) or ""
    phone = extract_phone(raw_text) or ""

    # Check each section
    ats_sections = []
    formatting_issues = []

    # Contact info check
    if not email:
        ats_sections.append(ATSSection(
            section_name="Email",
            status="failed",
            message="No email address detected. ATS cannot contact you."
        ))
        formatting_issues.append("Missing email address")
    else:
        ats_sections.append(ATSSection(
            section_name="Email",
            status="parsed",
            message=f"Detected: {email}"
        ))

    if not phone:
        ats_sections.append(ATSSection(
            section_name="Phone",
            status="partial",
            message="No phone number detected. Some ATS require this."
        ))
    else:
        ats_sections.append(ATSSection(
            section_name="Phone",
            status="parsed",
            message=f"Detected: {phone}"
        ))

    if not name:
        ats_sections.append(ATSSection(
            section_name="Name",
            status="failed",
            message=(
                "Could not detect candidate name. "
                "May be in an image/header that ATS can't read."
            )
        ))
        formatting_issues.append("Name not parseable — may be in header image")
    else:
        ats_sections.append(ATSSection(
            section_name="Name",
            status="parsed",
            message=f"Detected: {name}"
        ))

    # Experience section check
    if sections.get('experience'):
        # Check for dates
        date_pattern = r'\b(20\d{2}|19\d{2})\b'
        has_dates = bool(re.search(date_pattern, sections['experience']))

        if has_dates:
            ats_sections.append(ATSSection(
                section_name="Experience",
                status="parsed",
                message="Experience section found with dates."
            ))
        else:
            ats_sections.append(ATSSection(
                section_name="Experience",
                status="partial",
                message=(
                    "Experience section found but dates may not be "
                    "in standard format. Use 'Month Year - Month Year'."
                )
            ))
            formatting_issues.append(
                "Experience dates not in standard format"
            )
    else:
        ats_sections.append(ATSSection(
            section_name="Experience",
            status="failed",
            message="No experience section detected."
        ))
        formatting_issues.append("No clear experience section header")

    # Education section check
    if sections.get('education'):
        ats_sections.append(ATSSection(
            section_name="Education",
            status="parsed",
            message="Education section found."
        ))
    else:
        ats_sections.append(ATSSection(
            section_name="Education",
            status="partial",
            message="No clear education section. Some ATS require this."
        ))

    # Skills section check
    if sections.get('skills'):
        ats_sections.append(ATSSection(
            section_name="Skills",
            status="parsed",
            message="Skills section found."
        ))
    else:
        ats_sections.append(ATSSection(
            section_name="Skills",
            status="partial",
            message=(
                "No dedicated skills section. "
                "ATS may miss skills embedded in bullet points."
            )
        ))
        formatting_issues.append(
            "No dedicated skills section — add one for better ATS parsing"
        )

    # PDF formatting checks
    if pdf_metadata.get('has_images'):
        formatting_issues.append(
            "Resume contains images — ATS cannot read text in images "
            "(logos, icons, profile photos)"
        )

    if pdf_metadata.get('has_tables'):
        formatting_issues.append(
            "Resume uses tables — many ATS systems scramble table content. "
            "Consider using simple formatting."
        )

    if pdf_metadata.get('page_count', 0) > 2:
        formatting_issues.append(
            f"Resume is {pdf_metadata['page_count']} pages — "
            "keep it to 1-2 pages unless you have 10+ years experience."
        )

    if pdf_metadata.get('file_size_kb', 0) > 5000:
        formatting_issues.append(
            "File size is over 5MB — some ATS systems reject large files."
        )

    # Check for common formatting problems in text
    if '|' in raw_text and raw_text.count('|') > 5:
        formatting_issues.append(
            "Detected table/column separators (|) — "
            "likely a multi-column layout that ATS will misread."
        )

    # Generate raw text preview (what ATS actually sees)
    raw_preview = raw_text[:1500]

    return ATSSimulation(
        parsed_name=name,
        parsed_email=email,
        parsed_phone=phone,
        sections=ats_sections,
        raw_text_preview=raw_preview,
        formatting_issues=formatting_issues
    )