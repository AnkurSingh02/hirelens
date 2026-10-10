try:
    from pydantic import BaseModel, Field  # type: ignore[reportMissingImports]
except ImportError:  # pragma: no cover - fallback for Pydantic v2 compatibility
    from pydantic.v1 import BaseModel, Field  # type: ignore[reportMissingImports]

from typing import List, Optional, Dict
from datetime import datetime


# ============================================================
# REQUEST MODELS
# ============================================================

class AnalysisOptions(BaseModel):
    generate_cover_letter: bool = True
    rewrite_bullets: bool = True
    ats_simulation: bool = True


class AnalysisRequest(BaseModel):
    job_description: Optional[str] = None
    job_url: Optional[str] = None
    options: AnalysisOptions = AnalysisOptions()


# ============================================================
# INTERNAL MODELS (used between services)
# ============================================================

class ResumeSection(BaseModel):
    contact: Optional[str] = None
    summary: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    skills: Optional[str] = None
    projects: Optional[str] = None
    certifications: Optional[str] = None
    raw_text: str = ""


class JDStructured(BaseModel):
    title: str = ""
    company: str = ""
    requirements: List[str] = []
    responsibilities: List[str] = []
    qualifications: List[str] = []
    skills_required: List[str] = []
    experience_required: str = ""
    education_required: str = ""
    raw_text: str = ""


class KeywordResult(BaseModel):
    keyword: str
    importance: str = "medium"  # high, medium, low
    found_in_resume: bool = False
    context: str = ""


# ============================================================
# RESPONSE MODELS
# ============================================================

class CategoryScore(BaseModel):
    score: int = Field(ge=0, le=100)
    matched: List[str] = []
    missing: List[str] = []
    details: str = ""


class CategoryScores(BaseModel):
    skills_match: CategoryScore = CategoryScore(score=0)
    experience_match: CategoryScore = CategoryScore(score=0)
    education_match: CategoryScore = CategoryScore(score=0)
    keyword_density: CategoryScore = CategoryScore(score=0)


class MissingKeyword(BaseModel):
    keyword: str
    importance: str  # high, medium, low
    context: str


class BulletRewrite(BaseModel):
    original: str
    rewritten: str
    reasoning: str


class RedFlag(BaseModel):
    type: str  # formatting, buzzword_stuffing, gap, length, etc.
    severity: str  # high, medium, low
    message: str


class ATSSection(BaseModel):
    section_name: str
    status: str  # parsed, partial, failed
    message: str


class ATSSimulation(BaseModel):
    parsed_name: str = ""
    parsed_email: str = ""
    parsed_phone: str = ""
    sections: List[ATSSection] = []
    raw_text_preview: str = ""
    formatting_issues: List[str] = []


class AnalysisMetadata(BaseModel):
    analysis_time_ms: int = 0
    llm_model: str = ""
    embedding_model: str = ""
    timestamp: str = ""


class AnalysisResponse(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    category_scores: CategoryScores
    missing_keywords: List[MissingKeyword] = []
    bullet_rewrites: List[BulletRewrite] = []
    red_flags: List[RedFlag] = []
    cover_letter: str = ""
    ats_simulation: Optional[ATSSimulation] = None
    metadata: AnalysisMetadata = AnalysisMetadata()


# ============================================================
# DATABASE MODELS
# ============================================================

class AnalysisRecord(BaseModel):
    id: Optional[str] = None
    resume_hash: str = ""
    jd_hash: str = ""
    overall_score: int = 0
    results: Dict = {}
    created_at: Optional[str] = None