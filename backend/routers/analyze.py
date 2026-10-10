import time
import hashlib
from fastapi import APIRouter, UploadFile, File, Form, HTTPException  # type: ignore[reportMissingImports]
from typing import Optional
import json

from core.config import settings
from core.models import (
    AnalysisResponse, AnalysisMetadata,
    AnalysisOptions, MissingKeyword
)
from services.pdf_parser import parse_pdf, get_pdf_metadata
from services.jd_parser import parse_job_description
from services.scraper import scrape_job_url
from services.keyword_extractor import extract_keywords
from services.semantic_matcher import compute_semantic_scores
from services.llm_analyzer import (
    analyze_match_scoring,
    analyze_bullet_rewrites,
    generate_cover_letter,
    analyze_red_flags
)
from services.ats_simulator import simulate_ats_parsing
from services.scorer import compute_weighted_score, extract_resume_bullets


router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume_file: UploadFile = File(...),
    job_description: Optional[str] = Form(None),
    job_url: Optional[str] = Form(None),
    options: Optional[str] = Form('{}')
):
    """
    Main analysis endpoint.

    Accepts a resume PDF and job description (text or URL).
    Returns comprehensive analysis.
    """
    start_time = time.time()

    # ---- Validate inputs ----
    if not job_description and not job_url:
        raise HTTPException(
            status_code=400,
            detail="Provide either job_description text or job_url"
        )

    if not resume_file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    # Parse options
    try:
        opts = AnalysisOptions(**json.loads(options))
    except Exception:
        opts = AnalysisOptions()

    # ---- Step 1: Parse Resume ----
    try:
        file_bytes = await resume_file.read()

        if len(file_bytes) > settings.max_file_size_mb * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max {settings.max_file_size_mb}MB"
            )

        resume_sections = parse_pdf(file_bytes)
        pdf_metadata = get_pdf_metadata(file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse resume: {str(e)}"
        )

    # ---- Step 2: Get Job Description ----
    if job_url and not job_description:
        try:
            job_description = scrape_job_url(job_url)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    jd_structured = parse_job_description(job_description)

    # ---- Step 3: Keyword Extraction ----
    keyword_results, matched_kw, missing_kw = extract_keywords(
        resume_text=resume_sections.raw_text,
        jd_text=jd_structured.raw_text,
        jd_skills=jd_structured.skills_required
    )

    keyword_match_ratio = (
        len(matched_kw) / (len(matched_kw) + len(missing_kw))
        if (matched_kw or missing_kw) else 0.5
    )

    # ---- Step 4: Semantic Matching ----
    resume_dict = {
        'skills': resume_sections.skills or '',
        'experience': resume_sections.experience or '',
        'education': resume_sections.education or '',
    }
    jd_dict = {
        'skills_required': ', '.join(jd_structured.skills_required),
        'responsibilities': ' '.join(jd_structured.responsibilities),
        'education_required': jd_structured.education_required,
    }

    semantic_scores = compute_semantic_scores(resume_dict, jd_dict)

    # ---- Step 5: LLM Match Scoring ----
    overall_score, category_scores = analyze_match_scoring(
        resume_text=resume_sections.raw_text,
        jd_text=jd_structured.raw_text,
        matched_keywords=matched_kw,
        missing_keywords=missing_kw,
        semantic_score=semantic_scores.get('overall', 0.5)
    )

    # ---- Step 6: Compute Final Score ----
    final_score = compute_weighted_score(
        llm_scores=category_scores,
        semantic_scores=semantic_scores,
        keyword_match_ratio=keyword_match_ratio
    )

    # ---- Step 7: Bullet Rewrites ----
    bullet_rewrites = []
    if opts.rewrite_bullets:
        experience_bullets = extract_resume_bullets(
            resume_sections.experience or ''
        )
        if experience_bullets:
            bullet_rewrites = analyze_bullet_rewrites(
                jd_text=jd_structured.raw_text,
                bullets=experience_bullets
            )

    # ---- Step 8: Red Flags ----
    red_flags = analyze_red_flags(
        resume_text=resume_sections.raw_text,
        jd_text=jd_structured.raw_text,
        pdf_metadata=pdf_metadata
    )

    # ---- Step 9: Cover Letter ----
    cover_letter = ""
    if opts.generate_cover_letter:
        cover_letter = generate_cover_letter(
            resume_text=resume_sections.raw_text,
            jd_text=jd_structured.raw_text,
            matched_skills=matched_kw,
            match_score=final_score
        )

    # ---- Step 10: ATS Simulation ----
    ats_sim = None
    if opts.ats_simulation:
        section_dict = {
            'experience': resume_sections.experience,
            'education': resume_sections.education,
            'skills': resume_sections.skills,
        }
        ats_sim = simulate_ats_parsing(
            raw_text=resume_sections.raw_text,
            pdf_metadata=pdf_metadata,
            sections=section_dict
        )

    # ---- Step 11: Build Missing Keywords List ----
    missing_keyword_list = [
        MissingKeyword(
            keyword=kr.keyword,
            importance=kr.importance,
            context=kr.context
        )
        for kr in keyword_results
        if not kr.found_in_resume
    ]

    # ---- Build Response ----
    elapsed_ms = int((time.time() - start_time) * 1000)

    return AnalysisResponse(
        overall_score=final_score,
        category_scores=category_scores,
        missing_keywords=missing_keyword_list,
        bullet_rewrites=bullet_rewrites,
        red_flags=red_flags,
        cover_letter=cover_letter,
        ats_simulation=ats_sim,
        metadata=AnalysisMetadata(
            analysis_time_ms=elapsed_ms,
            llm_model=settings.llm_model,
            embedding_model=settings.embedding_model,
            timestamp=time.strftime('%Y-%m-%dT%H:%M:%SZ')
        )
    )