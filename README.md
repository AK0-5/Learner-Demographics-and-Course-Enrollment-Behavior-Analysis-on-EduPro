# EduPro Learner Analytics Dashboard

## Overview
Interactive dashboard analyzing learner demographics and course enrollment behavior on EduPro online learning platform.

## Features
- Filter by date range, age group, gender, course category, and level
- KPIs: Total records, unique learners, avg courses per learner, gender ratio
- Visualizations: Age distribution, heatmaps, category popularity, free vs paid enrollment
- Download filtered data as CSV

## Tech Stack
- Python
- Streamlit
- Plotly
- Pandas

## Key Findings
- 52% of enrollments are age 18-25
- Programming is most popular category (35%)
- Beginner courses make up 55% of enrollments
- Gender ratio: 1.15 (Female:Male)

## How to Run
```bash
pip install streamlit pandas plotly
streamlit run main.py
