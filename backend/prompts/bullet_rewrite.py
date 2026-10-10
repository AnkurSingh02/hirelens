BULLET_REWRITE_PROMPT = """You are an expert resume writer who specializes in ATS optimization.

## JOB DESCRIPTION:
{jd_text}

## RESUME BULLETS TO IMPROVE:
{bullets}

## YOUR TASK:
Rewrite each bullet point to better match the job description while remaining truthful.

For each bullet, return a JSON array with objects containing:
{{
    "original": "<the original bullet>",
    "rewritten": "<improved version>",
    "reasoning": "<why this rewrite is better for this specific job>"
}}

REWRITING RULES:
1. Start each bullet with a strong ACTION VERB (Architected, Developed, Optimized, Led, etc.)
2. Include QUANTIFIABLE METRICS where possible (%, $, users, time saved)
3. Incorporate KEYWORDS from the job description naturally
4. Use the XYZ formula: "Accomplished [X] as measured by [Y] by doing [Z]"
5. Keep bullets concise (1-2 lines max)
6. Do NOT fabricate experience — only reframe what's already there
7. Match the TERMINOLOGY used in the job description

Return ONLY a valid JSON array, no other text. Rewrite up to 8 bullets."""