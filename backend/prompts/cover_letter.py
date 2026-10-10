COVER_LETTER_PROMPT = """You are an expert career coach writing a cover letter.

## JOB DESCRIPTION:
{jd_text}

## CANDIDATE'S RESUME:
{resume_text}

## ANALYSIS:
- Top matching skills: {matched_skills}
- Match score: {match_score}/100

## YOUR TASK:
Write a compelling, personalized cover letter (250-350 words).

STRUCTURE:
1. Opening: Hook that shows you understand the company's mission/challenge
2. Body paragraph 1: Your most relevant experience mapped to their top requirement
3. Body paragraph 2: A specific achievement that demonstrates impact (use numbers)
4. Body paragraph 3: Why you're excited about THIS role specifically (not generic)
5. Closing: Confident but not arrogant call to action

RULES:
- Do NOT start with "I am writing to apply for..."
- Do NOT use buzzwords like "synergy", "passionate", "rockstar"
- DO reference specific details from the job description
- DO mention specific achievements from the resume
- Keep it natural and conversational, not stiff
- Address it to "Dear Hiring Manager" unless a name is available

Return ONLY the cover letter text, no JSON wrapping."""