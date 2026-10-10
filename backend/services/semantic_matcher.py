from __future__ import annotations

from importlib import import_module
np = import_module('numpy')
from typing import Any, Dict
from core.config import settings

# Load model once at module level (cached)
_model = None


def _cosine_similarity(left: Any, right: Any) -> Any:
    """Compute pairwise cosine similarity without an sklearn dependency."""
    left = np.asarray(left, dtype=float)
    right = np.asarray(right, dtype=float)
    left_norms = np.linalg.norm(left, axis=1, keepdims=True)
    right_norms = np.linalg.norm(right, axis=1, keepdims=True)
    denominator = left_norms @ right_norms.T
    return np.divide(
        left @ right.T,
        denominator,
        out=np.zeros((left.shape[0], right.shape[0]), dtype=float),
        where=denominator != 0,
    )


def get_model() -> Any:
    """Lazy load the embedding model."""
    global _model
    if _model is None:
        SentenceTransformer = import_module('sentence_transformers').SentenceTransformer
        _model = SentenceTransformer(settings.embedding_model)
    return _model


def compute_semantic_scores(
    resume_sections: Dict[str, str],
    jd_sections: Dict[str, str]
) -> Dict[str, float]:
    """
    Compute semantic similarity between resume and JD sections.

    Args:
        resume_sections: Dict of section_name -> text
        jd_sections: Dict of section_name -> text

    Returns:
        Dict of section_name -> similarity_score (0-1)
    """
    model = get_model()
    scores = {}

    # Overall similarity
    resume_full = ' '.join(resume_sections.values())
    jd_full = ' '.join(jd_sections.values())

    if resume_full and jd_full:
        embeddings = model.encode([resume_full, jd_full])
        similarity = _cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        scores['overall'] = float(max(0, min(1, similarity)))

    # Section-level comparisons
    section_mappings = [
        ('skills', 'skills_required', 'skills'),
        ('experience', 'responsibilities', 'experience'),
        ('education', 'education_required', 'education'),
    ]

    for resume_key, jd_key, score_name in section_mappings:
        resume_text = resume_sections.get(resume_key, '')
        jd_text = jd_sections.get(jd_key, '')

        if resume_text and jd_text:
            embeddings = model.encode([resume_text, jd_text])
            similarity = _cosine_similarity(
                [embeddings[0]], [embeddings[1]]
            )[0][0]
            scores[score_name] = float(max(0, min(1, similarity)))
        else:
            scores[score_name] = 0.0

    return scores


def compute_bullet_similarities(
    resume_bullets: list,
    jd_requirements: list
) -> list:
    """
    Find which resume bullets best match which JD requirements.
    Returns list of (resume_bullet, best_matching_requirement, similarity).
    """
    if not resume_bullets or not jd_requirements:
        return []

    model = get_model()

    resume_embeddings = model.encode(resume_bullets)
    jd_embeddings = model.encode(jd_requirements)

    similarities = _cosine_similarity(resume_embeddings, jd_embeddings)

    results = []
    for i, bullet in enumerate(resume_bullets):
        best_match_idx = np.argmax(similarities[i])
        best_score = similarities[i][best_match_idx]

        results.append({
            'resume_bullet': bullet,
            'matched_requirement': jd_requirements[best_match_idx],
            'similarity': float(best_score)
        })

    return results