"""Interactive command-line interface for the Three-Way Fuzzy Decision System."""

from __future__ import annotations

import argparse
import sys
from typing import Callable

from three_way_fuzzy.batch import process_csv
from three_way_fuzzy.decision import DecisionThresholds, make_decision
from three_way_fuzzy.model import PictureFuzzyNumber
from three_way_fuzzy.pfpo import OperatorParameters, iterate_sequence

TITLE = "Three-Way Fuzzy Decision System"


def _prompt_float(label: str, validator: Callable[[float], None] | None = None) -> float:
    """Prompt for a float value, re-prompting on invalid input."""
    while True:
        raw_value = input(label).strip()
        try:
            value = float(raw_value)
        except ValueError:
            print(f"  Invalid number: {raw_value!r}. Please try again.")
            continue
        if validator is not None:
            try:
                validator(value)
            except ValueError as error:
                print(f"  {error} Please try again.")
                continue
        return value


def _prompt_unit_interval(label: str) -> float:
    def validator(value: float) -> None:
        if value < 0 or value > 1:
            raise ValueError("Value must be between 0 and 1.")

    return _prompt_float(label, validator)


def _prompt_yes_no(label: str) -> bool:
    while True:
        raw_value = input(label).strip().lower()
        if raw_value in ("y", "yes"):
            return True
        if raw_value in ("n", "no"):
            return False
        print("  Please answer 'y' or 'n'.")


def print_assessment(picture_fuzzy_number: PictureFuzzyNumber, thresholds: DecisionThresholds) -> None:
    result = make_decision(picture_fuzzy_number, thresholds)

    print()
    print("Picture Fuzzy Assessment")
    print("-" * 25)
    print(f"Positive membership: {picture_fuzzy_number.positive:.2f}")
    print(f"Neutral membership:  {picture_fuzzy_number.neutral:.2f}")
    print(f"Negative membership: {picture_fuzzy_number.negative:.2f}")
    print(f"Refusal/uncertainty: {picture_fuzzy_number.refusal:.2f}")
    print()
    print(f"Score: {picture_fuzzy_number.score:.2f}")
    print(f"Accuracy/certainty: {picture_fuzzy_number.accuracy:.2f}")
    print()
    print(f"Decision: {result.decision.value}")
    print()
    print("Explanation:")
    print(result.explanation)


def print_pfpo_table(
    picture_fuzzy_number: PictureFuzzyNumber,
    parameters: OperatorParameters,
    iterations: int,
) -> None:
    sequence = iterate_sequence(picture_fuzzy_number, parameters, iterations)

    print()
    print(f"{'Iteration':<10} | {'Positive':>10} | {'Neutral':>10} | {'Negative':>10} | {'Refusal':>10}")
    print("-" * 62)
    for step, value in enumerate(sequence):
        print(
            f"{step:<10} | {value.positive:>10.6f} | {value.neutral:>10.6f} "
            f"| {value.negative:>10.6f} | {value.refusal:>10.6f}"
        )


def run_interactive(thresholds: DecisionThresholds) -> None:
    print(TITLE)
    print("=" * len(TITLE))
    print()
    print("Enter a picture fuzzy number t = (positive, neutral, negative).")

    positive = _prompt_unit_interval("Positive membership (mu): ")
    neutral = _prompt_unit_interval("Neutral membership (eta): ")

    def negative_validator(value: float) -> None:
        if value < 0 or value > 1:
            raise ValueError("Value must be between 0 and 1.")
        if positive + neutral + value > 1:
            raise ValueError("positive + neutral + negative must not exceed 1.")

    negative = _prompt_float("Negative membership (nu): ", negative_validator)

    picture_fuzzy_number = PictureFuzzyNumber(positive, neutral, negative)
    print_assessment(picture_fuzzy_number, thresholds)

    if _prompt_yes_no("\nApply Picture Fuzzy Point Operator? (y/n): "):
        iota = _prompt_unit_interval("iota: ")
        alpha = _prompt_unit_interval("alpha: ")

        def beta_validator(value: float) -> None:
            if value < 0 or value > 1:
                raise ValueError("Value must be between 0 and 1.")
            if iota + alpha + value > 1:
                raise ValueError("iota + alpha + beta must not exceed 1.")

        beta = _prompt_float("beta: ", beta_validator)

        def iteration_validator(value: float) -> None:
            if value < 0 or value != int(value):
                raise ValueError("Number of iterations must be a non-negative integer.")

        iterations = int(_prompt_float("Number of iterations: ", iteration_validator))

        parameters = OperatorParameters(iota, alpha, beta)
        print_pfpo_table(picture_fuzzy_number, parameters, iterations)


def run_batch(input_path: str, output_path: str | None, thresholds: DecisionThresholds) -> None:
    results = process_csv(input_path, output_path, thresholds)

    header = f"{'case_id':<10} | {'positive':>8} | {'neutral':>8} | {'negative':>8} | {'refusal':>8} | {'score':>7} | {'decision':<8}"
    print(header)
    print("-" * len(header))
    for row in results:
        print(
            f"{row['case_id']:<10} | {row['positive']:>8.2f} | {row['neutral']:>8.2f} "
            f"| {row['negative']:>8.2f} | {row['refusal']:>8.2f} | {row['score']:>7.2f} "
            f"| {row['decision']:<8}"
        )

    if output_path is not None:
        print(f"\nResults written to {output_path}")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="three-way-fuzzy",
        description=TITLE,
    )
    parser.add_argument(
        "--batch",
        metavar="INPUT_CSV",
        help="Path to a CSV file of cases (case_id, positive, neutral, negative) "
        "to process in batch mode instead of the interactive prompt.",
    )
    parser.add_argument(
        "--output",
        metavar="OUTPUT_CSV",
        help="Optional path to write batch results to as a CSV file.",
    )
    parser.add_argument(
        "--accept-threshold",
        type=float,
        default=DecisionThresholds().accept_score_threshold,
        help="Score threshold above which a case is accepted (default: 0.30).",
    )
    parser.add_argument(
        "--reject-threshold",
        type=float,
        default=DecisionThresholds().reject_score_threshold,
        help="Score threshold below which a case is rejected (default: -0.30).",
    )
    parser.add_argument(
        "--max-uncertainty",
        type=float,
        default=DecisionThresholds().maximum_uncertainty_for_commitment,
        help="Maximum refusal degree allowed for a committed decision (default: 0.25).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    thresholds = DecisionThresholds(
        accept_score_threshold=args.accept_threshold,
        reject_score_threshold=args.reject_threshold,
        maximum_uncertainty_for_commitment=args.max_uncertainty,
    )

    try:
        if args.batch:
            run_batch(args.batch, args.output, thresholds)
        else:
            run_interactive(thresholds)
    except (KeyboardInterrupt, EOFError):
        print("\nAborted.")
        return 1
    except (ValueError, FileNotFoundError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
