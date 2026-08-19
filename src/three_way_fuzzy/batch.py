"""Batch processing of picture fuzzy numbers from a CSV file.

Expected input CSV columns: case_id, positive, neutral, negative.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from three_way_fuzzy.decision import DecisionThresholds, make_decision
from three_way_fuzzy.model import PictureFuzzyNumber

OUTPUT_FIELDNAMES = [
    "case_id",
    "positive",
    "neutral",
    "negative",
    "refusal",
    "score",
    "accuracy",
    "decision",
    "explanation",
]


def process_case(
    case_id: str,
    positive: float,
    neutral: float,
    negative: float,
    thresholds: DecisionThresholds | None = None,
) -> dict[str, Any]:
    """Evaluate a single (case_id, positive, neutral, negative) row."""
    picture_fuzzy_number = PictureFuzzyNumber(positive, neutral, negative)
    result = make_decision(picture_fuzzy_number, thresholds)
    return {
        "case_id": case_id,
        "positive": picture_fuzzy_number.positive,
        "neutral": picture_fuzzy_number.neutral,
        "negative": picture_fuzzy_number.negative,
        "refusal": picture_fuzzy_number.refusal,
        "score": picture_fuzzy_number.score,
        "accuracy": picture_fuzzy_number.accuracy,
        "decision": result.decision.value,
        "explanation": result.explanation,
    }


def process_csv(
    input_path: str | Path,
    output_path: str | Path | None = None,
    thresholds: DecisionThresholds | None = None,
) -> list[dict[str, Any]]:
    """Read a CSV of picture fuzzy numbers, evaluate each row, and return results.

    If `output_path` is given, the results are also written to that CSV file.
    """
    input_path = Path(input_path)
    results: list[dict[str, Any]] = []

    with input_path.open(newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            results.append(
                process_case(
                    case_id=row["case_id"],
                    positive=float(row["positive"]),
                    neutral=float(row["neutral"]),
                    negative=float(row["negative"]),
                    thresholds=thresholds,
                )
            )

    if output_path is not None:
        output_path = Path(output_path)
        with output_path.open("w", newline="", encoding="utf-8") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=OUTPUT_FIELDNAMES)
            writer.writeheader()
            writer.writerows(results)

    return results
