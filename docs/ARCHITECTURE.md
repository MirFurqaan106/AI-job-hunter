# AI Job Hunter — Architecture Document

## Overview
AI Job Hunter is a 24/7 personal job discovery and matching system that monitors job sources, filters for freshness (<= 24 hours), computes AI-assisted transparent match scores against candidate profiles, deduplicates postings, and dispatches high-relevance job alerts directly via WhatsApp.

---

## System Architecture Diagram

```
+------------------------------------------------------------------+
|                          JOB SOURCES                             |
|  - Email Alerts Parser (IMAP/Job Alert emails)                    |
|  - Permitted RSS / Public Job APIs                                |
|  - User-Provided Job URLs / JSON Batch Input                     |
+--------------------------------┬---------------------------------+
                                 |
                                 v
+------------------------------------------------------------------+
|                     24/7 INGESTION WORKER                        |
|                                                                  |
|   1. Freshness Check: Is job posted <= 24 hours ago?             |
|   2. Content Hashing & Deduplication (SQLite Database)           |
|   3. AI Analysis & Extraction (Gemini / Fallback Provider)       |
|   4. Transparent Match Engine (0-100 Score)                      |
|      - Role Relevance (25%)                                      |
|      - Technical Skills (30%)                                    |
|      - Experience Match (20%)                                    |
|      - Education Match (10%)                                     |
|      - Location Match (10%)                                      |
|      - Other/Freshness (5%)                                      |
+--------------------------------┬---------------------------------+
                                 |
                     Score >= 85%|
                                 v
+------------------------------------------------------------------+
|                   WHATSAPP NOTIFICATION SERVICE                  |
|  - Twilio / Official Meta WhatsApp Business API Adapter          |
|  - Console Mock Adapter (for dry-run testing)                    |
+--------------------------------┬---------------------------------+
                                 |
                                 v
                     WhatsApp Alert to Candidate
                 [ APPLY NOW -> Opens Direct Job Link ]
```

---

## Data Model Schema

### Jobs Table (`jobs`)
- `id` (INTEGER, Primary Key)
- `title` (VARCHAR)
- `company` (VARCHAR)
- `location` (VARCHAR)
- `description` (TEXT)
- `url` (VARCHAR, Unique)
- `source` (VARCHAR)
- `posted_at` (DATETIME)
- `discovered_at` (DATETIME)
- `experience_min` (INTEGER)
- `experience_max` (INTEGER)
- `remote_type` (VARCHAR)
- `salary_info` (VARCHAR)
- `content_hash` (VARCHAR, Index)
- `created_at` (DATETIME)

### Job Matches Table (`job_matches`)
- `id` (INTEGER, Primary Key)
- `job_id` (INTEGER, ForeignKey -> jobs.id)
- `profile_name` (VARCHAR)
- `match_score` (FLOAT)
- `matched_skills` (JSON/TEXT)
- `missing_skills` (JSON/TEXT)
- `explanation` (TEXT)
- `notified` (BOOLEAN)
- `notified_at` (DATETIME)
- `created_at` (DATETIME)

---

## Scoring Formula Breakdown

Total Score $S \in [0, 100]$:
$$S = W_{\text{role}} \cdot S_{\text{role}} + W_{\text{skills}} \cdot S_{\text{skills}} + W_{\text{exp}} \cdot S_{\text{exp}} + W_{\text{edu}} \cdot S_{\text{edu}} + W_{\text{loc}} \cdot S_{\text{loc}} + W_{\text{fresh}} \cdot S_{\text{fresh}}$$

Where:
- $W_{\text{role}} = 0.25$
- $W_{\text{skills}} = 0.30$
- $W_{\text{exp}} = 0.20$
- $W_{\text{edu}} = 0.10$
- $W_{\text{loc}} = 0.10$
- $W_{\text{fresh}} = 0.05$
