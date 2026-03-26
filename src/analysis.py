"""
analysis.py
--------------
Script 3 of 3: Statistical Analysis

Dataset : US Accidents (2016–2023) - Cleaned version
Input   : US_Accidents_Cleaned.csv  (produced by data_cleaning.py)

Description:
This script performs statistical analysis on the cleaned dataset to uncover:
- Trends over time
- Temporal accident patterns (hour, day)
- Geographic concentration (states and cities)
- Relationships between variables (weather, severity, time of day)

It combines descriptive statistics and inferential statistics
(e.g., linear regression, chi-square test, t-test)
to support data-driven conclusions.
"""

import pandas as pd
import numpy as np
from scipy import stats

# Input file path
INPUT_FILE = "data/US_Accidents_Cleaned.csv"

# -----------------------------------------------
# LOAD DATA
# -----------------------------------------------
# Loads the cleaned dataset for analysis
# low_memory=False ensures proper data type handling
# -----------------------------------------------
print("=" * 55)
print("Loading Cleaned Dataset")
print("=" * 55)

df = pd.read_csv(INPUT_FILE, low_memory=False)

# Display dataset dimensions for verification
print(f"  Rows: {df.shape[0]:,} | Columns: {df.shape[1]}")

# -----------------------------------------------
# ANALYSIS 1: Descriptive Statistics
# -----------------------------------------------
# Purpose:
# Provide an overview of the dataset including:
# - Total records
# - Coverage (years, states, cities)
# - Distribution of accidents over time and severity
# -----------------------------------------------
print("\n" + "=" * 55)
print("ANALYSIS 1: Descriptive Statistics")
print("=" * 55)

print(f"\n  Total accidents recorded : {len(df):,}")
print(f"  Time period              : {df['Year'].min()} to {df['Year'].max()}")
print(f"  States covered           : {df['State'].nunique()}")
print(f"  Unique cities            : {df['City'].nunique():,}")

# Accident counts per year (time trend overview)
print("\n  Accidents by Year:")
yearly = df["Year"].value_counts().sort_index()

