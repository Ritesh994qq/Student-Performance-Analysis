# Student Performance Analysis Using Python

## Overview
An interactive Streamlit dashboard that analyzes student marks, attendance, and daily study hours. It calculates totals, averages, percentages, grades, and pass status, and displays visualizations and summary insights.

## Features
- Filter by class, attendance range, and student name
- Calculate total marks, average marks, percentage, grade, and result
- Subject average and grade distribution charts
- Attendance and study-hours comparisons
- Correlation heatmap
- Download filtered results as CSV
- Sample dataset with 20 fictional students

## Requirements
Python 3.10 or newer is recommended.

## Run in VS Code / terminal
1. Extract the project ZIP and open the folder in VS Code.
2. Open a terminal in the project folder.
3. Create a virtual environment (optional but recommended):
   - Windows: `python -m venv .venv`
   - Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
4. Install packages: `python -m pip install -r requirements.txt`
5. Start the dashboard: `streamlit run app.py`
6. Open the local URL printed in the terminal (usually `http://localhost:8501`).

## Dataset format
Keep `student_data.csv` in the same folder as `app.py`. Required columns:
- `Student_ID`
- `Student_Name`
- `Class`
- `Maths`, `Science`, `English` (marks out of 100)
- `Attendance_Percent` (0 to 100)
- `Study_Hours_Per_Day`

If using your own dataset, keep these column names or update the column names in `app.py`. Use fictional/anonymized data when sharing the project.

## Notes
The sample data is fictional and for demonstration only. Correlation does not prove causation; the dashboard is an educational analysis tool, not a formal assessment system.
