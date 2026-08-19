# 🛡️ Palo Alto Networks: HR Diagnostic Dashboard

An interactive Data Science & HR Analytics dashboard designed to detect early-warning signals of employee burnout and disengagement using custom diagnostic metrics.

## Project Objective
The primary objective of this project is to equip HR leadership with an early-warning diagnostic system. Historically, attrition problems are only addressed after an employee has already decided to leave. This project shifts the analytical focus from **reactive** turnover tracking to **preventive** employee experience diagnostics. 

By engineering custom Key Performance Indicators (KPIs) and deploying them via an interactive Streamlit dashboard, managers can instantly identify high-risk employee segments. This allows for proactive, human-centered retention interventions before critical talent is lost.

## Engineered KPIs
Instead of relying on isolated survey scores, this project engineered five custom composite metrics to accurately measure workforce health:
1. **Engagement Index:** A composite score combining job involvement, environment satisfaction, and relationship satisfaction.
2. **Burnout Risk Score:** A weighted indicator combining excessive overtime and poor work-life balance.
3. **Satisfaction Stability Score:** Measures the consistency of an employee's satisfaction across multiple dimensions.
4. **Workload Stress Indicator:** A combined metric of business travel frequency and overtime intensity.

## Dashboard Features
The interactive web application features three primary modules:
* **Engagement Health:** Company-wide engagement spread and career-stage tenure analysis.
* **Burnout Risk:** Job role burnout assessments and workload stress correlations.
* **Priority Intervention Table:** A dynamic, filterable table that isolates employees exhibiting metrics mathematically identical to those who have previously left the organization due to burnout.

## Tech Stack
* **Language:** Python 3.x
* **Data Processing:** Pandas, NumPy
* **Data Visualization:** Plotly Express, Seaborn, Matplotlib
* **Web Framework:** Streamlit
* **Environment:** Jupyter Notebook

## How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/HR-Burnout-Diagnostic-Dashboard.git](https://github.com/YourUsername/HR-Burnout-Diagnostic-Dashboard.git)
   cd HR-Burnout-Diagnostic-Dashboard