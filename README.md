<div align="center">

# Road Stats

Temporal and Geographic Data Analysis of US Road Accidents (2016-2023)

[**Technical Paper »**](https://drive.google.com/file/d/1zLL274hqoCkYknEOS0YWuYJinHiTjbZT/view?usp=sharing)

[Report Bug](https://github.com/feiryrej/road-stats/issues)
·
[Request Feature](https://github.com/feiryrej/road-stats/pulls)

</div>

## Overview

This project performs exploratory data analysis and statistical inference on the [US Accidents (2016-2023)](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents) dataset by Sobhan Moosavi. The dataset contains approximately 7.7 million accident records with attributes covering time, location, severity, and weather conditions across 49 US states. The pipeline covers the full data analysis workflow: cleaning, visualization, and statistical analysis.

This repository is the code companion to the technical report *"Temporal and Geographic Data Analysis of US Road Accidents"* submitted to the Polytechnic University of the Philippines for Current Trends and Topics in Computing (March 2026).

## Background

Road traffic accidents remain a significant public safety concern worldwide, contributing to injuries, fatalities, and economic losses. Understanding patterns in accident occurrence is essential for developing effective traffic management strategies and safety interventions. This project applies data cleaning, visualization, and statistical analysis techniques to extract meaningful insights that can support data-driven decision-making in traffic safety.

### Key Features

- **Data Cleaning Pipeline**: Eight-step preprocessing pipeline handling missing values, duplicates, datetime parsing, text standardization, and severity validation
- **Six Visualizations**: Charts covering yearly trends, hourly distribution, day-of-week patterns, severity distribution, geographic concentration, and weather conditions
- **Statistical Analysis**: Seven analyses including linear regression for trend detection, chi-square test for weather-severity association, and Welch's t-test for day vs. night severity comparison
- **Reproducible Workflow**: Three standalone scripts that run in sequence, each producing output consumed by the next

## Pipeline

The pipeline runs in three sequential scripts, all reading from and writing to the `data/` and `figures/` directories.

**Script 1: `data_cleaning.py`** reads the raw CSV and runs eight preprocessing steps: dropping irrelevant columns (ID, Source, TMC, Description, and others), removing duplicate records, handling missing values (critical fields are required, text fields are filled with "Unknown", numeric fields are imputed with the median), parsing `Start_Time` into datetime and extracting `Year`, `Month`, `Day_of_Week`, and `Hour`, standardizing categorical text to title case, and validating that `Severity` falls within 1 to 4. Outputs `US_Accidents_Cleaned.csv`.

**Script 2: `visualization.py`** reads the cleaned CSV and generates six figures saved as PNG files to the `figures/` directory. Charts cover yearly trends (line chart with shaded area under curve and annotated data points), hourly distribution (bar chart with coolwarm palette), day-of-week comparison (weekdays in blue, weekends in red), severity distribution (pie chart with four color levels), top 15 states by accident count (horizontal bar chart), and top 10 weather conditions (bar chart with viridis palette, excluding "Unknown").

**Script 3: `analysis.py`** performs seven statistical analyses on the cleaned dataset: descriptive statistics (total records, year range, state and city coverage, severity breakdown), year-over-year trend with linear regression (slope, R-squared, p-value), peak hours analysis (morning rush 7-9 AM, afternoon rush 3-6 PM, and night groupings), weekday vs. weekend comparison, geographic concentration by state and city, a chi-square test on weather conditions vs. accident severity, and a Welch's t-test comparing day vs. night severity using the `Sunrise_Sunset` field.

## Project Structure

```
road-stats/
├── data/
│   ├── US_Accidents_March23.csv        # Raw dataset (download separately from Kaggle)
│   └── US_Accidents_Cleaned.csv        # Produced by data_cleaning.py
├── figures/
│   ├── figure1_accidents_by_year.png
│   ├── figure2_accidents_by_hour.png
│   ├── figure3_accidents_by_day.png
│   ├── figure4_severity_distribution.png
│   ├── figure5_top_states.png
│   └── figure6_weather_conditions.png
├── src/
│   ├── data_cleaning.py                # Script 1 of 3
│   ├── visualization.py                # Script 2 of 3
│   └── analysis.py                     # Script 3 of 3
└── .gitignore
```

## Visualizations

### Accidents By Year
![Accidents By Year](https://raw.githubusercontent.com/feiryrej/road-stats/main/figures/figure1_accidents_by_year.png)

### Accidents By Hour
![Accidents By Hour](https://raw.githubusercontent.com/feiryrej/road-stats/main/figures/figure2_accidents_by_hour.png)

### Accidents By Day of Week
![Accidents By Day](https://raw.githubusercontent.com/feiryrej/road-stats/main/figures/figure3_accidents_by_day.png)

### Severity Distribution
![Severity Distribution](https://raw.githubusercontent.com/feiryrej/road-stats/main/figures/figure4_severity_distribution.png)

### Top 15 States by Accident Count
![Top States](https://raw.githubusercontent.com/feiryrej/road-stats/main/figures/figure5_top_states.png)

### Top 10 Weather Conditions
![Weather Conditions](https://raw.githubusercontent.com/feiryrej/road-stats/main/figures/figure6_weather_conditions.png)

After running `visualization.py`, six figures will be saved to the `figures/` directory. See the [Pipeline](#pipeline) section for a description of each chart.

## Key Findings

- Accident frequency shows an overall increasing trend from 2016 to 2023, as confirmed by linear regression with a positive slope.
- Accidents peak during morning rush hours (7-9 AM) and afternoon rush hours (3-6 PM), reflecting the strong influence of commuting behavior on accident occurrence.
- California accounts for 22.5% of all recorded accidents, followed by Florida (11.0%) and Texas (7.9%). These three states together represent over 41% of the total dataset.
- 77.6% of accidents are classified as moderate in severity (Severity 2); only 2.6% are categorized as severe (Severity 4).
- The chi-square test yielded X²(12) = 188,184.2 (p ≈ 0.00), confirming a statistically significant association between weather conditions and accident severity.

## Dataset

| Field | Details |
|-------|---------|
| Source | [Kaggle - US Accidents (2016-2023)](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents) |
| Author | Sobhan Moosavi |
| File | `US_Accidents_March23.csv` |
| Size | ~7.7 million records |
| Coverage | 49 US states, 2016 to 2023 |

## Setup and Usage

### Prerequisites

- Python 3.8+

### Installation

1. **Clone the repository**:

   ```
   git clone https://github.com/feiryrej/road-stats.git
   cd road-stats
   ```

2. **Install dependencies**:

   ```
   pip install pandas numpy matplotlib seaborn scipy
   ```

### Download the Dataset

Download the dataset from Kaggle and place the CSV file in the `data/` directory:

https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents

After downloading, your `data/` folder should contain:

```
data/
└── US_Accidents_March23.csv
```

### Run

Run the scripts in order:

```
python src/data_cleaning.py
python src/visualization.py
python src/analysis.py
```

`data_cleaning.py` must be run first, as both `visualization.py` and `analysis.py` depend on `US_Accidents_Cleaned.csv`.

## Dependencies

| Package | Purpose |
|---------|---------|
| `pandas` | Data loading, cleaning, and tabular analysis |
| `numpy` | Numerical operations and median imputation |
| `matplotlib` | Chart rendering and figure export |
| `seaborn` | Statistical chart styling |
| `scipy` | Linear regression, chi-square test, and Welch's t-test |

## Contributors
<table style="width: 100%; text-align: center;">
    <thead>
      <tr>
        <th>Name</th>
        <th>Avatar</th>
        <th>GitHub</th>
        <th>Contributions</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Regina S. Bonifacio</td>
        <td><img src="https://github.com/user-attachments/assets/8caf5539-c233-4cc0-a203-36226d033474" alt="" style="border-radius: 50%; width: 50px;"></td>
        <td><a href="https://github.com/feiryrej">feiryrej</a></td>
        <td><b>Analyst</b>: Was responsible for the full development of this project, including dataset selection, 
          data cleaning pipeline design, visualization development, statistical analysis, technical report writing, and repository documentation. 
          The author implemented all Python scripts, generated figures, conducted statistical tests, and prepared the final research and GitHub repository.
        </td>
      </tr>
    </tbody>
  </table>
</section>

## Reference

Moosavi, S. (2023). US Accidents (2016-2023) [Dataset]. Kaggle. https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents

World Health Organization. (2023). Global status report on road safety 2023. https://www.who.int/publications/i/item/global-status-report-on-road-safety-2023

[[Back to top](#road-stats)]
