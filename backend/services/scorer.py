from typing import Dict, List
from core.models import CategoryScores


def compute_weighted_score(
    llm_scores: CategoryScores,
    semantic_scores: Dict[str, float],
    keyword_match_ratio: float
) -> int:
    """
    Compute final weighted score combining:
    - LLM analysis (60% weight)
    - Semantic similarity (25% weight)  
    - Keyword match ratio (15% weight)
    """
    # LLM component (average of category scores)
    llm_avg = (
        llm_scores.skills_match.score * 0.40 +
        llm_scores.experience_match.score * 0.30 +
        llm_scores.education_match.score * 0.15 +
        llm_scores.keyword_density.score * 0.15
    )

    # Semantic component (0-1 scale, convert to 0-100)
    semantic_avg = semantic_scores.get('overall', 0.5) * 100

    # Keyword component (0-1 scale, convert to 0-100)
    keyword_score = keyword_match_ratio * 100

    # Weighted combination
    final_score = (
        llm_avg * 0.60 +
        semantic_avg * 0.25 +
        keyword_score * 0.15
    )

    return int(max(0, min(100, round(final_score))))


def extract_resume_bullets(experience_text: str) -> List[str]:
    """Extract individual bullet points from experience section."""
    if not experience_text:
        return []

    bullets = []
    lines = experience_text.split('\n')

    for line in lines:
        line = line.strip()
        # Skip empty lines and section headers
        if not line or len(line) < 20:
            continue

        # Remove bullet markers
        import re
        cleaned = re.sub(r'^[\-\•\*\>\◦\▪\●\○]\s*', '', line)
        cleaned = re.sub(r'^\d+[\.\)]\s*', '', cleaned)

        # Skip lines that look like job titles or dates
        if re.match(r'^(19|20)\d{2}', cleaned):
            continue
        if len(cleaned.split()) < 4:
            continue

        if cleaned:
            bullets.append(cleaned)

    return bullets