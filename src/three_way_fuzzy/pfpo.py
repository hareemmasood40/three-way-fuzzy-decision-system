"""Picture Fuzzy Point Operator (PFPO).

The Picture Fuzzy Point Operator redistributes part of a picture fuzzy
number's refusal/hesitation degree into its positive, neutral and negative
components. Repeated application lets us study how uncertainty evolves
(typically shrinking) over successive iterations.

This is a computational implementation inspired by the operator used in the
author's MPhil thesis "Three-Way Decisions on Picture Fuzzy Rough Sets".

For t = (positive, neutral, negative) with refusal pi = 1 - positive -
neutral - negative, and operator parameters iota, alpha, beta in [0, 1]
with iota + alpha + beta <= 1, the one-step transformation is:

    E(t) = (positive + iota * pi, neutral + alpha * pi, negative + beta * pi)

For n repeated applications, letting r = iota + alpha + beta:

    if r != 0:
        factor = (1 - (1 - r) ** n) / r
        positive_n = positive + iota * pi * factor
        neutral_n  = neutral  + alpha * pi * factor
        negative_n = negative + beta  * pi * factor
        pi_n = (1 - r) ** n * pi
    if r == 0:
        the picture fuzzy number is unchanged for any n.
"""

from __future__ import annotations

from dataclasses import dataclass

from three_way_fuzzy.model import FLOAT_TOLERANCE, PictureFuzzyNumber


@dataclass(frozen=True)
class OperatorParameters:
    """Parameters (iota, alpha, beta) controlling the PFPO redistribution.

    Each parameter must lie in [0, 1] and iota + alpha + beta must not
    exceed 1.
    """

    iota: float
    alpha: float
    beta: float

    def __post_init__(self) -> None:
        for name, value in (
            ("iota", self.iota),
            ("alpha", self.alpha),
            ("beta", self.beta),
        ):
            if value < -FLOAT_TOLERANCE or value > 1 + FLOAT_TOLERANCE:
                raise ValueError(
                    f"{name} must be between 0 and 1, got {value}."
                )

        total = self.iota + self.alpha + self.beta
        if total > 1 + FLOAT_TOLERANCE:
            raise ValueError(
                f"iota + alpha + beta must not exceed 1, got {total}."
            )

    @property
    def total(self) -> float:
        """r = iota + alpha + beta."""
        return self.iota + self.alpha + self.beta


def apply_once(
    picture_fuzzy_number: PictureFuzzyNumber,
    parameters: OperatorParameters,
) -> PictureFuzzyNumber:
    """Apply a single step of the Picture Fuzzy Point Operator."""
    refusal = picture_fuzzy_number.refusal
    return PictureFuzzyNumber(
        positive=picture_fuzzy_number.positive + parameters.iota * refusal,
        neutral=picture_fuzzy_number.neutral + parameters.alpha * refusal,
        negative=picture_fuzzy_number.negative + parameters.beta * refusal,
    )


def apply_iterations(
    picture_fuzzy_number: PictureFuzzyNumber,
    parameters: OperatorParameters,
    iterations: int,
) -> PictureFuzzyNumber:
    """Apply the Picture Fuzzy Point Operator `iterations` times.

    Uses the closed-form iterative expression rather than looping, which is
    equivalent to repeatedly calling `apply_once`.
    """
    if iterations < 0:
        raise ValueError(f"iterations must be non-negative, got {iterations}.")
    if iterations == 0:
        return picture_fuzzy_number

    total = parameters.total
    refusal = picture_fuzzy_number.refusal

    if abs(total) < FLOAT_TOLERANCE:
        return picture_fuzzy_number

    factor = (1 - (1 - total) ** iterations) / total
    return PictureFuzzyNumber(
        positive=picture_fuzzy_number.positive + parameters.iota * refusal * factor,
        neutral=picture_fuzzy_number.neutral + parameters.alpha * refusal * factor,
        negative=picture_fuzzy_number.negative + parameters.beta * refusal * factor,
    )


def iterate_sequence(
    picture_fuzzy_number: PictureFuzzyNumber,
    parameters: OperatorParameters,
    iterations: int,
) -> list[PictureFuzzyNumber]:
    """Return [t_0, t_1, ..., t_n], the PFPO trajectory over `iterations` steps.

    t_0 is the original, unmodified picture fuzzy number.
    """
    if iterations < 0:
        raise ValueError(f"iterations must be non-negative, got {iterations}.")

    sequence = [picture_fuzzy_number]
    for step in range(1, iterations + 1):
        sequence.append(apply_iterations(picture_fuzzy_number, parameters, step))
    return sequence
