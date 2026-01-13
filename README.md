# Problem Trend Finder

Problem Trend Finder is a full-stack application that analyzes Stack Overflow questions to surface trending developer pain points. It uses the public Google BigQuery dataset `bigquery-public-data.stackoverflow.posts_questions` to extract keywords, topics, trends over time, and high-pain unanswered questions for any query such as "azure" or "web development".

## Architecture Overview

- **Frontend (HTML/CSS/JS)**: A lightweight interface that lets users enter a query and view results.
- **Backend (FastAPI)**: Accepts a query, fetches relevant Stack Overflow questions from BigQuery, performs NLP + trend analysis, and returns structured JSON.
- **Data/NLP**: Uses TF-IDF for keyword extraction, LDA for topic modeling, and monthly aggregation for time trends.

```
problem-trend-finder/
├── backend/
│   ├── app.py
│   ├── bigquery_client.py
│   ├── preprocess.py
│   ├── analysis.py
│   └── pain_points.py
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── requirements.txt
├── README.md
└── .gitignore
```

## Running Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Authenticate with BigQuery

This project uses the free, public Stack Overflow dataset. Authenticate with Google Cloud so the BigQuery client can run the query:

```bash
gcloud auth application-default login
```

### 3. Start the backend

```bash
uvicorn backend.app:app --reload
```

### 4. Open the frontend

Open `frontend/index.html` in your browser. The frontend will call the backend at `http://localhost:8000/analyze`.

## Example Queries

- `azure`
- `web development`
- `kubernetes`
- `python pandas`

## Legality & Data Source

This project uses the official public BigQuery dataset:

- **Dataset**: `bigquery-public-data.stackoverflow.posts_questions`
- **Access**: Public, free to query with BigQuery
- **Method**: Programmatic query only (no scraping or paid APIs)

The analysis is derived from public Stack Overflow data in compliance with Google BigQuery usage terms.
