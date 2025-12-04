# Nike KPI Dashboard (Plotly + Dash)

[![Python Tests](https://github.com/SidharthaManriquez44/nike_dashboard/actions/workflows/python-test.yml/badge.svg)](https://github.com/SidharthaManriquez44/nike_dashboard/actions/workflows/python-test.yml)
[![codecov](https://codecov.io/gh/SidharthaManriquez44/nike_dashboard/graph/badge.svg?token=P3KGBnRzgC)](https://codecov.io/gh/SidharthaManriquez44/nike_dashboard)

Professional dashboard developed with Plotly + Dash for the interactive visualization of Nike's key KPIs.
The project includes a modular architecture, simulated data, and components ready to be replaced with real-world data sources (CSV, database, or API).

---
## Project Goal
To provide a solid foundation for building professional data analytics and marketing dashboards, with a modular architecture compatible with enterprise systems.

Its main focus is to help you:
* Integrate real-world data
* Derive actionable insights
* Visualize key metrics for the retail/sportswear sector
* Professionalize academic or professional projects with Dash


## Overview

This project implements an interactive web application built with Dash, designed to display strategic metrics for the sporting goods retail sector, using Nike as a case study.

The dashboard includes:
* KPI cards (sales, CAC, conversion, profit, etc.)
* Time series data
* Conversion funnel
* Regional map
* Inventory and replenishment
* Predictive model metrics (forecast error)
* Dynamic filters by date range and sales channel

## Project structure

```
nike_dashboard/
│
├── src/
│ └── dashboard.py 
│
├── tests/
│ └── test_dashboard.py 
│
├── .gitignore
├── LICENSE
├── README.md 
└── requirements.txt
```
## Execution
Run the dashboard:

```bash
  python src/dashboard.py
```

Open in browser:
```
http://127.0.0.1:8050
```
## Unit Testing
This project uses pytest.

Run the tests:

```bash
  pytest
```

## Customization
### Replace dummy data
The script includes a load_data() module with randomly generated data. To use real data:
* pandas.read_csv("file.csv")
* SQL connection (MySQL, PostgreSQL, Snowflake) with SQLAlchemy
* Internal or external API calls

## Customize KPI cards
The cards are built using only HTML and CSS, avoiding complex dependencies. You can extend them, customize colors, or add states (up/down).

## Expand visualizations
You can easily integrate:
* Predictive models (ARIMA, Prophet, Neural Networks)
* Dynamic alerts (by threshold or standard deviation)
* Marketing indicators (ROI, LTV, churn, CAC)
* Operational metrics (inventory, turnover, replenishment)

## Contributions
If you'd like to expand this project, you can:
* Add new visualizations
* Add database connectors
* Integrate advanced ML models
* Improve the visual design

Pull requests are welcome.

## Licencia
[MIT License](LICENSE)

## Author

Project developed by Sidhartha Manriquez,
aimed at strengthening computational statistics and professional programming skills in Python.