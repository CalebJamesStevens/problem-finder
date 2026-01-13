from __future__ import annotations

from google.cloud import bigquery


def _build_query(tag_candidate: str) -> str:
    return """
        SELECT
            title,
            body,
            creation_date,
            view_count,
            answer_count
        FROM `bigquery-public-data.stackoverflow.posts_questions`
        WHERE creation_date >= TIMESTAMP('2019-01-01')
          AND (
            REGEXP_CONTAINS(LOWER(tags), CONCAT('<', @tag, '>'))
            OR LOWER(title) LIKE CONCAT('%', @keyword, '%')
            OR LOWER(body) LIKE CONCAT('%', @keyword, '%')
          )
        ORDER BY creation_date DESC
        LIMIT @limit
    """


def fetch_questions(query: str, limit: int = 10000) -> list[dict]:
    cleaned_query = query.strip().lower()
    if not cleaned_query:
        return []

    tag_candidate = cleaned_query.replace(" ", "-")
    client = bigquery.Client()
    sql = _build_query(tag_candidate)
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("tag", "STRING", tag_candidate),
            bigquery.ScalarQueryParameter("keyword", "STRING", cleaned_query),
            bigquery.ScalarQueryParameter("limit", "INT64", limit),
        ]
    )
    query_job = client.query(sql, job_config=job_config)
    rows = query_job.result()
    return [
        {
            "title": row.title,
            "body": row.body,
            "creation_date": row.creation_date,
            "view_count": row.view_count,
            "answer_count": row.answer_count,
        }
        for row in rows
    ]
