# NorthBridge Hospital Investment Analysis

**Healthcare Data Analytics Capstone Project**  
*NorthBridge Health Investment Fund  ·  Enobakhare Osadebamwen  ·  June 2026*

---

## Project Overview

NorthBridge Health Investment Fund commissioned an independent, data-driven analysis to identify the strongest hospital investment opportunity from three Nigerian hospital candidates. This repository contains the complete analytical pipeline — from raw data cleaning through to the final investment recommendation.

## Dashboard Preview

### Executive Overview
![Executive Overview](Executive%20Overview.png)

### Financial Performance
![Financial Performance](Financial%20performance.png)

### Clinical Quality
![Clinical Quality](Clinical%20Quality.png)

### Investment Scoreboard
![Investment ScoreBoard](Investment%20ScoreBoard.png)

**Recommendation: Invest in Greenfield General Hospital (GGH)**  
Investment score: **6.36/10** · 1st of 3 candidates

---

## The Investment Question

> Which of three Nigerian hospitals — ECH, GGH, or RMC — represents the strongest long-term investment opportunity for NorthBridge Health Investment Fund?

The answer required looking beyond financial performance alone. A hospital investment is not like buying a financial instrument. Patient outcomes, clinical quality, and regulatory risk are as important to long-term value as revenue and collection rates.

---

## Key Findings at a Glance

| Metric | ECH | GGH ★ | RMC |
|--------|-----|--------|-----|
| Investment Score | 5.93/10 | **6.36/10** | 4.35/10 |
| Beds | 190 | 280 | 480 |
| Encounters (24 months) | 3,500 | 3,600 | 3,800 |
| Revenue Collected | $4.1M | $2.3M | $6.6M |
| Claim Denial Rate | 28.8% | **50.6%** | 14.6% |
| Readmission Rate | 14.1% | **9.4% ✓** | 19.7% |
| Patient Satisfaction | 6.92/10 | **7.68/10 ✓** | 5.53/10 |
| ED Wait Time | 45.9 min | **33.5 min ✓** | 61.1 min |
| 5-Year Revenue Upside | ~$2M | **~$11M+** | Declining |

**Key insight:** GGH is simultaneously getting clinically better and financially worse — both trends driven by billing process failures, not clinical failures. Targeted investment unlocks an estimated **+$2.2M additional annual revenue** at a cost of $80–120K.

---

## Repository Structure

```
northbridge-hospital-investment-analysis/
│
├── README.md                          # This file
├── .gitignore
├── requirements.txt                   # Python dependencies
│
├── python/                            # Data processing scripts
│   ├── hospital_data_cleaning.py      # Main cleaning pipeline
│   └── fix_data_quality.py            # Targeted quality fixes
│
├── data/
│   ├── raw/                           # Original hospital CSVs
│   │   ├── HospitalA_ECH.csv
│   │   ├── HospitalB_GGH.csv
│   │   └── HospitalC_RMC.csv
│   └── clean/                         # Processed output
│       └── combined_hospitals_clean.csv
│
├── dashboard/                         # Power BI assets
│   ├── NorthBridge_Dashboard.pbix
│   └── screenshots/
│       ├── 01_overview.png
│       ├── 02_financial.png
│       ├── 03_clinical.png
│       └── 04_scorecard.png
│
└── deliverables/                      # Final outputs
    ├── NorthBridge_8Slides.pptx       # Board presentation (8 slides)
    ├── GGH_Solution_Slides.pptx       # GGH problem & automation fix
    ├── Presentation_Script.docx       # 10-minute board script
    └── NorthBridge_Investment_Scorecard.xlsx
```

---

## Dataset

| Property | Detail |
|----------|--------|
| Total records | 10,900 patient encounters |
| Hospitals | 3 (ECH, GGH, RMC) |
| Period | January 2022 – December 2023 |
| Fields per record | 54 |
| Source | Simulated hospital information system exports |

### Data Quality Issues Resolved

| Issue | Rows Affected | Fix Applied |
|-------|--------------|-------------|
| `patient_gender` typos (Mal, Femal, Mae) | 786 | Standardised to Male / Female |
| `department` abbreviations (Intmed, Surg, etc.) | 193 | Expanded to full department names |
| `claim_status` variant spellings (8 variants) | 303 | Unified to canonical values |
| `patient_age` = 0 (data entry errors) | 63 | Flagged and nulled |
| Missing `discharge_date` | 1 | Flagged for manual review |

---

## Methodology

### Scoring Framework

The investment scorecard weighted six dimensions to reflect the priorities of a healthcare fund:

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Clinical Performance | 35% | Patient outcomes determine regulatory risk and long-term reputation |
| Financial Performance | 20% | Revenue sustainability and collection efficiency |
| Operational Efficiency | 20% | ED wait time, length of stay, throughput |
| Patient Satisfaction | 10% | Predictor of patient retention and referral volume |
| Revenue Cycle Health | 10% | Denial rate, trend direction, billing maturity |
| Growth Potential | 5% | Bed capacity, scalability, market position |

### Tools Used

| Tool | Purpose |
|------|---------|
| Python (pandas, numpy) | Data cleaning, merging, validation, feature engineering |
| Power BI | Interactive dashboard — 4 pages (Overview, Financial, Clinical, Scorecard) |
| Excel | Weighted investment scorecard with scenario analysis |
| PowerPoint | Board presentation and solution slides |
| N8N | Automated billing workflow prototype (WF-01 and WF-02) |

