"""
NorthBridge Health Investment Fund — Capstone Data Preparation
Hospital Investment Analysis: ECH, GGH, RMC
Produces: combined_hospitals_clean.csv ready for Power BI
"""

import pandas as pd
import numpy as np

# ─────────────────────────────────────────
# STEP 1: LOAD THE THREE RAW CSV FILES
# Update paths to wherever your files are saved
# ─────────────────────────────────────────
ech = pd.read_csv('HospitalA_ECH.csv')
ggh = pd.read_csv('HospitalB_GGH.csv')
rmc = pd.read_csv('HospitalC_RMC.csv')

print(f"Loaded: ECH={len(ech)} rows | GGH={len(ggh)} rows | RMC={len(rmc)} rows")

# ─────────────────────────────────────────
# STEP 2: STANDARDISE EACH DATASET
# ─────────────────────────────────────────
def clean_hospital(df, hospital_code):
    df = df.copy()

    # --- Text standardisation ---
    # Normalise gender: M/Male/male → Male, F/Female/female → Female
    df['patient_gender'] = df['patient_gender'].str.strip().str.title()
    df['patient_gender'] = df['patient_gender'].replace({'M': 'Male', 'F': 'Female'})

    # Normalise admission type and department to Title Case
    df['admission_type'] = df['admission_type'].str.strip().str.title()
    df['department'] = df['department'].str.strip().str.title()

    # Normalise claim status and outcome
    df['claim_status'] = df['claim_status'].str.strip().str.title()
    df['outcome'] = df['outcome'].str.strip().str.title()

    # --- Date parsing ---
    df['admission_date']  = pd.to_datetime(df['admission_date'],  errors='coerce')
    df['discharge_date']  = pd.to_datetime(df['discharge_date'],  errors='coerce')
    df['ed_arrival_time'] = pd.to_datetime(df['ed_arrival_time'], errors='coerce')
    df['provider_seen_time'] = pd.to_datetime(df['provider_seen_time'], errors='coerce')
    df['claim_submission_date'] = pd.to_datetime(df['claim_submission_date'], errors='coerce')

    # --- Derived metrics ---
    # Length of stay in days
    df['length_of_stay_days'] = (df['discharge_date'] - df['admission_date']).dt.days

    # ED wait time in minutes (only populated for emergency encounters)
    df['ed_wait_minutes'] = (
        df['provider_seen_time'] - df['ed_arrival_time']
    ).dt.total_seconds() / 60

    # Financial derived fields
    df['collection_rate']  = df['paid_amount'] / df['billed_amount']   # 0–1 ratio per encounter
    df['write_off_amount'] = df['billed_amount'] - df['paid_amount']    # amount not collected

    # Date parts for time series analysis
    df['admission_year']    = df['admission_date'].dt.year
    df['admission_month']   = df['admission_date'].dt.month
    df['admission_quarter'] = df['admission_date'].dt.quarter
    df['admission_month_label'] = df['admission_date'].dt.to_period('M').astype(str)

    # Binary indicators as 0/1 integers (ensure consistent types)
    df['complication_flag'] = pd.to_numeric(df['complication_flag'], errors='coerce').fillna(0).astype(int)
    df['hospital_acquired_infection'] = pd.to_numeric(df['hospital_acquired_infection'], errors='coerce').fillna(0).astype(int)

    # Handle mortality_flag — GGH does NOT have this column
    if 'mortality_flag' not in df.columns:
        df['mortality_flag'] = np.nan   # null for GGH — note in README
        print(f"  WARNING: {hospital_code} has no mortality_flag — filled with null")
    else:
        df['mortality_flag'] = pd.to_numeric(df['mortality_flag'], errors='coerce')

    # Readmission binary flag (from outcome column)
    df['is_readmission'] = (df['outcome'].str.lower() == 'readmitted').astype(int)
    df['is_expired']     = (df['outcome'].str.lower() == 'expired').astype(int)

    # Claim outcome flags
    df['is_denied']  = (df['claim_status'].str.lower() == 'denied').astype(int)
    df['is_paid']    = (df['claim_status'].str.lower() == 'paid').astype(int)
    df['is_pending'] = (df['claim_status'].str.lower() == 'pending').astype(int)

    # Quality incident binary flag
    df['has_quality_incident'] = (
        df['quality_incident'].notna() & (df['quality_incident'].str.strip() != '')
    ).astype(int)

    # Age group buckets for demographic analysis
    df['age_group'] = pd.cut(
        df['patient_age'],
        bins=[0, 17, 30, 45, 60, 75, 200],
        labels=['0–17', '18–30', '31–45', '46–60', '61–75', '76+']
    )

    print(f"  {hospital_code}: cleaned {len(df)} rows | "
          f"LOS avg={df['length_of_stay_days'].mean():.1f} days | "
          f"Denial rate={df['is_denied'].mean()*100:.1f}%")
    return df