# Text-based bar visualization for quick console insight
for yr, count in yearly.items():
    bar = "█" * (count // 50000)  # scale for readability
    print(f"    {yr}: {count:>8,}  {bar}")

# Summary statistics
print(f"\n  Average accidents/year  : {yearly.mean():,.0f}")
print(f"  Peak year               : {yearly.idxmax()} ({yearly.max():,} accidents)")
print(f"  Lowest year             : {yearly.idxmin()} ({yearly.min():,} accidents)")

# Severity distribution analysis
print("\n  Severity breakdown:")

# Map numeric severity to descriptive labels
sev_labels = {1:"Minor", 2:"Moderate", 3:"Serious", 4:"Severe"}

for sev, count in df["Severity"].value_counts().sort_index().items():
    pct = count / len(df) * 100
    label = sev_labels.get(sev, str(sev))
    print(f"    Severity {sev} ({label:<8}): {count:>8,}  ({pct:.1f}%)")

# -----------------------------------------------
# ANALYSIS 2: Year-over-Year Trend + Linear Regression
# -----------------------------------------------
# Purpose:
# - Measure annual growth/decline in accidents
# - Use linear regression to determine overall trend direction
# - Evaluate statistical significance of the trend
# -----------------------------------------------
print("\n" + "=" * 55)
print("ANALYSIS 2: Year-over-Year Trend (Linear Regression)")
print("=" * 55)

# Compute year-over-year percentage change
yoy = yearly.pct_change() * 100

print("\n  Year-over-Year Change (%):")
for yr, change in yoy.items():
    if pd.notna(change):
        arrow = "UP" if change > 0 else "DOWN"
        print(f"    {yr}: {arrow} {abs(change):.1f}%")

# Prepare data for regression (X = year, Y = accident count)
x = yearly.index.values.astype(float)
y = yearly.values.astype(float)

# Perform linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

trend = "INCREASING" if slope > 0 else "DECREASING"

print(f"\n  Overall trend      : {trend}")
print(f"  Slope              : {slope:,.1f} accidents/year")

# R-squared indicates how well the model fits the data
print(f"  R-squared          : {r_value**2:.4f}")

# p-value determines statistical significance
print(f"  p-value            : {p_value:.6f}")

if p_value < 0.05:
    print("  Significance       : STATISTICALLY SIGNIFICANT (p < 0.05)")
else:
    print("  Significance       : Not statistically significant (p >= 0.05)")

# -----------------------------------------------
# ANALYSIS 3: Peak Hours Analysis
# -----------------------------------------------
# Purpose:
# Identify:
# - Most dangerous time of day
# - Least risky hours
# - Rush hour accident patterns
# -----------------------------------------------
print("\n" + "=" * 55)
print("ANALYSIS 3: Peak Hours Analysis")
print("=" * 55)

# Count accidents per hour
hourly = df["Hour"].value_counts().sort_index()

# Identify peak and lowest hours
peak_hour   = hourly.idxmax()
lowest_hour = hourly.idxmin()

# Helper function: convert 24-hour format to AM/PM
def to_ampm(h):
    if h == 0:   return "12 AM"
    if h < 12:   return f"{h} AM"
    if h == 12:  return "12 PM"
    return f"{h-12} PM"

print(f"\n  Peak accident hour   : {to_ampm(peak_hour)} ({hourly.max():,} accidents)")
print(f"  Lowest accident hour : {to_ampm(lowest_hour)} ({hourly.min():,} accidents)")

# Define time groupings
morning_rush   = hourly[hourly.index.isin(range(7, 10))].sum()
afternoon_rush = hourly[hourly.index.isin(range(15, 19))].sum()
night          = hourly[
    hourly.index.isin(range(22, 24)) | hourly.index.isin(range(0, 5))
].sum()

print(f"\n  Morning rush  (7–9 AM)   : {morning_rush:,}")
print(f"  Afternoon rush (3–6 PM)  : {afternoon_rush:,}")
print(f"  Night (10 PM–4 AM)       : {night:,}")

# Compare rush hours
if afternoon_rush > morning_rush:
    print("\n  -> Afternoon rush hours produce MORE accidents than morning rush hours.")
else:
    print("\n  -> Morning rush hours produce MORE accidents than afternoon rush hours.")

# -----------------------------------------------
# ANALYSIS 4: Weekday vs Weekend Comparison
# -----------------------------------------------
# Purpose:
# Determine whether accidents are more frequent on:
# - Weekdays (work-related travel)
# - Weekends (leisure travel)
# -----------------------------------------------
print("\n" + "=" * 55)
print("ANALYSIS 4: Weekday vs Weekend Comparison")
print("=" * 55)

day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

# Count accidents per day
dow = df["Day_of_Week"].value_counts().reindex(day_order).fillna(0)

# Compute averages
weekday_avg = dow[["Monday","Tuesday","Wednesday","Thursday","Friday"]].mean()
weekend_avg = dow[["Saturday","Sunday"]].mean()

print("\n  Accidents by Day:")
for day, count in dow.items():
    tag = "(weekend)" if day in ["Saturday","Sunday"] else ""
    print(f"    {day:<10}: {int(count):>8,}  {tag}")

print(f"\n  Weekday average : {weekday_avg:,.0f}")
print(f"  Weekend average : {weekend_avg:,.0f}")

# Compare differences in percentage
diff_pct = (weekday_avg - weekend_avg) / weekend_avg * 100

if weekday_avg > weekend_avg:
    print(f"  -> Weekdays have {abs(diff_pct):.1f}% MORE accidents than weekends on average.")
else:
    print(f"  -> Weekends have {abs(diff_pct):.1f}% MORE accidents than weekdays on average.")

# -----------------------------------------------
# ANALYSIS 5: Geographic Concentration
# -----------------------------------------------
# Purpose:
# Identify regions (states and cities) with highest accident frequency
# Useful for targeting safety policies and interventions
# -----------------------------------------------
print("\n" + "=" * 55)
print("ANALYSIS 5: Geographic Concentration")
print("=" * 55)

print("\n  Top 10 States:")
for i, (state, count) in enumerate(df["State"].value_counts().head(10).items(), 1):
    pct = count / len(df) * 100
    print(f"    {i:>2}. {state:<20} {count:>8,}  ({pct:.1f}%)")

print("\n  Top 10 Cities:")
for i, (city, count) in enumerate(df["City"].value_counts().head(10).items(), 1):
    pct = count / len(df) * 100
    print(f"    {i:>2}. {city:<25} {count:>7,}  ({pct:.1f}%)")

# -----------------------------------------------
# ANALYSIS 6: Weather vs Severity (Chi-Square Test)
# -----------------------------------------------
# Purpose:
# Test whether weather conditions and accident severity are related
#
# Chi-square test:
# - H0: No relationship (independent)
# - H1: There is a relationship (dependent)
# -----------------------------------------------
print("\n" + "=" * 55)
print("ANALYSIS 6: Chi-Square Test — Weather vs Severity")
print("=" * 55)

# Use top 5 weather conditions for manageable analysis
top_weather = df[df["Weather_Condition"] != "Unknown"]["Weather_Condition"] \
                .value_counts().head(5).index.tolist()

df_sub = df[df["Weather_Condition"].isin(top_weather)]

# Create contingency table
contingency = pd.crosstab(df_sub["Weather_Condition"], df_sub["Severity"])

# Perform chi-square test
chi2, p, dof, expected = stats.chi2_contingency(contingency)

print(f"\n  Chi-Square statistic : {chi2:,.4f}")
print(f"  Degrees of freedom   : {dof}")
print(f"  p-value              : {p:.2e}")

if p < 0.05:
    print("  Result               : SIGNIFICANT association (p < 0.05)")
    print("  Interpretation       : Weather conditions influence accident severity.")
else:
    print("  Result               : No significant association (p >= 0.05)")

# -----------------------------------------------
# ANALYSIS 7: Day vs Night Severity (T-Test)
# -----------------------------------------------
# Purpose:
# Compare average severity between:
# - Daytime accidents
# - Nighttime accidents
#
# Independent t-test:
# - Tests if two group means are significantly different
# -----------------------------------------------
print("\n" + "=" * 55)
print("ANALYSIS 7: Day vs Night Severity Comparison")
print("=" * 55)

if "Sunrise_Sunset" in df.columns:

    # Compute mean severity per condition
    light = df.groupby("Sunrise_Sunset")["Severity"].mean().round(2)

    print("\n  Average Severity by Light Condition:")
    for condition, avg in light.items():
        print(f"    {condition:<10}: {avg}")

    # Separate groups
    day_sev   = df[df["Sunrise_Sunset"] == "Day"]["Severity"]
    night_sev = df[df["Sunrise_Sunset"] == "Night"]["Severity"]

    # Perform Welch’s t-test (unequal variance)
    t_stat, p_val = stats.ttest_ind(day_sev, night_sev, equal_var=False)

    print(f"\n  T-test: t = {t_stat:.4f}, p = {p_val:.2e}")

    if p_val < 0.05:
        print("  -> SIGNIFICANT difference between day and night severity.")
    else:
        print("  -> No significant difference in severity.")

# -----------------------------------------------
# FINAL SUMMARY
# -----------------------------------------------
print("\n" + "=" * 55)
print("ANALYSIS COMPLETE")
print("=" * 55)

print("  Use the findings above for your technical report.")
print("  Pair with charts from the 'figures/' folder.")