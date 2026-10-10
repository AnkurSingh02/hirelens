from datetime import time
import json
import re
from typing import Dict, List, Optional
from groq import Groq, RateLimitError  # type: ignore[import-not-found]
from core.config import settings
from core.models import (
    CategoryScores, CategoryScore,
    BulletRewrite, RedFlag, MissingKeyword
)
from prompts.match_scoring import MATCH_SCORING_PROMPT
from prompts.bullet_rewrite import BULLET_REWRITE_PROMPT
from prompts.cover_letter import COVER_LETTER_PROMPT
from prompts.red_flags import RED_FLAGS_PROMPT


# Initialize Groq client
client = Groq(api_key=settings.groq_api_key)


def _call_llm(prompt: str, max_tokens: int = 4000) -> str:
    """Make a call to Groq with retry handling for temporary rate limits."""

    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=settings.llm_model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a precise AI assistant. "
                            "Always return valid JSON when asked. "
                            "Never include markdown formatting or code blocks."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content.strip()

        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise RuntimeError(
                    "Groq rate limit reached. Please try again in a few seconds."
                ) from e

            wait_time = 5 * (attempt + 1)
            time.sleep(wait_time)

        except Exception as e:
            raise RuntimeError(f"LLM call failed: {str(e)}") from e

    raise RuntimeError("LLM call failed after multiple retries.")


def _parse_json_response(response: str) -> dict | list:
    """Parse JSON from LLM response, handling common issues."""
    # Remove markdown code blocks if present
    response = re.sub(r'```json\s*', '', response)
    response = re.sub(r'```\s*', '', response)
    response = response.strip()

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # Try to find JSON within the response
        json_match = re.search(r'[\[{].*[\]}]', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        raise ValueError(f"Could not parse LLM response as JSON: {response[:200]}")


def analyze_match_scoring(
    resume_text: str,
    jd_text: str,
    matched_keywords: List[str],
    missing_keywords: List[str],
    semantic_score: float
) -> tuple:
    """
    Get match scores from LLM.
    Returns (overall_score, CategoryScores)
    """
    prompt = MATCH_SCORING_PROMPT.format(
        resume_text=resume_text[:4000],
        jd_text=jd_text[:3000],
        matched_keywords=', '.join(matched_keywords[:20]),
        missing_keywords=', '.join(missing_keywords[:20]),
        semantic_score=f"{semantic_score:.2f}"
    )

    response = _call_llm(prompt)
    data = _parse_json_response(response)

    overall_score = int(data.get('overall_score', 50))

    category_scores = CategoryScores(
        skills_match=CategoryScore(
            score=int(data.get('skills_match', {}).get('score', 50)),
            matched=data.get('skills_match', {}).get('matched', []),
            missing=data.get('skills_match', {}).get('missing', []),
            details=data.get('skills_match', {}).get('details', '')
        ),
        experience_match=CategoryScore(
            score=int(data.get('experience_match', {}).get('score', 50)),
            matched=data.get('experience_match', {}).get('matched', []),
            missing=data.get('experience_match', {}).get('missing', []),
            details=data.get('experience_match', {}).get('details', '')
        ),
        education_match=CategoryScore(
            score=int(data.get('education_match', {}).get('score', 50)),
            matched=data.get('education_match', {}).get('matched', []),
            missing=data.get('education_match', {}).get('missing', []),
            details=data.get('education_match', {}).get('details', '')
        ),
        keyword_density=CategoryScore(
            score=int(data.get('keyword_density', {}).get('score', 50)),
            details=data.get('keyword_density', {}).get('details', '')
        )
    )

    return overall_score, category_scores


def analyze_bullet_rewrites(
    jd_text: str,
    bullets: List[str]
) -> List[BulletRewrite]:
    """Get bullet point rewrites from LLM."""
    if not bullets:
        return []

    # Take top 8 bullets
    selected_bullets = bullets[:8]
    bullets_text = '\n'.join(
        f"{i+1}. {b}" for i, b in enumerate(selected_bullets)
    )

    prompt = BULLET_REWRITE_PROMPT.format(
        jd_text=jd_text[:3000],
        bullets=bullets_text
    )

    response = _call_llm(prompt)
    data = _parse_json_response(response)

    rewrites = []
    if isinstance(data, list):
        for item in data:
            rewrites.append(BulletRewrite(
                original=item.get('original', ''),
                rewritten=item.get('rewritten', ''),
                reasoning=item.get('reasoning', '')
            ))

    return rewrites


def generate_cover_letter(
    resume_text: str,
    jd_text: str,
    matched_skills: List[str],
    match_score: int
) -> str:
    """Generate a tailored cover letter."""
    prompt = COVER_LETTER_PROMPT.format(
        resume_text=resume_text[:3000],
        jd_text=jd_text[:3000],
        matched_skills=', '.join(matched_skills[:10]),
        match_score=match_score
    )

    return _call_llm(prompt, max_tokens=2000)


def analyze_red_flags(
    resume_text: str,
    jd_text: str,
    pdf_metadata: dict
) -> List[RedFlag]:
    """Detect red flags in the resume."""
    prompt = RED_FLAGS_PROMPT.format(
        resume_text=resume_text[:4000],
        jd_text=jd_text[:2000],
        page_count=pdf_metadata.get('page_count', 'unknown'),
        has_images=pdf_metadata.get('has_images', False),
        has_tables=pdf_metadata.get('has_tables', False),
        file_size_kb=round(pdf_metadata.get('file_size_kb', 0), 1)
    )

    response = _call_llm(prompt)
    data = _parse_json_response(response)

    flags = []
    if isinstance(data, list):
        for item in data:
            flags.append(RedFlag(
                type=item.get('type', 'other'),
                severity=item.get('severity', 'medium'),
                message=item.get('message', '')
            ))

    return flags