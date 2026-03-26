"""
data_cleaning.py
--------------
Script 1 of 3: Dataset Cleaning

Dataset : US Accidents (2016-2023) by Sobhan Moosavi
Source  : https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents
File    : US_Accidents_March23.csv 
Output  : US_Accidents_Cleaned.csv

Description:
This script performs preprocessing and cleaning of a large-scale traffic
accident dataset. The goal is to transform raw data into a structured,
consistent, and analysis-ready format by handling missing values,
removing irrelevant features, and extracting useful attributes.
"""

import pandas as pd
import numpy as np

# Define file paths for input (raw dataset) and output (cleaned dataset)
INPUT_FILE  = "data/US_Accidents_March23.csv"
OUTPUT_FILE = "data/US_Accidents_Cleaned.csv"

# -----------------------------------------------
# 1. LOAD DATA
# -----------------------------------------------
# Loads the dataset into a pandas DataFrame.
# The dataset contains ~7.7 million rows, so:
# - low_memory=False ensures consistent data types
# - prevents mixed-type warnings during loading
# -----------------------------------------------
print("=" * 55)
print("STEP 1: Loading Dataset")
print("=" * 55)

df = pd.read_csv(INPUT_FILE, low_memory=False)

# Display dataset size for initial inspection
print(f"\n  Rows   : {df.shape[0]:,}")
print(f"  Columns: {df.shape[1]}")

# -----------------------------------------------
# 2. DROP COLUMNS
# -----------------------------------------------
# Removes columns that are:
# - Irrelevant to analysis (e.g., IDs, descriptive text)
# - Highly missing or redundant
# - Not useful for modeling or visualization
#
# This improves performance and reduces noise.
# -----------------------------------------------
print("\n" + "=" * 55)
print("STEP 2: Dropping Unnecessary Columns")
print("=" * 55)

cols_to_drop = [
    "ID", "Source", "TMC", "End_Lat", "End_Lng",
    "Description", "Number", "Timezone", "Airport_Code",
    "Weather_Timestamp", "Civil_Twilight", "Nautical_Twilight",
    "Astronomical_Twilight", "Wind_Chill(F)", "Turning_Loop",
    "Country"
]

# Only drop columns that actually exist in dataset
existing_drops = [c for c in cols_to_drop if c in df.columns]
df.drop(columns=existing_drops, inplace=True)

print(f"\n  Dropped {len(existing_drops)} columns. Remaining: {df.shape[1]}")

# -----------------------------------------------
# 3. REMOVE DUPLICATES
# -----------------------------------------------
# Removes duplicate rows to ensure:
# - Data integrity
# - No repeated accident records
# -----------------------------------------------
print("\n" + "=" * 55)
print("STEP 3: Removing Duplicates")
print("=" * 55)

before = len(df)
df.drop_duplicates(inplace=True)

print(f"\n  Removed {before - len(df):,} duplicate rows. Remaining: {len(df):,}")

# -----------------------------------------------
# 4. HANDLE MISSING VALUES
# -----------------------------------------------
# Strategy:
# 1. Identify columns with missing values
# 2. Drop rows missing critical fields
# 3. Fill categorical/text columns with 'Unknown'
# 4. Fill numeric columns using median (robust to outliers)
# -----------------------------------------------
print("\n" + "=" * 55)
print("STEP 4: Handling Missing Values")
print("=" * 55)

# Show missing values only for columns that have nulls
print("\n  Missing values per column (only columns with nulls):")
missing = df.isnull().sum()
missing = missing[missing > 0].sort_values(ascending=False)

for col, count in missing.items():
    pct = count / len(df) * 100
    print(f"    {col:<30} {count:>8,}  ({pct:.1f}%)")

# Drop rows with missing values in critical columns
# These fields are essential for time-based and regional analysis
critical = ["Start_Time", "State", "Severity"]
before = len(df)
df.dropna(subset=critical, inplace=True)

print(f"\n  Dropped {before - len(df):,} rows missing critical fields (Start_Time, State, Severity).")

# Fill missing categorical/text values with 'Unknown'
# Prevents issues during grouping or visualization
text_fill = ["City", "Zipcode", "Street", "Side",
             "Weather_Condition", "Wind_Direction", "Sunrise_Sunset"]

for col in text_fill:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")

# Fill numeric columns with median values
# Median is preferred over mean to reduce influence of outliers
num_cols = df.select_dtypes(include=[np.number]).columns

for col in num_cols:
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].median())

print("  Remaining nulls: text columns -> 'Unknown', numeric columns -> median")

# -----------------------------------------------
# 5. PARSE DATES & EXTRACT TIME FEATURES
# -----------------------------------------------
# Converts 'Start_Time' into datetime format and extracts:
# - Year (trend analysis)
# - Month (seasonality)
# - Day of Week (weekday patterns)
# - Hour (traffic peak analysis)
# -----------------------------------------------
print("\n" + "=" * 55)
print("STEP 5: Parsing Dates & Extracting Time Features")
print("=" * 55)

# Convert to datetime; invalid parsing becomes NaT
df["Start_Time"] = pd.to_datetime(df["Start_Time"], errors="coerce")

# Remove rows where conversion failed
df.dropna(subset=["Start_Time"], inplace=True)

# Feature engineering: extract useful time components
df["Year"]        = df["Start_Time"].dt.year
df["Month"]       = df["Start_Time"].dt.month
df["Day_of_Week"] = df["Start_Time"].dt.day_name()
df["Hour"]        = df["Start_Time"].dt.hour

print("\n  Extracted: Year, Month, Day_of_Week, Hour")
print(f"  Year range in data: {df['Year'].min()} to {df['Year'].max()}")

# -----------------------------------------------
# 6. STANDARDIZE TEXT
# -----------------------------------------------
# Cleans categorical text data by:
# - Removing extra whitespace
# - Converting to Title Case for consistency
#
# Example:
# "  new york  " -> "New York"
# -----------------------------------------------
print("\n" + "=" * 55)
print("STEP 6: Standardizing Text Columns")
print("=" * 55)

for col in ["State", "City", "Weather_Condition", "Wind_Direction", "Sunrise_Sunset"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title()

print("\n  Applied: strip whitespace + title case to text columns")

# -----------------------------------------------
# 7. VALIDATE SEVERITY RANGE
# -----------------------------------------------
# Ensures that Severity values fall within expected range (1–4):
# 1 = Least severe
# 4 = Most severe
#
# Removes invalid or corrupted entries
# -----------------------------------------------
print("\n" + "=" * 55)
print("STEP 7: Validating Severity Values")
print("=" * 55)

before = len(df)

# Keep only valid severity values
df = df[df["Severity"].between(1, 4)]

print(f"\n  Removed {before - len(df):,} rows with invalid Severity values.")

# Display distribution for quick sanity check
print(f"\n  Severity distribution:\n")
print(df["Severity"].value_counts().sort_index().to_string())

# -----------------------------------------------
# 8. FINAL SUMMARY & EXPORT
# -----------------------------------------------
# Displays final dataset shape and saves cleaned dataset
# to CSV for downstream tasks (e.g., visualization, modeling)
# -----------------------------------------------
print("\n" + "=" * 55)
print("STEP 8: Final Summary & Export")
print("=" * 55)

print(f"\n  Final shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
print(f"  Total remaining nulls: {df.isnull().sum().sum():,}")

# Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

print(f"\n  Cleaned file saved -> {OUTPUT_FILE}")
print("  Run visualization.py next.")