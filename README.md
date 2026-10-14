@'


<img width="1672" height="941" alt="Regional Digital Payments Growth Monitor" src="https://github.com/user-attachments/assets/43b39469-1aed-435f-a8cd-d96b500c6de2" />



# Regional Digital Payments Monitor 🇮🇳

An interactive data analytics dashboard for exploring regional digital payment transaction trends in India using aggregated PhonePe Pulse data.

## 📌 Project Overview

The Regional Digital Payments Monitor helps users explore transaction activity across Indian states and union territories, compare regional performance, and analyze changes over time.

The project combines Python-based data preparation, SQL analysis, and interactive dashboards to turn public aggregated data into useful visual insights.

## 🎯 Objectives

- Analyze transaction volumes across states and union territories.
- Explore quarterly transaction trends.
- Compare transaction categories.
- Identify high-volume regions.
- Provide interactive filters and downloadable filtered data.
- Demonstrate an end-to-end data analytics workflow.

## ✨ Features

- **Interactive dashboard:** Built with Streamlit.
- **KPI cards:** Transaction count, number of regions, categories, and quarters.
- **Quarterly trends:** Explore transaction activity over time.
- **State comparison:** Compare regions and view the top 10 by transaction count.
- **Category analysis:** Examine transaction categories.
- **Heatmap:** Explore category activity across quarters.
- **Filters:** Select years, states/UTs, and transaction categories.
- **CSV export:** Download filtered records.
- **Glassmorphism UI:** Dark purple visual design.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and application logic |
| Pandas | Data cleaning and analysis |
| Streamlit | Interactive web dashboard |
| Plotly | Interactive charts and visualizations |
| SQL / MySQL | Data querying and database analysis |
| Power BI | Supplementary business intelligence dashboard |
| Git & GitHub | Version control and project portfolio |

## 📂 Project Structure

```text
Regional-Digital-Payments-Monitor/
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── assets/
├── data/
│   ├── processed/
│   │   └── phonepe_state_transactions.csv
│   └── raw/
├── reports/
├── clean_data.py
├── convert_to_csv.py
├── inspect_coverage.py
├── inspect_json.py
├── load_to_mysql.py
└── validate_data.py
