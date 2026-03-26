"""
visualization.py
-------------------
Script 2 of 3: Data Visualization

Dataset : US Accidents (2016–2023) - Cleaned version
Input   : US_Accidents_Cleaned.csv  (produced by data_cleaning.py)
Output  : figures/ folder containing 6 PNG chart files

Description:
This script generates visual insights from the cleaned accident dataset.
It focuses on identifying patterns in time (year, hour, day),
location (state), severity, and environmental factors (weather).

Each visualization is saved as a high-resolution PNG file
for use in reports, presentations, or dashboards.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# -----------------------------------------------
# SETUP
# -----------------------------------------------
# Define file paths
INPUT_FILE = "data/US_Accidents_Cleaned.csv"
OUTPUT_DIR = "figures"

# Create output directory if it does not exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set global visualization style
# - whitegrid: clean background with gridlines
# - muted palette: professional color scheme
# - font_scale: slightly larger text for readability
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)

print("=" * 55)
print("Loading Cleaned Dataset")
print("=" * 55)

# Load cleaned dataset
df = pd.read_csv(INPUT_FILE, low_memory=False)

# Display dataset size for verification
print(f"  Rows: {df.shape[0]:,} | Columns: {df.shape[1]}")

# -----------------------------------------------
# FIGURE 1: Accidents by Year (Trend Analysis)
# -----------------------------------------------
# Purpose:
# Analyze long-term trends in accident frequency
# Helps identify whether accidents are increasing or decreasing over time
# -----------------------------------------------
print("\n[Fig 1] Accidents by Year")

# Count accidents per year and sort chronologically
yearly = df["Year"].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(10, 5))

# Line plot for trend visualization
ax.plot(yearly.index, yearly.values,
        marker="o", linewidth=2.5, color="#2a7ae2", zorder=3)

# Shaded area under curve for emphasis
ax.fill_between(yearly.index, yearly.values,
                alpha=0.12, color="#2a7ae2")

# Annotate each data point with exact values
for x, y in zip(yearly.index, yearly.values):
    ax.annotate(f"{y:,}", (x, y),
                textcoords="offset points",
                xytext=(0, 8), ha="center", fontsize=9)

# Labels and formatting
ax.set_title("US Road Accidents by Year (2016–2023)",
             fontsize=14, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Accidents")

# Format y-axis with commas (e.g., 1,000,000)
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{int(x):,}")
)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/figure1_accidents_by_year.png", dpi=150)
plt.close()

print(f"  Saved -> {OUTPUT_DIR}/figure1_accidents_by_year.png")

# -----------------------------------------------
# FIGURE 2: Accidents by Hour of Day
# -----------------------------------------------
# Purpose:
# Identify peak hours for accidents (traffic congestion patterns)
# Useful for transportation planning and safety measures
# -----------------------------------------------
print("\n[Fig 2] Accidents by Hour of Day")

# Count accidents per hour (0–23)
hourly = df["Hour"].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(12, 5))

# Bar chart with gradient colors for visual distinction
bars = ax.bar(hourly.index, hourly.values,
              color=sns.color_palette("coolwarm", 24),
              edgecolor="white", linewidth=0.5)

ax.set_title("Accidents by Hour of Day",
             fontsize=14, fontweight="bold")
ax.set_xlabel("Hour (0 = Midnight, 17 = 5 PM)")
ax.set_ylabel("Number of Accidents")

# Ensure all 24 hours are displayed
ax.set_xticks(range(0, 24))

# Format y-axis values
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{int(x):,}")
)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/figure2_accidents_by_hour.png", dpi=150)
plt.close()

print(f"  Saved -> {OUTPUT_DIR}/figure2_accidents_by_hour.png")

# -----------------------------------------------
# FIGURE 3: Accidents by Day of Week
# -----------------------------------------------
# Purpose:
# Compare accident frequency between weekdays and weekends
# Highlights behavioral patterns in driving activity
# -----------------------------------------------
print("\n[Fig 3] Accidents by Day of Week")

# Define correct chronological order of days
day_order = ["Monday","Tuesday","Wednesday","Thursday",
             "Friday","Saturday","Sunday"]

# Count accidents and reorder accordingly
dow = df["Day_of_Week"].value_counts().reindex(day_order).fillna(0)

fig, ax = plt.subplots(figsize=(10, 5))

# Color weekends differently for emphasis
colors = ["#e74c3c" if d in ["Saturday","Sunday"] else "#3498db"
          for d in day_order]

ax.bar(dow.index, dow.values, color=colors, edgecolor="white")

ax.set_title("Accidents by Day of Week",
             fontsize=14, fontweight="bold")
ax.set_xlabel("Day")
ax.set_ylabel("Number of Accidents")

# Format y-axis
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{int(x):,}")
)

# Add legend for weekday vs weekend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#3498db", label="Weekday"),
    Patch(facecolor="#e74c3c", label="Weekend")
]
ax.legend(handles=legend_elements)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/figure3_accidents_by_day.png", dpi=150)
plt.close()

print(f"  Saved -> {OUTPUT_DIR}/figure3_accidents_by_day.png")

# -----------------------------------------------
# FIGURE 4: Accident Severity Distribution
# -----------------------------------------------
# Purpose:
# Show proportion of accidents by severity level
# Helps assess how critical most accidents are
# -----------------------------------------------
print("\n[Fig 4] Severity Distribution")

# Count severity levels and map to descriptive labels
sev = df["Severity"].value_counts().sort_index()
labels = {1:"Minor", 2:"Moderate", 3:"Serious", 4:"Severe"}
sev.index = [labels[i] for i in sev.index]

fig, ax = plt.subplots(figsize=(8, 6))

# Pie chart visualization
colors = ["#2ecc71", "#f39c12", "#e67e22", "#e74c3c"]

wedges, texts, autotexts = ax.pie(
    sev.values,
    labels=sev.index,
    autopct="%1.1f%%",
    colors=colors,
    startangle=140,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5}
)

# Improve percentage text readability
for autotext in autotexts:
    autotext.set_fontsize(10)

ax.set_title("Accident Distribution by Severity",
             fontsize=14, fontweight="bold")

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/figure4_severity_distribution.png", dpi=150)
plt.close()

print(f"  Saved -> {OUTPUT_DIR}/figure4_severity_distribution.png")

# -----------------------------------------------
# FIGURE 5: Top 15 States by Accident Count
# -----------------------------------------------
# Purpose:
# Identify geographic hotspots with highest accident frequency
# Useful for policy-making and infrastructure improvements
# -----------------------------------------------
print("\n[Fig 5] Top 15 States")

# Get top 15 states with highest accident counts
top_states = df["State"].value_counts().head(15)

fig, ax = plt.subplots(figsize=(10, 7))

# Horizontal bar chart for better readability of state names
sns.barplot(x=top_states.values,
            y=top_states.index,
            palette="Blues_r", ax=ax)

ax.set_title("Top 15 US States by Accident Count",
             fontsize=14, fontweight="bold")
ax.set_xlabel("Number of Accidents")
ax.set_ylabel("State")

# Format x-axis values
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{int(x):,}")
)

# Add value labels next to bars
for i, (val, name) in enumerate(zip(top_states.values, top_states.index)):
    ax.text(val + 1000, i, f"{val:,}",
            va="center", fontsize=9)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/figure5_top_states.png", dpi=150)
plt.close()

print(f"  Saved -> {OUTPUT_DIR}/figure5_top_states.png")

# -----------------------------------------------
# FIGURE 6: Top 10 Weather Conditions
# -----------------------------------------------
# Purpose:
# Analyze environmental factors influencing accidents
# Shows which weather conditions are most associated with incidents
# -----------------------------------------------
print("\n[Fig 6] Weather Conditions")

# Exclude 'Unknown' to focus on meaningful categories
weather = df[df["Weather_Condition"] != "Unknown"]["Weather_Condition"] \
            .value_counts().head(10)

fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(x=weather.values,
            y=weather.index,
            palette="viridis", ax=ax)

ax.set_title("Top 10 Weather Conditions During Accidents",
             fontsize=14, fontweight="bold")
ax.set_xlabel("Number of Accidents")
ax.set_ylabel("Weather Condition")

# Format x-axis
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{int(x):,}")
)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/figure6_weather_conditions.png", dpi=150)
plt.close()

print(f"  Saved -> {OUTPUT_DIR}/figure6_weather_conditions.png")

# -----------------------------------------------
# FINAL MESSAGE
# -----------------------------------------------
print("\n" + "=" * 55)
print(f"All 6 figures saved to '{OUTPUT_DIR}/' folder.")
print("Run 03_analysis.py next.")
print("=" * 55)