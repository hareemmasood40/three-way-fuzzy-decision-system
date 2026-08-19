"""Tests for three_way_fuzzy.pfpo, including a thesis-inspired numerical example."""

import pytest

from three_way_fuzzy.model import PictureFuzzyNumber
from three_way_fuzzy.pfpo import (
    OperatorParameters,
    apply_iterations,
    apply_once,
    iterate_sequence,
)


def test_one_iteration() -> None:
    value = PictureFuzzyNumber(positive=0.1, neutral=0.2, negative=0.3)
    parameters = OperatorParameters(iota=0.2, alpha=0.2, beta=0.2)

    result = apply_once(value, parameters)

    refusal = value.refusal  # 0.4
    assert result.positive == pytest.approx(0.1 + 0.2 * refusal)
    assert result.neutral == pytest.approx(0.2 + 0.2 * refusal)
    assert result.negative == pytest.approx(0.3 + 0.2 * refusal)


def test_apply_once_matches_apply_iterations_for_n_equals_1() -> None:
    value = PictureFuzzyNumber(positive=0.1, neutral=0.2, negative=0.3)
    parameters = OperatorParameters(iota=0.2, alpha=0.2, beta=0.2)

    once = apply_once(value, parameters)
    one_iteration = apply_iterations(value, parameters, iterations=1)

    assert once.positive == pytest.approx(one_iteration.positive)
    assert once.neutral == pytest.approx(one_iteration.neutral)
    assert once.negative == pytest.approx(one_iteration.negative)


def test_several_iterations_reduce_refusal() -> None:
    value = PictureFuzzyNumber(positive=0.1, neutral=0.2, negative=0.3)
    parameters = OperatorParameters(iota=0.2, alpha=0.2, beta=0.2)

    sequence = iterate_sequence(value, parameters, iterations=5)

    refusals = [item.refusal for item in sequence]
    for earlier, later in zip(refusals, refusals[1:]):
        assert later < earlier
    assert refusals[-1] < refusals[0] * 0.1


def test_repeated_apply_once_matches_closed_form() -> None:
    value = PictureFuzzyNumber(positive=0.1, neutral=0.2, negative=0.3)
    parameters = OperatorParameters(iota=0.2, alpha=0.2, beta=0.2)

    stepwise = value
    for _ in range(4):
        stepwise = apply_once(stepwise, parameters)

    closed_form = apply_iterations(value, parameters, iterations=4)

    assert stepwise.positive == pytest.approx(closed_form.positive)
    assert stepwise.neutral == pytest.approx(closed_form.neutral)
    assert stepwise.negative == pytest.approx(closed_form.negative)


def test_zero_operator_parameters_leave_number_unchanged() -> None:
    value = PictureFuzzyNumber(positive=0.1, neutral=0.2, negative=0.3)
    parameters = OperatorParameters(iota=0.0, alpha=0.0, beta=0.0)

    once = apply_once(value, parameters)
    several = apply_iterations(value, parameters, iterations=10)

    assert once.as_tuple() == value.as_tuple()
    assert several.as_tuple() == value.as_tuple()


def test_invalid_operator_parameters_are_rejected() -> None:
    with pytest.raises(ValueError):
        OperatorParameters(iota=-0.1, alpha=0.2, beta=0.2)

    with pytest.raises(ValueError):
        OperatorParameters(iota=1.1, alpha=0.0, beta=0.0)

    with pytest.raises(ValueError):
        OperatorParameters(iota=0.5, alpha=0.5, beta=0.5)


def test_negative_iterations_are_rejected() -> None:
    value = PictureFuzzyNumber(positive=0.1, neutral=0.2, negative=0.3)
    parameters = OperatorParameters(iota=0.2, alpha=0.2, beta=0.2)

    with pytest.raises(ValueError):
        apply_iterations(value, parameters, iterations=-1)


class TestThesisNumericalExample:
    """Thesis-inspired numerical validation example.

    Reproduces the worked PFPO example from the author's MPhil thesis for
    t = (0.005, 0.3, 0.5) with operator parameters (iota=0.005, alpha=0.3,
    beta=0.5), checked against the thesis's rounded values.
    """

    value = PictureFuzzyNumber(positive=0.005, neutral=0.3, negative=0.5)
    parameters = OperatorParameters(iota=0.005, alpha=0.3, beta=0.5)

    def test_initial_refusal(self) -> None:
        assert self.value.refusal == pytest.approx(0.195, abs=1e-6)

    def test_iteration_1(self) -> None:
        result = apply_iterations(self.value, self.parameters, iterations=1)
        assert result.positive == pytest.approx(0.005975, abs=1e-6)
        assert result.neutral == pytest.approx(0.3585, abs=1e-6)
        assert result.negative == pytest.approx(0.5975, abs=1e-6)
        assert result.refusal == pytest.approx(0.038025, abs=1e-6)

    def test_iteration_2(self) -> None:
        result = apply_iterations(self.value, self.parameters, iterations=2)
        assert result.positive == pytest.approx(0.006165, abs=1e-6)
        assert result.neutral == pytest.approx(0.3699, abs=1e-4)
        assert result.negative == pytest.approx(0.6165, abs=1e-4)
        assert result.refusal == pytest.approx(0.007414875, abs=1e-6)
