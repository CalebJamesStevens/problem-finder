from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


TOP_KEYWORDS = 20
DEFAULT_TOPICS = 8
TOP_TERMS_PER_TOPIC = 8


def extract_keywords(documents: list[str]) -> list[str]:
    if not documents:
        return []
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000,
    )
    tfidf_matrix = vectorizer.fit_transform(documents)
    scores = tfidf_matrix.sum(axis=0).A1
    terms = vectorizer.get_feature_names_out()
    ranked = sorted(zip(terms, scores), key=lambda item: item[1], reverse=True)
    return [term for term, _ in ranked[:TOP_KEYWORDS]]


def _topic_count(documents: list[str]) -> int:
    if len(documents) < DEFAULT_TOPICS:
        return max(1, min(6, len(documents)))
    return DEFAULT_TOPICS


def topic_modeling(documents: list[str]) -> tuple[list[dict[str, Any]], list[int]]:
    if not documents:
        return [], []
    vectorizer = CountVectorizer(stop_words="english", max_features=6000)
    doc_term_matrix = vectorizer.fit_transform(documents)
    topic_count = _topic_count(documents)
    lda = LatentDirichletAllocation(
        n_components=topic_count,
        random_state=42,
        learning_method="batch",
    )
    lda.fit(doc_term_matrix)
    feature_names = vectorizer.get_feature_names_out()

    topics = []
    for idx, topic_weights in enumerate(lda.components_):
        top_indices = topic_weights.argsort()[::-1][:TOP_TERMS_PER_TOPIC]
        terms = [feature_names[i] for i in top_indices]
        topics.append({"topic_id": idx, "terms": terms})

    topic_distributions = lda.transform(doc_term_matrix)
    dominant_topics = topic_distributions.argmax(axis=1).tolist()
    return topics, dominant_topics


def trend_analysis(records: list[dict], dominant_topics: list[int]) -> list[dict[str, Any]]:
    if not records or not dominant_topics:
        return []
    df = pd.DataFrame(records)
    df["topic_id"] = dominant_topics
    df["month"] = pd.to_datetime(df["creation_date"]).dt.to_period("M").astype(str)
    grouped = df.groupby(["month", "topic_id"]).size().reset_index(name="count")
    grouped = grouped.sort_values("month")
    return grouped.to_dict(orient="records")
