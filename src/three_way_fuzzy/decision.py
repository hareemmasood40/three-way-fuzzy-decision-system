"""Three-way decision layer.

This module turns a `PictureFuzzyNumber` into one of three decisions:
ACCEPT, DEFER (non-commitment) or REJECT, together with a human-readable
explanation.

Important: the thresholds and policy implemented here are an educational,
configurable demonstration layer, not a result taken from the author's
MPhil thesis. The thesis studied three-way decisions built from
decision-theoretic loss functions over rough approximations; this module
offers a simple, transparent, replaceable stand-in so the overall pipeline
(picture fuzzy number -> uncertainty -> decision) can be explored and
extended. See the README "Academic Integrity / Scope" section.

The decision policy is isolated behind `make_decision` so it can later be
swapped for a more rigorous decision-theoretic model without touching the
rest of the codebase.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from three_way_fuzzy.model import PictureFuzzyNumber


class Decision(str, Enum):
    """The three possible outcomes of a three-way decision."""

    ACCEPT = "ACCEPT"
    DEFER = "DEFER"
    REJECT = "REJECT"


@dataclass(frozen=True)
class DecisionThresholds:
    """Configurable thresholds for the demonstration decision policy.

    These defaults are illustrative, not derived from any empirical study.

    Attributes:
        accept_score_threshold: Minimum score required to accept.
        reject_score_threshold: Maximum (most negative) score allowed
            before rejecting.
        maximum_uncertainty_for_commitment: Maximum refusal/hesitation
            degree allowed before the system is willing to commit to
            ACCEPT or REJECT. Above this, the decision defers.
    """

    accept_score_threshold: float = 0.30
    reject_score_threshold: float = -0.30
    maximum_uncertainty_for_commitment: float = 0.25


@dataclass(frozen=True)
class DecisionResult:
    """The outcome of applying the decision policy to a picture fuzzy number."""

    decision: Decision
    explanation: str


def make_decision(
    picture_fuzzy_number: PictureFuzzyNumber,
    thresholds: DecisionThresholds | None = None,
) -> DecisionResult:
    """Apply the demonstration three-way decision policy.

    ACCEPT when the score is sufficiently positive and refusal uncertainty
    is sufficiently low. REJECT when the score is sufficiently negative and
    refusal uncertainty is sufficiently low. Otherwise DEFER/NON-COMMITMENT.
    """
    if thresholds is None:
        thresholds = DecisionThresholds()

    score = picture_fuzzy_number.score
    refusal = picture_fuzzy_number.refusal
    uncertainty_is_low = refusal <= thresholds.maximum_uncertainty_for_commitment

    if score >= thresholds.accept_score_threshold and uncertainty_is_low:
        explanation = (
            f"ACCEPT because the score ({score:.2f}) exceeds the acceptance "
            f"threshold ({thresholds.accept_score_threshold:.2f}) and refusal "
            f"uncertainty ({refusal:.2f}) is below the allowed commitment "
            f"threshold ({thresholds.maximum_uncertainty_for_commitment:.2f})."
        )
        return DecisionResult(Decision.ACCEPT, explanation)

    if score <= thresholds.reject_score_threshold and uncertainty_is_low:
        explanation = (
            f"REJECT because the score ({score:.2f}) falls below the "
            f"rejection threshold ({thresholds.reject_score_threshold:.2f}) "
            f"and refusal uncertainty ({refusal:.2f}) is below the allowed "
            f"commitment threshold ({thresholds.maximum_uncertainty_for_commitment:.2f})."
        )
        return DecisionResult(Decision.REJECT, explanation)

    if not uncertainty_is_low:
        explanation = (
            f"DEFER/NON-COMMITMENT because refusal uncertainty ({refusal:.2f}) "
            f"exceeds the allowed commitment threshold "
            f"({thresholds.maximum_uncertainty_for_commitment:.2f}), so a "
            "confident accept or reject decision cannot be made."
        )
    else:
        explanation = (
            f"DEFER/NON-COMMITMENT because the score ({score:.2f}) is not "
            f"extreme enough to exceed the acceptance threshold "
            f"({thresholds.accept_score_threshold:.2f}) or fall below the "
            f"rejection threshold ({thresholds.reject_score_threshold:.2f})."
        )

    return DecisionResult(Decision.DEFER, explanation)
