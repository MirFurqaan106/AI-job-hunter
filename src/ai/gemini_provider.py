import json
import logging
from src.ai.provider import BaseAIProvider, JobAnalysisResult, MockAIProvider

logger = logging.getLogger(__name__)

class GeminiAIProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.fallback = MockAIProvider()
        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel("gemini-1.5-flash")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini API: {e}. Falling back to mock provider.")
                self.model = None
        else:
            self.model = None

    def analyze_job_description(self, raw_description: str) -> JobAnalysisResult:
        if not self.model:
            return self.fallback.analyze_job_description(raw_description)
            
        prompt = f"""
Analyze the following job description and output JSON strictly matching this schema:
{{
  "job_title": "string",
  "company": "string",
  "location": "string",
  "experience_min": int,
  "experience_max": int,
  "education_required": "string",
  "remote_type": "On-site" | "Hybrid" | "Remote",
  "salary_info": "string",
  "required_skills": ["string"],
  "preferred_skills": ["string"],
  "summary": "string"
}}

Job Description:
{raw_description}
"""
        try:
            response = self.model.generate_content(prompt)
            clean_json = response.text.strip().removeprefix("```json").removesuffix("```").strip()
            data = json.loads(clean_json)
            return JobAnalysisResult(**data)
        except Exception as e:
            logger.error(f"Gemini API analysis failed: {e}. Falling back to heuristic mock.")
            return self.fallback.analyze_job_description(raw_description)
