from typing import List, Dict, Any, Tuple
from src.core.config import Settings, CandidateProfile

class ScoringEngine:
    def __init__(self, settings: Settings):
        self.profile: CandidateProfile = settings.candidate
        self.weights = settings.rules.weights

    def evaluate_role_match(self, job_title: str) -> float:
        title_lower = job_title.lower()
        for target in self.profile.target_roles:
            target_lower = target.lower()
            if target_lower in title_lower or title_lower in target_lower:
                return 1.0
        
        # Partial match heuristic
        keywords = ["data", "analyst", "genai", "ai", "python", "software", "developer", "engineer", "operations"]
        matches = sum(1 for kw in keywords if kw in title_lower)
        if matches >= 2:
            return 0.75
        elif matches == 1:
            return 0.5
        return 0.2

    def evaluate_skill_match(self, job_description: str, job_skills: List[str]) -> Tuple[float, List[str], List[str]]:
        profile_skills_lower = {s.lower(): s for s in self.profile.skills}
        
        # Collect skills from job_skills parameter or scan description
        detected_job_skills = set(s.lower() for s in job_skills)
        desc_lower = job_description.lower()
        
        for sk in profile_skills_lower.keys():
            if sk in desc_lower:
                detected_job_skills.add(sk)
                
        if not detected_job_skills:
            return 0.5, [], []

        matched = []
        missing = []

        for skill in detected_job_skills:
            if skill in profile_skills_lower:
                matched.append(profile_skills_lower[skill])
            else:
                missing.append(skill.title())

        matched_count = len(matched)
        total_detected = len(detected_job_skills)
        
        score = min(1.0, matched_count / max(1, total_detected)) if total_detected > 0 else 0.5
        return score, matched, missing

    def evaluate_experience_match(self, exp_min: int, exp_max: int, job_description: str) -> float:
        # Candidate target: 0-1 years
        if exp_min <= 1:
            return 1.0
        elif exp_min == 2:
            return 0.6
        elif exp_min >= 3:
            return 0.2
        
        desc_lower = job_description.lower()
        for term in self.profile.accepted_experience_terms:
            if term in desc_lower:
                return 1.0
                
        return 0.5

    def evaluate_education_match(self, education_req: str, job_description: str) -> float:
        text = f"{education_req} {job_description}".lower()
        for deg in self.profile.accepted_degrees:
            if deg.lower() in text:
                return 1.0
        return 0.6 # Neutral default if not explicitly restricting degree

    def evaluate_location_match(self, job_location: str, remote_type: str) -> float:
        loc_text = f"{job_location} {remote_type}".lower()
        for target_loc in self.profile.target_locations:
            if target_loc.lower() in loc_text:
                return 1.0
        if "remote" in loc_text or "hybrid" in loc_text:
            return 0.9
        return 0.4

    def calculate_match_score(self, job_data: Dict[str, Any]) -> Tuple[float, List[str], List[str], str]:
        title = job_data.get("title", "")
        desc = job_data.get("description", "")
        job_skills = job_data.get("skills", [])
        exp_min = job_data.get("experience_min", 0)
        exp_max = job_data.get("experience_max", 1)
        edu = job_data.get("education_required", "")
        location = job_data.get("location", "")
        remote_type = job_data.get("remote_type", "On-site")

        s_role = self.evaluate_role_match(title)
        s_skill, matched_skills, missing_skills = self.evaluate_skill_match(desc, job_skills)
        s_exp = self.evaluate_experience_match(exp_min, exp_max, desc)
        s_edu = self.evaluate_education_match(edu, desc)
        s_loc = self.evaluate_location_match(location, remote_type)
        s_other = 1.0 # Default full score for fresh job

        weighted_score = (
            self.weights.role * s_role +
            self.weights.skills * s_skill +
            self.weights.experience * s_exp +
            self.weights.education * s_edu +
            self.weights.location * s_loc +
            self.weights.other * s_other
        ) * 100.0

        final_score = round(min(100.0, max(0.0, weighted_score)), 1)

        # Generate transparent explanation
        explanation = (
            f"Role match: {int(s_role*100)}% | Skill match: {int(s_skill*100)}% "
            f"| Exp match: {int(s_exp*100)}% | Edu match: {int(s_edu*100)}% | Loc match: {int(s_loc*100)}%"
        )

        return final_score, matched_skills, missing_skills, explanation
