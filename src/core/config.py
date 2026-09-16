import os
import yaml
from pathlib import Path
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = BASE_DIR / "config" / "settings.yaml"

class CandidateProfile(BaseModel):
    name: str
    degree: str
    accepted_degrees: List[str]
    target_experience_min: int
    target_experience_max: int
    accepted_experience_terms: List[str]
    target_roles: List[str]
    target_locations: List[str]
    skills: List[str]

class WeightsConfig(BaseModel):
    role: float
    skills: float
    experience: float
    education: float
    location: float
    other: float

class RulesConfig(BaseModel):
    max_job_age_hours: int
    min_match_score_for_alert: float
    alert_schedule_minutes: int
    weights: WeightsConfig

class NotificationConfig(BaseModel):
    provider: str
    whatsapp_to: Optional[str] = None
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_whatsapp_from: Optional[str] = None
    callmebot_api_key: Optional[str] = None
    meta_phone_number_id: Optional[str] = None
    meta_access_token: Optional[str] = None

class AIConfig(BaseModel):
    provider: str
    gemini_api_key: Optional[str] = None

class Settings(BaseModel):
    candidate: CandidateProfile
    rules: RulesConfig
    notification: NotificationConfig
    ai: AIConfig
    db_url: str = os.getenv("DATABASE_URL", "sqlite:///./jobs.db")

def load_settings(config_path: Path = CONFIG_PATH) -> Settings:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
    
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    # Environment overrides
    if os.getenv("GEMINI_API_KEY"):
        data["ai"]["gemini_api_key"] = os.getenv("GEMINI_API_KEY")
    if os.getenv("TWILIO_ACCOUNT_SID"):
        data["notification"]["twilio_account_sid"] = os.getenv("TWILIO_ACCOUNT_SID")
    if os.getenv("TWILIO_AUTH_TOKEN"):
        data["notification"]["twilio_auth_token"] = os.getenv("TWILIO_AUTH_TOKEN")
    if os.getenv("TWILIO_WHATSAPP_FROM"):
        data["notification"]["twilio_whatsapp_from"] = os.getenv("TWILIO_WHATSAPP_FROM")
    if os.getenv("USER_WHATSAPP_NUMBER"):
        data["notification"]["whatsapp_to"] = os.getenv("USER_WHATSAPP_NUMBER")
        
    return Settings(**data)
