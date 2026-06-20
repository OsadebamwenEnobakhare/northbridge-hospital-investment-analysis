"""
NorthBridge Capstone — Final Data Quality Fix
Fixes all 3 remaining issues in combined_hospitals_clean.csv
Run this ONCE, then refresh Power BI
"""

import pandas as pd

# ── Load ────────────────────────────────────────────────────────
df = pd.read_csv(r'C:\Users\OSADEBAMWEN\combined_hospitals_clean.csv')
print(f"Loaded: {len(df)} rows")

# ── ISSUE 1: patient_gender typos ───────────────────────────────
gender_map = {
    'Mal':   'Male',
    'Mae':   'Male',
    'Femal': 'Female',
    'Femle': 'Female',
    'Feale': 'Female',
}
before = df['patient_gender'].value_counts().to_dict()
df['patient_gender'] = df['patient_gender'].str.strip().replace(gender_map)
after = df['patient_gender'].value_counts().to_dict()
print(f"\nFix 1 — patient_gender:")
print(f"  Before: {before}")
print(f"  After:  {after}")

# ── ISSUE 2: department name variants ───────────────────────────
dept_map = {
    'Intmed':       'Internal Medicine',
    'Int.Medicine': 'Internal Medicine',
    'Gen Surge':    'General Surgery',
    'Surgery':      'General Surgery',
    'Emergency':    'Emergency Medicine',
}
before_dept = df['department'].value_counts().to_dict()
df['department'] = df['department'].str.strip().replace(dept_map)
print(f"\nFix 2 — department (after standardisation):")
print(df['department'].value_counts().to_string())

# ── ISSUE 3: claim_status appeal variants ───────────────────────
appeal_variants = [
    'Appeal', 'Appealed', 'Appealing',
    'Appealling', 'Appell', 'Under Appeal'
]
before_claims = df['claim_status'].value_counts().to_dict()
df['claim_status'] = df['claim_status'].str.strip().replace(
    {v: 'Under Appeal' for v in appeal_variants}
)
print(f"\nFix 3 — claim_status (after standardisation):")
print(df['claim_status'].value_counts().to_string())

# ── Re-derive is_pending since claim_status changed ─────────────
# Under Appeal rows are NOT pending payments, keep them separate
df['is_under_appeal'] = (df['claim_status'] == 'Under Appeal').astype(int)
df['is_pending']      = (df['claim_status'] == 'Pending').astype(int)

# ── Final validation ────────────────────────────────────────────
print("\n" + "="*50)
print("FINAL VALIDATION")
print("="*50)
print(f"Total rows:              {len(df)}")
print(f"Unique genders:          {sorted(df['patient_gender'].unique().tolist())}")
print(f"Unique departments:      {sorted(df['department'].unique().tolist())}")
print(f"Unique claim statuses:   {sorted(df['claim_status'].unique().tolist())}")
print(f"Duplicate encounter IDs: {df['encounter_id'].duplicated().sum()}")
print(f"Negative billed amounts: {(df['billed_amount']<0).sum()}")
print(f"Paid > Billed rows:      {(df['paid_amount']>df['billed_amount']).sum()}")

# Key metrics — should not have changed
for h in ['ECH','GGH','RMC']:
    hdf = df[df['hospital_code']==h]
    paid   = hdf['paid_amount'].sum()
    billed = hdf['billed_amount'].sum()
    denied = (hdf['claim_status']=='Denied').sum()
    print(f"\n{h}: collection={paid/billed*100:.1f}% | "
          f"denial={(denied/len(hdf))*100:.1f}% | "
          f"encounters={len(hdf)}")

# ── Export ──────────────────────────────────────────────────────
output_path = r'C:\Users\OSADEBAMWEN\combined_hospitals_clean.csv'
df.to_csv(output_path, index=False)
print(f"\n✓ Saved to: {output_path}")
print("Go to Power BI → Home ribbon → click Refresh")