# Apply cleaning to all three
ech_clean = clean_hospital(ech, 'ECH')
ggh_clean = clean_hospital(ggh, 'GGH')
rmc_clean = clean_hospital(rmc, 'RMC')

# ─────────────────────────────────────────
# STEP 3: COMBINE INTO ONE MASTER TABLE
# ─────────────────────────────────────────
combined = pd.concat([ech_clean, ggh_clean, rmc_clean], ignore_index=True)
print(f"\nCombined dataset: {len(combined)} total rows")
print(f"Columns: {len(combined.columns)}")

# ─────────────────────────────────────────
# STEP 4: VALIDATE KEY METRICS
# ─────────────────────────────────────────
print("\n=== VALIDATION: KEY METRICS BY HOSPITAL ===")
summary = combined.groupby('hospital_code').agg(
    encounters       = ('encounter_id', 'count'),
    avg_los          = ('length_of_stay_days', 'mean'),
    avg_ed_wait      = ('ed_wait_minutes', 'mean'),
    readmission_rate = ('is_readmission', 'mean'),
    complication_rate= ('complication_flag', 'mean'),
    hai_rate         = ('hospital_acquired_infection', 'mean'),
    denial_rate      = ('is_denied', 'mean'),
    collection_rate  = ('collection_rate', 'mean'),
    avg_satisfaction = ('patient_satisfaction_score', 'mean'),
    total_billed     = ('billed_amount', 'sum'),
    total_paid       = ('paid_amount', 'sum'),
).round(4)

summary['readmission_rate_pct']  = (summary['readmission_rate'] * 100).round(1)
summary['complication_rate_pct'] = (summary['complication_rate'] * 100).round(1)
summary['hai_rate_pct']          = (summary['hai_rate'] * 100).round(1)
summary['denial_rate_pct']       = (summary['denial_rate'] * 100).round(1)
summary['collection_rate_pct']   = (summary['collection_rate'] * 100).round(1)

print(summary[[
    'encounters','avg_los','avg_ed_wait',
    'readmission_rate_pct','complication_rate_pct','hai_rate_pct',
    'denial_rate_pct','collection_rate_pct','avg_satisfaction',
    'total_billed','total_paid'
]].T.to_string())

# ─────────────────────────────────────────
# STEP 5: EXPORT FILES
# ─────────────────────────────────────────

# Main combined file for Power BI
combined.to_csv('combined_hospitals_clean.csv', index=False)
print("\nExported: combined_hospitals_clean.csv")

# Individual cleaned files
ech_clean.to_csv('ECH_clean.csv', index=False)
ggh_clean.to_csv('GGH_clean.csv', index=False)
rmc_clean.to_csv('RMC_clean.csv', index=False)
print("Exported: ECH_clean.csv | GGH_clean.csv | RMC_clean.csv")

# Summary table for scorecard reference
summary_export = combined.groupby(['hospital_code', 'admission_year']).agg(
    encounters       = ('encounter_id', 'count'),
    total_billed     = ('billed_amount', 'sum'),
    total_paid       = ('paid_amount', 'sum'),
    denial_count     = ('is_denied', 'sum'),
    readmission_count= ('is_readmission', 'sum'),
    complication_count=('complication_flag', 'sum'),
    hai_count        = ('hospital_acquired_infection', 'sum'),
    avg_satisfaction = ('patient_satisfaction_score', 'mean'),
    avg_los          = ('length_of_stay_days', 'mean'),
    avg_ed_wait      = ('ed_wait_minutes', 'mean'),
).round(2)

summary_export.to_csv('hospital_summary_by_year.csv')
print("Exported: hospital_summary_by_year.csv  (use this for your Excel scorecard)")

print("\nDone! Load combined_hospitals_clean.csv into Power BI.")
