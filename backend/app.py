from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.analysis import extract_keywords, topic_modeling, trend_analysis
from backend.bigquery_client import fetch_questions
from backend.pain_points import identify_pain_points
from backend.preprocess import prepare_documents


app = FastAPI(title="Problem Trend Finder")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/analyze")
async def analyze(query: str) -> dict:
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    records = fetch_questions(query)
    if not records:
        return {
            "query": query,
            "top_keywords": [],
            "topics": [],
            "trends": [],
            "pain_points": [],
        }

    documents = prepare_documents(records)
    keywords = extract_keywords(documents)
    topics, dominant_topics = topic_modeling(documents)
    trends = trend_analysis(records, dominant_topics)
    pain_points = identify_pain_points(records)

    return {
        "query": query,
        "top_keywords": keywords,
        "topics": topics,
        "trends": trends,
        "pain_points": pain_points,
    }
