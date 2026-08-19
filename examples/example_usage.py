"""Worked example: using the three_way_fuzzy package as a library.

Run with:
    python examples/example_usage.py
"""

from three_way_fuzzy.decision import DecisionThresholds, make_decision
from three_way_fuzzy.model import PictureFuzzyNumber
from three_way_fuzzy.pfpo import OperatorParameters, iterate_sequence


def main() -> None:
    # A confident, mostly positive judgement.
    confident_case = PictureFuzzyNumber(positive=0.70, neutral=0.10, negative=0.05)
    result = make_decision(confident_case)
    print("Confident case:", confident_case.as_tuple())
    print(f"  refusal={confident_case.refusal:.2f} score={confident_case.score:.2f} "
          f"accuracy={confident_case.accuracy:.2f}")
    print(f"  decision={result.decision.value}")
    print(f"  explanation: {result.explanation}")
    print()

    # An ambiguous judgement (low refusal, but score too close to zero) -> DEFER.
    ambiguous_case = PictureFuzzyNumber(positive=0.40, neutral=0.30, negative=0.20)
    result = make_decision(ambiguous_case)
    print("Ambiguous case:", ambiguous_case.as_tuple())
    print(f"  decision={result.decision.value}")
    print(f"  explanation: {result.explanation}")
    print()

    # Custom thresholds.
    strict_thresholds = DecisionThresholds(
        accept_score_threshold=0.5,
        reject_score_threshold=-0.5,
        maximum_uncertainty_for_commitment=0.10,
    )
    result = make_decision(confident_case, strict_thresholds)
    print("Confident case with stricter thresholds:")
    print(f"  decision={result.decision.value}")
    print(f"  explanation: {result.explanation}")
    print()

    # Thesis-inspired Picture Fuzzy Point Operator example.
    thesis_case = PictureFuzzyNumber(positive=0.005, neutral=0.3, negative=0.5)
    parameters = OperatorParameters(iota=0.005, alpha=0.3, beta=0.5)
    sequence = iterate_sequence(thesis_case, parameters, iterations=2)

    print("Thesis-inspired PFPO trajectory:")
    for step, value in enumerate(sequence):
        print(
            f"  n={step}: (positive={value.positive:.6f}, neutral={value.neutral:.6f}, "
            f"negative={value.negative:.6f}) refusal={value.refusal:.6f}"
        )


if __name__ == "__main__":
    main()
