import importlib
from typing import List, Tuple, Set
from core.models import KeywordResult
import re


def extract_keywords(
    resume_text: str,
    jd_text: str,
    jd_skills: List[str]
) -> Tuple[List[KeywordResult], List[str], List[str]]:
    """
    Extract and compare keywords between resume and JD.

    Returns:
        - List of KeywordResult objects
        - List of matched keywords
        - List of missing keywords
    """
    # Extract keywords from JD using multiple methods
    jd_keywords = _extract_jd_keywords(jd_text, jd_skills)

    # Check which keywords appear in resume
    resume_lower = resume_text.lower()

    matched = []
    missing = []
    results = []

    for keyword, importance in jd_keywords:
        # Check for keyword presence (case-insensitive, word boundary)
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        found = bool(re.search(pattern, resume_lower))

        results.append(KeywordResult(
            keyword=keyword,
            importance=importance,
            found_in_resume=found,
            context=_find_keyword_context(jd_text, keyword)
        ))

        if found:
            matched.append(keyword)
        else:
            missing.append(keyword)

    return results, matched, missing


def _extract_jd_keywords(
    jd_text: str,
    jd_skills: List[str]
) -> List[Tuple[str, str]]:
    """
    Extract keywords from job description using TF-IDF + YAKE.

    Returns list of (keyword, importance) tuples.
    """
    keywords_with_importance: dict = {}

    # Method 1: Explicit skills from JD parser (highest importance)
    for skill in jd_skills:
        keywords_with_importance[skill.lower()] = (skill, 'high')

    # Method 2: YAKE keyword extraction
    try:
        yake = importlib.import_module("yake")
        yake_extractor = yake.KeywordExtractor(
            lan="en",
            n=2,        # max ngram size
            top=30,     # number of keywords
            dedupLim=0.7
        )
        yake_keywords = yake_extractor.extract_keywords(jd_text)

        for kw, score in yake_keywords:
            kw_clean = kw.strip()
            if (
                kw_clean.lower() not in keywords_with_importance
                and len(kw_clean) > 2
                and not kw_clean.isdigit()
            ):
                importance = 'high' if score < 0.01 else (
                    'medium' if score < 0.05 else 'low'
                )
                keywords_with_importance[kw_clean.lower()] = (
                    kw_clean, importance
                )
    except Exception:
        pass  # YAKE can fail on very short texts

    # Method 3: TF-IDF for additional terms
    try:
        TfidfVectorizer = importlib.import_module(
            "sklearn.feature_extraction.text"
        ).TfidfVectorizer
        tfidf = TfidfVectorizer(
            max_features=30,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1
        )
        tfidf_matrix = tfidf.fit_transform([jd_text])
        feature_names = tfidf.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]

        for name, score in zip(feature_names, scores):
            if (
                name.lower() not in keywords_with_importance
                and score > 0
                and len(name) > 2
            ):
                keywords_with_importance[name.lower()] = (name, 'medium')
    except Exception:
        pass

    # Sort by importance: high > medium > low
    importance_order = {'high': 0, 'medium': 1, 'low': 2}
    sorted_keywords = sorted(
        keywords_with_importance.values(),
        key=lambda x: importance_order.get(x[1], 2)
    )

    return sorted_keywords[:50]  # Cap at 50 keywords


def _find_keyword_context(jd_text: str, keyword: str) -> str:
    """Find the sentence in JD where keyword appears."""
    sentences = re.split(r'[.!?\n]', jd_text)
    keyword_lower = keyword.lower()

    for sentence in sentences:
        if keyword_lower in sentence.lower():
            cleaned = sentence.strip()
            if len(cleaned) > 20:
                return cleaned[:200]

    return "Found in job description"