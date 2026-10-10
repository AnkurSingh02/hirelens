<div align="center">

# 🔍 HireLens

### AI Resume Screener & ATS Optimizer

**Paste a job description. Upload your resume. Get hired.**

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-hirelens.vercel.app-blue?style=for-the-badge)](hirelens-khaki.vercel.app)
[![API Docs](https://img.shields.io/badge/📄_API_Docs-Swagger_UI-green?style=for-the-badge)](https://hirelens-api-f3mr.onrender.com/docs)
[![Built With](https://img.shields.io/badge/Built_With-Llama_3.3_70B-purple?style=for-the-badge)](https://groq.com)
[![Cost](https://img.shields.io/badge/Monthly_Cost-$0.00-brightgreen?style=for-the-badge)](#)

<br/>

> *"I built an AI tool that helps people get hired — and I'm using it to get hired myself."*

</div>

---

## 🎯 The Problem

- Job seekers apply to **200+ jobs** and get ghosted
- **75% of resumes** are rejected by ATS before a human ever sees them
- Recruiters spend **6 seconds** per resume
- Candidates have **no idea** their fancy PDF formatting breaks ATS parsers

## 💡 The Solution

HireLens analyzes your resume against any job description in **30 seconds** and tells you exactly:

| Feature | What It Does |
|---------|-------------|
| 🎯 **Match Score** | 0–100 score with breakdown by skills, experience, education, keywords |
| 🔑 **Missing Keywords** | Exact ATS keywords you're missing, ranked by importance |
| ✍️ **Bullet Rewrites** | AI rewrites your bullets to match the JD (side-by-side diff) |
| 🚩 **Red Flags** | Formatting issues, buzzword stuffing, gaps, missing sections |
| 📝 **Cover Letter** | Tailored cover letter draft generated in seconds |
| 🖥️ **ATS Simulation** | See exactly what an ATS parser sees from your resume |

---

## ⚡ Live Demo

**[→ Try it now at hirelens.vercel.app](hirelens-khaki.vercel.app)**

No signup. No API keys. No credit card. Just paste and upload.

### How it works:

```
1. Paste any job description (or LinkedIn/Indeed URL)
2. Upload your resume PDF
3. Get instant analysis with actionable fixes
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              Next.js Frontend (Vercel)              │
│         Tailwind CSS · shadcn/ui · Framer Motion    │
└──────────────────────┬──────────────────────────────┘
                       │ POST /api/analyze
                       ▼
┌─────────────────────────────────────────────────────┐
│              FastAPI Backend (Render)                │
│                                                     │
│  ┌───────────┐  ┌───────────┐  ┌────────────────┐  │
│  │ PDF Parser │  │ JD Parser │  │ URL Scraper    │  │
│  │ pdfplumber │  │ regex+NLP │  │ BeautifulSoup  │  │
│  └─────┬─────┘  └─────┬─────┘  └───────┬────────┘  │
│        └───────────┬───┘────────────────┘            │
│                    ▼                                 │
│  ┌─────────────────────────────────────────────┐    │
│  │          Analysis Pipeline                  │    │
│  │                                             │    │
│  │  1. Keyword Extraction (YAKE)               │    │
│  │  2. Semantic Matching (Groq LLM)            │    │
│  │  3. Match Scoring (Llama 3.3 70B)          │    │
│  │  4. Bullet Rewrites (Llama 3.3 70B)        │    │
│  │  5. Red Flag Detection (Llama 3.3 70B)     │    │
│  │  6. Cover Letter Gen (Llama 3.3 70B)       │    │
│  │  7. ATS Simulation (heuristic parser)       │    │
│  └─────────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│           Supabase (PostgreSQL) — Free              │
│         Analysis history · User feedback            │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Why | Cost |
|-------|-----------|-----|------|
| **LLM** | Groq (Llama 3.3 70B) | Fastest inference, 14K req/day free | $0 |
| **Keywords** | YAKE | Lightweight, no ML dependencies | $0 |
| **Backend** | Python + FastAPI | Async, fast, great DX | $0 |
| **PDF Parsing** | pdfplumber + PyMuPDF | Handles complex layouts | $0 |
| **Web Scraping** | BeautifulSoup4 | LinkedIn/Indeed JD extraction | $0 |
| **Frontend** | Next.js 14 + TypeScript | SSR, fast, great DX | $0 |
| **Styling** | Tailwind CSS + shadcn/ui | Beautiful, accessible components | $0 |
| **Animations** | Framer Motion | Spring physics, page transitions | $0 |
| **Database** | Supabase (PostgreSQL) | 500MB free, real-time | $0 |
| **Hosting** | Vercel + Render | Free tiers, auto-deploy | $0 |
| | | **Total** | **$0/mo** |

---

## 📂 Project Structure

```
hirelens/
├── backend/
│   ├── main.py                    # FastAPI entry point
│   ├── core/
│   │   ├── config.py              # Settings & env vars
│   │   └── models.py              # Pydantic schemas
│   ├── services/
│   │   ├── pdf_parser.py          # Resume PDF → structured sections
│   │   ├── jd_parser.py           # JD text → requirements/skills
│   │   ├── scraper.py             # URL → JD text (LinkedIn/Indeed)
│   │   ├── keyword_extractor.py   # YAKE keyword extraction
│   │   ├── semantic_matcher.py    # LLM-based semantic scoring
│   │   ├── llm_analyzer.py        # Groq API (scoring, rewrites, etc.)
│   │   ├── ats_simulator.py       # ATS parsing simulation
│   │   └── scorer.py              # Weighted score computation
│   ├── prompts/                   # LLM prompt templates
│   ├── routers/                   # API endpoints
│   └── utils/                     # Helpers & rate limiting
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx           # Landing page
│   │   │   └── analyze/page.tsx   # Analysis dashboard
│   │   ├── components/
│   │   │   ├── animations/        # Framer Motion components
│   │   │   ├── ScoreRing.tsx      # Animated score circle
│   │   │   ├── KeywordTable.tsx   # Found/missing keywords
│   │   │   ├── BulletRewriter.tsx # Side-by-side rewrites
│   │   │   ├── RedFlagCards.tsx   # Severity-colored alerts
│   │   │   ├── ATSSimulation.tsx  # Raw ATS view
│   │   │   └── CoverLetterPanel.tsx
│   │   └── lib/
│   │       └── api.ts             # Backend API client
│   └── package.json
│
└── README.md                      # You are here
```

---

## 🚀 Run Locally

### Prerequisites
- Python 3.11+
- Node.js 18+
- [Groq API key](https://console.groq.com) (free)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

python main.py
# → http://localhost:8000
# → http://localhost:8000/docs (Swagger UI)
```

### Frontend

```bash
cd frontend
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

npm run dev
# → http://localhost:3000
```

---

## 📊 API Example

```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "resume_file=@resume.pdf" \
  -F "job_description=We are looking for a Senior Python Developer..."
```

**Response:**

```json
{
  "overall_score": 72,
  "category_scores": {
    "skills_match": { "score": 85, "matched": ["Python", "FastAPI"], "missing": ["Kubernetes"] },
    "experience_match": { "score": 65, "details": "JD asks 5 years, resume shows ~3" },
    "education_match": { "score": 90, "details": "BS CS matches requirement" },
    "keyword_density": { "score": 48, "details": "18/37 key terms found" }
  },
  "missing_keywords": [
    { "keyword": "Kubernetes", "importance": "high", "context": "Required skills" }
  ],
  "bullet_rewrites": [
    {
      "original": "Worked on backend systems",
      "rewritten": "Architected scalable backend microservices serving 10K+ daily requests using Python and FastAPI",
      "reasoning": "JD emphasizes scalability and quantifiable impact"
    }
  ],
  "red_flags": [
    { "type": "formatting", "severity": "high", "message": "Two-column layout breaks ATS parsers" }
  ],
  "cover_letter": "Dear Hiring Manager,\n\n...",
  "ats_simulation": {
    "parsed_name": "John Doe",
    "parsed_email": "john@email.com",
    "formatting_issues": ["Images detected — ATS cannot read them"]
  }
}
```

---

## 🌐 Deployment

| Service | Platform | URL |
|---------|----------|-----|
| Frontend | Vercel | [hirelens.vercel.app](hirelens-khaki.vercel.app) |
| Backend | Render | [hirelens-api.onrender.com](https://hirelens-api-f3mr.onrender.com) |
| Database | Supabase | PostgreSQL (free tier) |

Auto-deploys on every push to `main`.

---

## 🤔 Why This Project?

**The meta-narrative:** I built an AI tool that helps people get hired — while using it to get hired myself.

**What it demonstrates:**
- 🧠 **AI/LLM Integration** — Prompt engineering with Llama 3.3 70B via Groq
- ⚡ **Full-Stack Development** — FastAPI + Next.js end-to-end
- 📄 **Document Processing** — PDF parsing, text extraction, NLP
- 🎨 **UI/UX** — Animated dashboard with Framer Motion
- 🏗️ **System Design** — Microservice architecture, rate limiting, error handling
- 💰 **Cost Optimization** — Entire stack runs on $0/month free tiers
- 🚀 **DevOps** — CI/CD with GitHub → Vercel + Render auto-deploy

---

## 📝 License

MIT — Use it, fork it, build on it.

---

<div align="center">

**If this helped you, drop a ⭐ — it helps more than you think.**

Built with ☕ and too many rejected job applications.

</div>
