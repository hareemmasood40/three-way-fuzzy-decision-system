"""Tests for three_way_fuzzy.decision."""

from three_way_fuzzy.decision import Decision, DecisionThresholds, make_decision
from three_way_fuzzy.model import PictureFuzzyNumber


def test_clear_accept() -> None:
    value = PictureFuzzyNumber(positive=0.70, neutral=0.10, negative=0.05)
    result = make_decision(value)
    assert result.decision is Decision.ACCEPT
    assert "ACCEPT" in result.explanation


def test_clear_reject() -> None:
    value = PictureFuzzyNumber(positive=0.05, neutral=0.15, negative=0.70)
    result = make_decision(value)
    assert result.decision is Decision.REJECT
    assert "REJECT" in result.explanation


def test_defer_because_score_is_ambiguous() -> None:
    # Low refusal, but the score is too close to zero to commit either way.
    value = PictureFuzzyNumber(positive=0.40, neutral=0.30, negative=0.20)
    result = make_decision(value)
    assert value.refusal <= DecisionThresholds().maximum_uncertainty_for_commitment
    assert result.decision is Decision.DEFER
    assert "not extreme enough" in result.explanation


def test_defer_because_uncertainty_is_too_high() -> None:
    # Score alone would qualify for ACCEPT, but refusal is too high to commit.
    value = PictureFuzzyNumber(positive=0.40, neutral=0.05, negative=0.05)
    result = make_decision(value)
    assert value.score >= DecisionThresholds().accept_score_threshold
    assert value.refusal > DecisionThresholds().maximum_uncertainty_for_commitment
    assert result.decision is Decision.DEFER
    assert "uncertainty" in result.explanation


def test_custom_thresholds_change_outcome() -> None:
    value = PictureFuzzyNumber(positive=0.55, neutral=0.15, negative=0.10)
    default_result = make_decision(value)

    strict_thresholds = DecisionThresholds(
        accept_score_threshold=0.5,
        reject_score_threshold=-0.5,
        maximum_uncertainty_for_commitment=0.25,
    )
    strict_result = make_decision(value, strict_thresholds)

    assert default_result.decision is Decision.ACCEPT
    assert strict_result.decision is Decision.DEFER
