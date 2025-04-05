# Genesis – AI-Enhanced Claim Audit & Litigation Strategy System

**Genesis** is a modular, hybrid AI system built to expose suppressed injury valuations and optimize personal injury claim negotiations. Originally developed from over a decade of manual audit experience, Genesis provides structured audits, automated insurer challenge responses (ZAP), and litigation risk modeling (Prophet).

---

## 🔍 Overview

- **Origin:** Based on a 2015–2024 manual audit system used successfully in U.S. personal injury claims
- **Purpose:** Break insurer manipulation cycles powered by Claim IQ and Colossus
- **Edge:** Genesis audits the audit — exposing undervaluation using AI-backed strategy and historical offer data

---

## 🧠 Core Modules

- **GDS (General Data Scraper):** Extracts all relevant facts and dollar figures from demand packages
- **Adjuster Questions:** Strategically worded questions tailored to insurer software logic
- **RRT (Reconciliation Review Table):** Compares adjuster responses to medical fact pattern
- **Decision Point:** Recommends settlement vs. escalation using AI-calculated logic
- **Prophet:** Final escalation summary and litigation risk engine

---

## 🧰 Utility Highlights

Located in `/utils`:

- `json_loader.py` – Load JSON cleanly from `/config` or `/data`
- `text_cleaner.py` – Normalize spacing, remove legalese, improve parsing accuracy
- `section_router.py` – Modular handoff between system components
- `claim_value_tracker.py` – Tracks value shifts and logs % uplift
- `email_parser.py` – Prepares for adjuster reply intake via dedicated firm emails

---

## 📁 Directory Structure

```
/genesis
├── app.py                # Main Flask app logic
├── /modules              # Genesis core sections (GDS, RRT, etc.)
├── /utils                # Utility scripts (routing, parsing, logging)
├── /data                 # Input/output storage
├── /templates, /static   # For potential UI/UX expansion
├── /tests                # Unit tests and mock runs
```

---

## ⚙️ Setup Instructions

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/genesis-claim-audit.git
cd genesis-claim-audit

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 🧩 Modularity

Each section of Genesis can be activated, extended, or tested independently. Future add-ons like inbox parsing, WPI calculations, or ICD-10 severity heatmaps can be plugged in with zero refactor.

---

## 🎯 Strategic Vision

Genesis is a **blue ocean legal tech opportunity**—designed not to compete with demand tools, but to reveal their strategic gaps. With proper deployment, Genesis shifts control of injury claim valuation away from insurers and back to attorneys.

---

## 🧠 Creator

Developed by Andrew Weber, PlaintiffMax Pty Ltd  
[www.plaintiffmax.com](http://www.plaintiffmax.com)

---

