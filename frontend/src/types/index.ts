// ============================================================
// API RESPONSE TYPES
// ============================================================

export interface CategoryScore {
  score: number;
  matched: string[];
  missing: string[];
  details: string;
}

export interface CategoryScores {
  skills_match: CategoryScore;
  experience_match: CategoryScore;
  education_match: CategoryScore;
  keyword_density: CategoryScore;
}

export interface MissingKeyword {
  keyword: string;
  importance: "high" | "medium" | "low";
  context: string;
}

export interface BulletRewrite {
  original: string;
  rewritten: string;
  reasoning: string;
}

export interface RedFlag {
  type: string;
  severity: "high" | "medium" | "low";
  message: string;
}

export interface ATSSection {
  section_name: string;
  status: "parsed" | "partial" | "failed";
  message: string;
}

export interface ATSSimulation {
  parsed_name: string;
  parsed_email: string;
  parsed_phone: string;
  sections: ATSSection[];
  raw_text_preview: string;
  formatting_issues: string[];
}

export interface AnalysisMetadata {
  analysis_time_ms: number;
  llm_model: string;
  embedding_model: string;
  timestamp: string;
}

export interface AnalysisResponse {
  overall_score: number;
  category_scores: CategoryScores;
  missing_keywords: MissingKeyword[];
  bullet_rewrites: BulletRewrite[];
  red_flags: RedFlag[];
  cover_letter: string;
  ats_simulation: ATSSimulation | null;
  metadata: AnalysisMetadata;
}

// ============================================================
// UI STATE TYPES
// ============================================================

export type AnalysisStatus = "idle" | "uploading" | "analyzing" | "complete" | "error";

export interface AnalysisState {
  status: AnalysisStatus;
  progress: number;
  progressMessage: string;
  result: AnalysisResponse | null;
  error: string | null;
}