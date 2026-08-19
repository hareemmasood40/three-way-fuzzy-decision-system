"""Tests for three_way_fuzzy.model."""

import pytest

from three_way_fuzzy.model import PictureFuzzyNumber


def test_valid_picture_fuzzy_number() -> None:
    value = PictureFuzzyNumber(positive=0.70, neutral=0.10, negative=0.05)
    assert value.positive == pytest.approx(0.70)
    assert value.neutral == pytest.approx(0.10)
    assert value.negative == pytest.approx(0.05)


def test_refusal_calculation() -> None:
    value = PictureFuzzyNumber(positive=0.70, neutral=0.10, negative=0.05)
    assert value.refusal == pytest.approx(0.15)


def test_score_calculation() -> None:
    value = PictureFuzzyNumber(positive=0.70, neutral=0.10, negative=0.05)
    assert value.score == pytest.approx(0.55)


def test_accuracy_calculation() -> None:
    value = PictureFuzzyNumber(positive=0.70, neutral=0.10, negative=0.05)
    assert value.accuracy == pytest.approx(0.85)


def test_boundary_values_are_valid() -> None:
    value = PictureFuzzyNumber(positive=1.0, neutral=0.0, negative=0.0)
    assert value.refusal == pytest.approx(0.0)

    value = PictureFuzzyNumber(positive=0.0, neutral=0.0, negative=0.0)
    assert value.refusal == pytest.approx(1.0)


def test_rejects_negative_value() -> None:
    with pytest.raises(ValueError):
        PictureFuzzyNumber(positive=-0.1, neutral=0.2, negative=0.2)


def test_rejects_value_greater_than_one() -> None:
    with pytest.raises(ValueError):
        PictureFuzzyNumber(positive=1.1, neutral=0.0, negative=0.0)


def test_rejects_membership_sum_greater_than_one() -> None:
    with pytest.raises(ValueError):
        PictureFuzzyNumber(positive=0.6, neutral=0.3, negative=0.3)


def test_as_tuple() -> None:
    value = PictureFuzzyNumber(positive=0.5, neutral=0.2, negative=0.1)
    assert value.as_tuple() == (0.5, 0.2, 0.1)