---

## The GGH Investment Thesis

GGH presents a rare and specific investment profile: **clinical excellence paired with a fixable administrative failure.**

### Why GGH

1. **Clinical foundation is unmatched** — GGH leads all 6 clinical metrics. Readmission 9.4% vs RMC's 19.7%. Satisfaction 7.68 vs RMC's 5.53. This is not a hospital that needs to be fixed clinically.

2. **Financial problem has a precise diagnosis** — The 50.6% denial rate comes from exactly 5 billing administration causes. Not one is clinical. ECH reduced its own denial rate by 6.2pp in 12 months without any external help.

3. **Revenue upside is a calculation, not a forecast** — GGH billed $7.97M over 24 months and collected $2.32M. At RMC's collection rate, GGH would collect $4.54M — a difference of **$2.22M per year already earned but not yet collected.**

### The Automation Fix (N8N)

Two automated workflows address all 5 denial causes:

**WF-01 — Pre-Submission Validator** (triggers on every new encounter)
- Checks pre-authorisation status, ICD/CPT code validity, duplicate claims, filing deadline, and documentation completeness
- Runs in under 2 seconds per claim
- Addresses 4 of 5 denial causes

**WF-02 — Filing Deadline Monitor** (runs daily at 06:00)
- Scans all open claims and calculates days to deadline
- Sends tiered alerts at 7 days (email), 3 days (SMS + email), 1 day (urgent escalation)
- Eliminates all 270 timely filing failures per year

**Financial case:** Implementation cost $80–120K. Annual recovery +$2.2M. ROI payback under 6 weeks.

### 5-Year Return Projection

| Year | Denial Rate Target | Collection Rate | Additional Revenue | Cumulative |
|------|-------------------|-----------------|-------------------|------------|
| Year 1 | ~35% | ~38% | ~$1.0M | ~$1.0M |
| Year 2 | ~22% | ~45% | ~$1.8M | ~$2.8M |
| Year 3 | ~15% | ~52% | ~$2.5M | ~$5.3M |
| Year 4 | ~15% | ~55% | ~$3.0M | ~$8.3M |
| Year 5 | ~15% | ~57% | ~$3.0M | **~$11M+** |

---

## Why Not ECH?

ECH is a well-run, genuinely improving hospital. It is not selected because:

- **Physical ceiling:** 190 licensed beds cannot be expanded without years of regulatory approval and construction. Capital cannot create beds.
- **Capped upside:** Even at 0% denial rate and full collection, ECH's revenue potential is hard-capped by capacity.
- **5-year return:** Approximately $2M — against GGH's $11M+. The opportunity cost of choosing ECH is $9M.

## Why Not RMC?

RMC has the strongest financial metrics but carries a clinical liability that compounds over time:

- **19.7% readmission rate** — 1 in 5 patients returns within 30 days. All hospitals treat the same patient severity mix, so this reflects genuine quality of care failures.
- **Regulatory risk:** Under Nigeria's NHIA framework, sustained high readmission attracts mandatory quality programmes — estimated $400–600K in Year 2–3.
- **Reputational erosion:** Satisfaction of 5.53/10 (worst of three) drives patient trust downward over time.
- **Year 1 vs Year 5:** RMC returns well in Year 1. By Year 5, value is declining and NorthBridge's brand is associated with the worst clinical outcomes in this cohort.

---

## Running the Python Scripts

### Requirements

```bash
pip install pandas numpy matplotlib seaborn
```

Or install from the requirements file:

```bash
pip install -r requirements.txt
```

### Data Cleaning Pipeline

```bash
# Step 1: Run main cleaning script
python python/hospital_data_cleaning.py

# Step 2: Apply targeted quality fixes
python python/fix_data_quality.py
```

**Output:** `data/clean/combined_hospitals_clean.csv` — 10,900 rows, 54 columns, validated and ready for analysis.

---

## Power BI Dashboard

Download and open the dashboard file from the `dashboard/` folder in Power BI Desktop.

The dashboard has 4 pages:

| Page | Content |
|------|---------|
| Overview | KPI cards, payer mix, monthly revenue trend |
| Financial Performance | Billed vs collected, denial breakdown by cause, revenue per encounter |
| Clinical Quality | Patient outcomes, all 6 clinical metrics, ED wait times, severity distribution |
| Investment Scorecard | Weighted scores, radar chart, dimension breakdown, recommendation strip |

---

## About the Analyst

**Enobakhare Osadebamwen**  
Registered Nurse · Healthcare Data Analyst  
Inducted by the Nursing and Midwifery Council of Nigeria

*Completed:* ALX Data Analysis Course · TS Academy Automation Course · Dataverse Africa Data Analysis Internship · Aspire Leadership Institute

This capstone project bridges clinical healthcare expertise with data analytics — applying the perspective of a practising nurse to the challenge of healthcare investment analysis.

---

## Licence

This project is an academic and professional capstone. All hospital data used is simulated for educational purposes. No real patient data is included.

---

*NorthBridge Health Investment Fund  ·  Hospital Investment Analysis  ·  June 2026*
