"""Picture fuzzy number model.

A Picture Fuzzy Number (PFN) represents an uncertain judgement using three
independent degrees of membership: positive, neutral and negative. Unlike a
classical fuzzy set (a single membership degree) or an intuitionistic fuzzy
set (positive/negative only), a picture fuzzy set explicitly models
"neutral" opinions as well as leftover, unassigned belief.

This module is a computational, educational implementation inspired by the
picture fuzzy set formalism used in the author's MPhil thesis
"Three-Way Decisions on Picture Fuzzy Rough Sets". It is not a reproduction
of the thesis, only of the underlying mathematical building blocks.
"""

from __future__ import annotations

from dataclasses import dataclass

FLOAT_TOLERANCE = 1e-9


@dataclass(frozen=True)
class PictureFuzzyNumber:
    """A picture fuzzy number t = (positive, neutral, negative).

    Attributes:
        positive: Positive membership degree, mu, in [0, 1].
        neutral: Neutral membership degree, eta, in [0, 1].
        negative: Negative membership degree, nu, in [0, 1].

    The three degrees must satisfy positive + neutral + negative <= 1.
    The remaining mass is the refusal/hesitation degree:
        refusal = 1 - positive - neutral - negative
    """

    positive: float
    neutral: float
    negative: float

    def __post_init__(self) -> None:
        for name, value in (
            ("positive", self.positive),
            ("neutral", self.neutral),
            ("negative", self.negative),
        ):
            if value < -FLOAT_TOLERANCE or value > 1 + FLOAT_TOLERANCE:
                raise ValueError(
                    f"{name} membership must be between 0 and 1, got {value}."
                )

        membership_sum = self.positive + self.neutral + self.negative
        if membership_sum > 1 + FLOAT_TOLERANCE:
            raise ValueError(
                "positive + neutral + negative must not exceed 1, "
                f"got {membership_sum}."
            )

    @property
    def refusal(self) -> float:
        """Refusal/hesitation degree: pi = 1 - positive - neutral - negative."""
        return 1.0 - self.positive - self.neutral - self.negative

    @property
    def score(self) -> float:
        """Score function: S(t) = positive - neutral - negative.

        Higher scores indicate a judgement that leans towards acceptance;
        lower (more negative) scores lean towards rejection.
        """
        return self.positive - self.neutral - self.negative

    @property
    def accuracy(self) -> float:
        """Accuracy/certainty function: H(t) = positive + neutral + negative.

        Equivalent to (1 - refusal). Higher values indicate that less
        belief mass remains unassigned/unknown.
        """
        return self.positive + self.neutral + self.negative

    def as_tuple(self) -> tuple[float, float, float]:
        """Return the (positive, neutral, negative) triple."""
        return (self.positive, self.neutral, self.negative)
