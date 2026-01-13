from __future__ import annotations

import pandas as pd


DEFAULT_LIMIT = 20


def identify_pain_points(records: list[dict], limit: int = DEFAULT_LIMIT) -> list[dict]:
    if not records:
        return []
    df = pd.DataFrame(records)
    df = df[df["answer_count"].fillna(0) == 0]
    if df.empty:
        return []
    threshold = df["view_count"].quantile(0.75)
    df = df[df["view_count"] >= threshold]
    df = df.sort_values("view_count", ascending=False).head(limit)
    return (
        df[["title", "view_count"]]
        .fillna("")
        .to_dict(orient="records")
    )
