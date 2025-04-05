# Genesis Reboot

Genesis Reboot is an AI-enhanced claim audit system designed to expose undervaluation tactics used by insurers. Built from over a decade of manual audit insights, it automates demand package extraction, claim analysis, and litigation prediction through a hybrid of rule-based logic and OpenAI integration.

## 🚀 Purpose

Plaintiff attorneys often face suppressed claim valuations due to insurer-side software like Colossus or Claim IQ. Genesis Reboot levels the playing field by:
- Extracting structured data from demand packages
- Auditing adjuster behavior through strategic traps
- Triggering litigation escalation recommendations
- Forcing insurers to justify suppressed offers

---

## 🧩 Core Modules

- **GDS (Genesis Data Scan)**: Extracts injuries, ICD-10 codes, delay triggers, and value drivers from plaintiff demand packages.
- **RRT (Reconciliation Review Table)**: Compares adjuster responses with medically assessed data.
- **ZAP (Zero Acceptance Protocol)**: Auto-generates AI-backed responses to baseless adjuster defenses.
- **Prophet**: Projects litigation outcomes if undervaluation is not corrected.

---

## 🛠️ Installation

```bash
git clone https://github.com/andyweb67/genesis-reboot.git
cd genesis-reboot
python -m venv venv
venv\Scripts\activate   # On Windows
pip install -r requirements.txt
