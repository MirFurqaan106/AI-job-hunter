# AI Job Hunter — Personal 24/7 Job Discovery & WhatsApp Alert System

AI Job Hunter is an automated 24/7 personal job discovery, matching, and notification system. It monitors job sources (email job alerts, public feeds, career pages, manual URLs), filters out stale postings (>24h old), deduplicates postings, calculates transparent AI-assisted match scores against candidate profiles (MCA, 0–1 yrs exp, Bangalore/Delhi/Chandigarh/Hyderabad/Remote, Python/SQL/Power BI), and sends immediate WhatsApp notifications with direct `Apply Now` links.

---

## 🌟 Key Features

1. **24/7 Background Automation**: Runs silently in the background via Windows Task Scheduler or cloud platforms (Render/Railway/PythonAnywhere).
2. **24-Hour Freshness Constraint**: Rejects any job posted more than 24 hours ago.
3. **Transparent Match Engine (0–100%)**:
   - Role Relevance (25%)
   - Technical Skills (30%)
   - Experience Match (20%)
   - Education Match (10%)
   - Location Match (10%)
   - Freshness & Other (5%)
4. **WhatsApp Alerts**: Instant notifications containing job summary, match percentage, matched/missing skills, and clickable Apply link.
5. **Deduplication**: Content hashing & SQLite database check prevent duplicate alerts.
6. **No Auto-Apply Safety**: Gives you 100% control to apply manually on the official application page.

---

## 🚀 Installation & Setup (Windows 11 / PowerShell)

### Step 1: Clone & Setup Virtual Environment
```powershell
cd "d:\Personal Projects\whatsapp job alert"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 2: Configure Settings & Credentials
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```
Edit `config/settings.yaml` or `.env` to update your WhatsApp phone number or API keys (Gemini / Twilio).

---

## 🧪 Running Tests & Trial Execution

### 1. Run Automated Test Suite
```powershell
python -m pytest
```

### 2. Run Single Discovery Trial
```powershell
python src/main.py --once
```

### 3. Run 24/7 Continuous Daemon
```powershell
python src/main.py --daemon
```

---

## ☁️ 24/7 Cloud & Windows Daemon Deployment

### Windows Task Scheduler (Local 24/7 Service)
1. Open PowerShell as Administrator.
2. Create a background trigger to run `python src/main.py --once` every 30 minutes.

### Cloud Deployment (Render / Railway / PythonAnywhere)
- The repo includes `requirements.txt` and `Procfile`.
- Environment variables (`DATABASE_URL`, `GEMINI_API_KEY`, `TWILIO_ACCOUNT_SID`, etc.) can be set in your cloud dashboard.
