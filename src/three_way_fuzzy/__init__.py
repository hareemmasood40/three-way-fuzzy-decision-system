"""Three-Way Fuzzy Decision System.

A Python implementation and educational demonstration inspired by
mathematical concepts from the author's MPhil research on picture fuzzy
sets and three-way decision-making under uncertainty.
"""

from three_way_fuzzy.batch import process_case, process_csv
from three_way_fuzzy.decision import Decision, DecisionResult, DecisionThresholds, make_decision
from three_way_fuzzy.model import PictureFuzzyNumber
from three_way_fuzzy.pfpo import OperatorParameters, apply_iterations, apply_once, iterate_sequence

__all__ = [
    "PictureFuzzyNumber",
    "Decision",
    "DecisionResult",
    "DecisionThresholds",
    "make_decision",
    "OperatorParameters",
    "apply_once",
    "apply_iterations",
    "iterate_sequence",
    "process_case",
    "process_csv",
]

__version__ = "0.1.0"
