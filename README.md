<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/English-275DAD?style=for-the-badge" alt="Read in English"></a>
  <a href="README.pt-BR.md"><img src="https://img.shields.io/badge/Português-667085?style=for-the-badge" alt="Ler em português"></a>
</p>

# Sales and Engagement Dashboard

A lightweight local dashboard that combines sales performance and student
engagement metrics in a single view.

The application reads exclusively from `relatorio_final.csv`, a cleaned,
enriched, and anonymized dataset. Raw source files are never accessed by the
dashboard.

## Screenshots

### Desktop overview

![Sales and engagement dashboard desktop view](assets/screenshots/dashboard-overview.png)

### Responsive mobile view

<p align="center">
  <img src="assets/screenshots/dashboard-mobile.png" alt="Sales and engagement dashboard mobile view" width="360">
</p>

## Features

- Total sales, total revenue, and average order value KPIs
- Monthly revenue trend
- Sales distribution by Brazilian state
- Student engagement rate and metric coverage
- Filters by date range, course, state, and holiday sales
- Responsive layout for desktop and mobile screens
- Browser payload limited to the fields required by the dashboard

## Running Locally

### Requirements

- Python 3

### Start the dashboard

```powershell
python dashboard.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

The health endpoint is available at
[http://127.0.0.1:8000/health](http://127.0.0.1:8000/health).

## Architecture

The backend follows a DDD-inspired organization:

- `domain`: entities and business rules, including engagement scoring
- `application`: use cases, DTOs, and data access ports
- `infrastructure`: CSV repository implementation
- `presentation`: HTTP adapter and dashboard rendering
- `bootstrap.py`: application dependency composition

The root `dashboard.py` remains the local execution entry point.

### Tests

```powershell
python -m unittest discover -v
```

## Engagement Score

The engagement score ranges from 0 to 100 and combines:

- watched hours: 50%
- NPS score: 30%
- low number of support tickets: 20%

When a metric is unavailable, the remaining weights are normalized. A student
is considered engaged when their score is 60 or higher. Students with multiple
purchases are counted once using the average of their scores.

## Privacy

CPF, ZIP code, and transaction identifiers are not sent to the browser.
Purchases belonging to the same student are associated only through a
server-generated hash.
