import axios from "axios";
import { AnalysisResponse } from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 120000, // 2 minutes — LLM calls take time
});

export async function analyzeResume(
  resumeFile: File,
  jobDescription: string,
  jobUrl?: string,
  onProgress?: (progress: number, message: string) => void
): Promise<AnalysisResponse> {
  const formData = new FormData();
  formData.append("resume_file", resumeFile);

  if (jobDescription) {
    formData.append("job_description", jobDescription);
  }

  if (jobUrl) {
    formData.append("job_url", jobUrl);
  }

  formData.append(
    "options",
    JSON.stringify({
      generate_cover_letter: true,
      rewrite_bullets: true,
      ats_simulation: true,
    })
  );

  // Simulate progress since we can't get real progress from a single POST
  let progressInterval: NodeJS.Timeout | null = null;
  if (onProgress) {
    let currentProgress = 0;
    const messages = [
      "Parsing your resume...",
      "Extracting keywords...",
      "Computing semantic similarity...",
      "AI is analyzing match quality...",
      "Generating bullet rewrites...",
      "Checking for red flags...",
      "Writing cover letter...",
      "Running ATS simulation...",
      "Compiling results...",
    ];

    progressInterval = setInterval(() => {
      if (currentProgress < 90) {
        currentProgress += Math.random() * 12;
        currentProgress = Math.min(currentProgress, 90);
        const msgIndex = Math.min(
          Math.floor(currentProgress / 11),
          messages.length - 1
        );
        onProgress(Math.round(currentProgress), messages[msgIndex]);
      }
    }, 800);
  }

  try {
    const response = await apiClient.post<AnalysisResponse>(
      "/api/analyze",
      formData,
      {
        headers: { "Content-Type": "multipart/form-data" },
      }
    );

    if (onProgress) onProgress(100, "Analysis complete!");

    return response.data;
  } catch (error: unknown) {
    const apiError = error as {
      response?: { data?: { detail?: string } };
      message?: string;
    };
    const message =
      apiError.response?.data?.detail ||
      apiError.message ||
      "Analysis failed. Please try again.";
    throw new Error(message);
  } finally {
    if (progressInterval) clearInterval(progressInterval);
  }
}

export async function checkHealth(): Promise<boolean> {
  try {
    const response = await apiClient.get("/health");
    return response.data.status === "healthy";
  } catch {
    return false;
  }
}