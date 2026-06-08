# 🧪 Lab Data Quality Monitor

## Aragen Life Sciences Internship Assignment

This project demonstrates an end-to-end pharmaceutical laboratory data quality monitoring solution. The system generates synthetic laboratory data, performs ETL processing, applies data quality validation rules, calculates quality scores, and presents insights through an interactive Streamlit dashboard.

---

## Project Objectives

- Generate a synthetic pharmaceutical laboratory dataset (~500,000 records)
- Build an ETL pipeline using Python and SQLite
- Implement a Data Quality Rules Engine
- Calculate record-level and dataset-level quality scores
- Categorize failures by severity (Critical, Major, Minor)
- Develop an interactive Streamlit dashboard for monitoring data quality

---

## Project Structure

```
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
│   ├── Aragen Life Sciences Internship Assignment.docx
│   ├── dashboard_overview.png
│   ├── dashboard_chart1.png
│   ├── dashboard_chart2.png
│   ├── dashboard_filter.png
│   └── dashboard_failed_records.png
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

## Task 1: Synthetic Dataset Generation

Generated approximately 500,000 pharmaceutical laboratory records containing:

- Sample Information
- Laboratory Details
- Instrument Information
- Operator Information
- Experiment Dates
- Measured Values
- Units
- Status Information

Intentional data quality issues were introduced to simulate real-world scenarios:

- Missing values
- Duplicate records
- Invalid measurements
- Invalid dates
- Cross-field inconsistencies
- Delayed record entry

---

## Task 2: ETL Pipeline

Performed ETL processing using Python and SQLite:

### Extract
- Loaded source CSV dataset

### Transform
- Data cleansing
- Date standardization
- Data type validation
- Dimension table creation

### Load
Created Star Schema:

### Fact Table
- fact_lab_measurements

### Dimension Tables
- dim_lab
- dim_instrument
- dim_operator

Database:
- lab_quality.db

---

## Task 3: Data Quality Rules Engine

Implemented 12 Data Quality Rules across multiple dimensions:

### Completeness
- Missing measured value
- Missing analyte name
- Missing unit

### Uniqueness
- Duplicate sample_id detection

### Validity
- Negative measured values
- Values outside acceptable range
- Invalid status values
- Invalid date formats

### Consistency
- Status = Pass but measured value missing
- Unit missing while value exists

### Timeliness
- Records entered more than 24 hours after experiment

### Quality Scoring

Each rule contributes to a record-level score:

- Quality Score Range: 0–100
- Dataset Quality Score: 97.15%

### Severity Classification

- Critical
- Major
- Minor

Database:
- lab_quality_task3.db

---

## Task 4: Interactive Dashboard

Built using Streamlit and Plotly.

### Dashboard Features

#### KPI Metrics
- Overall Quality Score
- Total Records
- Failed Records

#### Visualizations
- Quality Breakdown by Lab
- Quality Breakdown by Instrument
- Quality Score Trend Over Time
- Severity Distribution

#### Drill Down Analysis
- Failed Records Table

#### Interactive Filters
- Severity
- Lab
- Instrument
- Date Range

---

## Technology Stack

- Python
- Pandas
- NumPy
- SQLite
- Plotly
- Streamlit
- Jupyter Notebook

---

## Dashboard Preview

Dashboard screenshots are available in the `docs` folder.

---

## How to Run

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Dashboard

```bash
streamlit run dashboard/app.py
```

---

## Author

Miya Brijesh

Aragen Life Sciences Internship Assignment
