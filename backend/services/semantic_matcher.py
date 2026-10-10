"""
Semantic matching using Groq LLM instead of local embeddings.
This eliminates the need for PyTorch/sentence-transformers entirely.
"""

import json
import re
from importlib import import_module
from typing import Dict
from core.config import settings

try:
    Groq = getattr(import_module("groq"), "Groq")
    client = Groq(api_key=settings.groq_api_key)
except ImportError:
    client = None


def compute_semantic_scores(
    resume_sections: Dict[str, str],
    jd_sections: Dict[str, str]
) -> Dict[str, float]:
    """
    Use LLM to estimate semantic similarity between resume and JD sections.
    Returns scores between 0.0 and 1.0.
    """
    resume_text = ' '.join(
        v for v in resume_sections.values() if v
    )[:2000]
    jd_text = ' '.join(
        v for v in jd_sections.values() if v
    )[:2000]

    if not resume_text or not jd_text:
        return {
            'overall': 0.5,
            'skills': 0.5,
            'experience': 0.5,
            'education': 0.5,
        }

    prompt = f"""You are an expert recruiter. Rate the semantic similarity between this resume and job description on a scale of 0.0 to 1.0.

RESUME EXCERPT:
{resume_text}

JOB DESCRIPTION EXCERPT:
{jd_text}

Return ONLY a JSON object with these exact keys and float values between 0.0 and 1.0:
{{"overall": 0.0, "skills": 0.0, "experience": 0.0, "education": 0.0}}

Rules:
- 0.9-1.0 = near perfect match
- 0.7-0.89 = strong match
- 0.5-0.69 = moderate match
- 0.3-0.49 = weak match
- 0.0-0.29 = no match
- Be realistic, not generous"""

    try:
        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": "Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=200
        )

        text = response.choices[0].message.content.strip()
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)

        data = json.loads(text)

        return {
            'overall': float(data.get('overall', 0.5)),
            'skills': float(data.get('skills', 0.5)),
            'experience': float(data.get('experience', 0.5)),
            'education': float(data.get('education', 0.5)),
        }

    except Exception as e:
        print(f"⚠️ Semantic scoring fallback: {e}")
        return {
            'overall': 0.5,
            'skills': 0.5,
            'experience': 0.5,
            'education': 0.5,
        }


def compute_bullet_similarities(
    resume_bullets: list,
    jd_requirements: list
) -> list:
    """
    Simplified bullet matching without local embeddings.
    Returns basic pairing based on order and keyword overlap.
    """
    if not resume_bullets or not jd_requirements:
        return []

    results = []
    for bullet in resume_bullets:
        # Simple keyword overlap scoring
        bullet_words = set(bullet.lower().split())
        best_score = 0
        best_match = jd_requirements[0]

        for req in jd_requirements:
            req_words = set(req.lower().split())
            overlap = len(bullet_words & req_words)
            total = len(bullet_words | req_words)
            score = overlap / total if total > 0 else 0

            if score > best_score:
                best_score = score
                best_match = req

        results.append({
            'resume_bullet': bullet,
            'matched_requirement': best_match,
            'similarity': min(best_score * 2, 1.0)  # Scale up slightly
        })

    return results