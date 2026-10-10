RED_FLAGS_PROMPT = """You are an ATS system and experienced recruiter analyzing a resume for potential issues.

## RESUME TEXT:
{resume_text}

## JOB DESCRIPTION:
{jd_text}

## PDF METADATA:
- Page count: {page_count}
- Has images: {has_images}
- Has tables: {has_tables}
- File size: {file_size_kb}KB

## YOUR TASK:
Identify red flags that could cause this resume to be rejected by ATS systems or human recruiters.

Return a JSON array of red flag objects:
[
    {{
        "type": "<one of: formatting, buzzword_stuffing, gap, length, overqualified, underqualified, generic, missing_section, other>",
        "severity": "<high, medium, or low>",
        "message": "<specific, actionable feedback>"
    }}
]

CHECK FOR:
1. FORMATTING: Tables, columns, images, headers/footers that ATS can't parse
2. LENGTH: Too long (>2 pages for <10 years exp) or too short (<half page)
3. BUZZWORD STUFFING: Overused meaningless terms
4. EMPLOYMENT GAPS: Periods >3 months between roles
5. MISSING SECTIONS: No skills section, no dates on experience, etc.
6. GENERIC CONTENT: Bullets that could apply to anyone
7. OVERQUALIFICATION: Senior person applying for junior role (or vice versa)
8. QUANTIFICATION: Lack of numbers/metrics in achievements
9. CONTACT INFO: Missing email, phone, LinkedIn
10. TENSE ISSUES: Current role in past tense, or past roles in present tense

Return 3-8 red flags, ordered by severity (high first).
Return ONLY valid JSON array, no other text."""