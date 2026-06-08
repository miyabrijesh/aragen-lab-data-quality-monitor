# 🧪 Lab Data Quality Monitor

## Aragen Life Sciences Internship Assignment

### Candidate Details
- Name: Miya Brijesh
- Internship Assignment: Data Quality Monitoring System
- Technology Stack: Python, Pandas, SQLite, Streamlit, Plotly
- Repository: https://github.com/miyabrijesh/aragen-lab-data-quality-monitor
- Live Dashboard: https://aragen-lab-data-quality-monitor-ephu6jrh58bpnng2zjus3n.streamlit.app

---

# 1. Project Overview

This project implements a complete Data Quality Monitoring solution for laboratory measurement data.

The solution covers:

- Synthetic laboratory dataset generation
- ETL pipeline development
- Data quality rule implementation
- Quality score computation
- Failed record identification
- SQLite data warehouse creation
- Interactive Streamlit dashboard
- Cloud deployment using Streamlit Community Cloud

The objective is to continuously monitor laboratory data quality, identify problematic records, and provide analytical insights through an interactive dashboard.

---

# 2. Project Architecture

```text
Raw Dataset
    ↓
ETL Pipeline
    ↓
Data Quality Rules
    ↓
Quality Scoring
    ↓
SQLite Database
    ↓
Streamlit Dashboard
    ↓
Cloud Deployment
```

---

# 3. Folder Structure

```text
Aragen_Assignment/
│
├── dashboard/
│   └── app.py
│
├── data/
│   └── lab_data.csv
│
├── database/
│   ├── lab_quality.db
│   └── lab_quality_task3.db
│
├── docs/
│   ├── dashboard_overview.png
│   ├── dashboard_filter.png
│   ├── dashboard_chart1.png
│   ├── dashboard_chart2.png
│   ├── dashboard_failed_records.png
│   └── Aragen Life Sciences Internship Assignment.docx
│
├── src/
│   ├── 01_dataset_generation.ipynb
│   ├── 02_etl_pipeline.ipynb
│   └── 03_data_quality_rules.ipynb
│
├── README.md
└── requirements.txt
```

---

# 4. Dataset Generation

A synthetic pharmaceutical laboratory dataset was generated containing:

- Sample IDs
- Laboratory Information
- Instrument Information
- Operator Information
- Experiment Dates
- Recording Timestamps
- Analyte Information
- Measurement Values
- Units
- Status Indicators

Total records generated:

```text
500,000 records
```

Purposefully injected data quality issues include:

- Missing values
- Invalid ranges
- Future dates
- Timestamp inconsistencies
- Invalid units
- Duplicate records

---

# 5. ETL Pipeline

The ETL pipeline performs:

## Extract

Reading raw laboratory dataset.

## Transform

- Data type standardization
- Date formatting
- Null handling
- Data cleaning

## Load

Loading transformed records into SQLite database tables.

---

# 6. Data Quality Rules Implemented

The following validation rules were implemented:

### Rule 1: Missing Measurement Value

Checks for:

```text
measured_value IS NULL
```

Severity:

```text
Major
```

---

### Rule 2: Invalid Measurement Range

Checks:

```text
measured_value < 0
OR
measured_value > allowed threshold
```

Severity:

```text
Critical
```

---

### Rule 3: Future Experiment Date

Checks:

```text
experiment_date > current_date
```

Severity:

```text
Critical
```

---

### Rule 4: Timestamp Validation

Checks:

```text
recorded_at < experiment_date
```

Severity:

```text
Major
```

---

### Rule 5: Invalid Units

Checks:

```text
unit NOT IN approved units
```

Severity:

```text
Minor
```

---

### Rule 6: Duplicate Sample IDs

Checks:

```text
duplicate sample_id
```

Severity:

```text
Major
```

---

# 7. Quality Score Calculation

Each record starts with:

```text
100 Points
```

Penalty Model:

| Severity | Penalty |
|-----------|----------|
| Critical | 20 |
| Major | 10 |
| Minor | 5 |

Formula:

```text
Quality Score = 100 - Total Penalties
```

Minimum score:

```text
0
```

Maximum score:

```text
100
```

---

# 8. Database Design

SQLite database was created with the following tables.

## Fact Table

### fact_lab_measurements

Stores:

- Sample Information
- Quality Scores
- Rule Violations
- Severity

---

## Dimension Tables

### dim_lab

Laboratory details.

### dim_instrument

Instrument details.

### dim_operator

Operator details.

---

## Failed Records Table

### failed_records

Stores all records violating one or more quality rules.

---

# 9. Dashboard Development

An interactive Streamlit dashboard was developed.

Features include:

- KPI Cards
- Interactive Filters
- Visual Analytics
- Failed Records Drilldown
- Cloud Deployment

---

# 10. Dashboard KPIs

The dashboard displays:

### Overall Data Quality Score

Average quality score across all records.

### Total Records

Total records processed.

### Failed Records

Records that violated at least one quality rule.

---

# 11. Dashboard Filters

Implemented filters:

### Severity Filter

```text
Critical
Major
Minor
```

### Lab Filter

Select individual laboratories.

### Instrument Filter

Select instruments.

### Date Range Filter

Filter records based on experiment date.

---

# 12. Dashboard Visualizations

## Quality Breakdown by Lab

Displays average quality score for each laboratory.

### Screenshot

![Quality by Lab](docs/dashboard_overview.png)

---

## Quality Breakdown by Instrument

Displays average quality score across instruments.

### Screenshot

![Quality by Instrument](docs/dashboard_chart1.png)

---

## Quality Score Over Time

Trend analysis of quality scores.

### Screenshot

![Quality Over Time](docs/dashboard_chart2.png)

---

## Severity Distribution

Distribution of:

- Critical
- Major
- Minor

violations.

### Screenshot

![Severity Distribution](docs/dashboard_chart2.png)

---

## Failed Records Drilldown

Detailed failed record inspection.

### Screenshot

![Failed Records](docs/dashboard_failed_records.png)

---

## Dashboard Filters

### Screenshot

![Filters](docs/dashboard_filter.png)

---

# 13. Deployment

The dashboard was deployed using:

### Streamlit Community Cloud

Deployment Link:

https://aragen-lab-data-quality-monitor-ephu6jrh58bpnng2zjus3n.streamlit.app

Repository:

https://github.com/miyabrijesh/aragen-lab-data-quality-monitor

---

# 14. Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Core Programming |
| Pandas | Data Processing |
| NumPy | Numerical Operations |
| SQLite | Data Warehouse |
| Streamlit | Dashboard |
| Plotly | Interactive Charts |
| Git | Version Control |
| GitHub | Repository Hosting |
| Streamlit Cloud | Deployment |

---

# 15. Key Outcomes

Successfully implemented:

✅ Large-scale laboratory dataset generation

✅ End-to-end ETL pipeline

✅ Automated data quality validation

✅ Quality score computation framework

✅ SQLite analytical database

✅ Interactive monitoring dashboard

✅ Cloud deployment

✅ GitHub repository management

---

# 16. Conclusion

This project demonstrates the implementation of a complete Data Quality Monitoring System for laboratory environments. The solution automates quality validation, tracks quality trends, identifies failed records, and provides stakeholders with actionable insights through an interactive dashboard.

The final solution is scalable, modular, and suitable for extension into production-grade laboratory data quality monitoring systems.
