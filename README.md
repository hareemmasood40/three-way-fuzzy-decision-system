# Three-Way Fuzzy Decision System

A Python implementation and educational demonstration inspired by mathematical concepts from my MPhil research on picture fuzzy sets and three-way decision-making under uncertainty.

## Overview

This project explores how mathematical decision-making under uncertainty can be implemented computationally. It accepts uncertain information represented as a **picture fuzzy number** `t = (μ, η, ν)` — positive, neutral and negative membership degrees — and produces an explainable **three-way decision**: accept, defer/non-commitment, or reject.

The project is deliberately small, deterministic and dependency-free. It is meant as a computational portfolio piece connecting a mathematics background to interpretable, uncertainty-aware computing.

## Research Background

This project is inspired by my MPhil Mathematics thesis, **"Three-Way Decisions on Picture Fuzzy Rough Sets."** The original research investigated uncertainty, picture fuzzy sets, rough-set-based decision models, and three-way decisions.

This repository does **not** reproduce the entire thesis. It implements selected mathematical building blocks — the picture fuzzy number, its score/accuracy functions, the Picture Fuzzy Point Operator, and a simplified three-way decision rule — as an educational, computational demonstration.

## Why Three-Way Decisions?

Traditional binary systems force a choice between:

- accept
- reject

Three-way decision theory introduces a middle ground:

- accept
- defer / non-commitment
- reject

Deferral is valuable when the available evidence is too uncertain to justify a confident commitment. Rather than forcing a premature accept or reject, the system can explicitly say "not enough information yet."

The ability to defer decisions under uncertainty is also relevant to trustworthy and autonomous AI systems, where acting despite insufficient evidence may be undesirable. This project does not claim to be such a system — it is a small, transparent demonstration of the underlying mathematical idea.

## Picture Fuzzy Representation

A picture fuzzy number represents a judgement using three independent degrees:

- **Positive membership (μ)** — degree of support/agreement
- **Neutral membership (η)** — degree of neutrality/indifference
- **Negative membership (ν)** — degree of opposition/disagreement

These must satisfy `μ + η + ν ≤ 1`. Whatever is left over is the **refusal/hesitation degree**:

```
π = 1 - μ - η - ν
```

From these, the system computes:

- **Score**: `S(t) = μ - η - ν`
- **Accuracy/certainty**: `H(t) = μ + η + ν`

## Picture Fuzzy Point Operator

The Picture Fuzzy Point Operator (PFPO) redistributes part of a picture fuzzy number's refusal/hesitation degree into its positive, neutral and negative components. Repeated application lets us study how uncertainty evolves — typically shrinking — over successive iterations.

One-step transformation, with operator parameters `ι, α, β ∈ [0,1]`, `ι + α + β ≤ 1`:

```
E(t) = (μ + ιπ, η + απ, ν + βπ)
```

Iterative form (`n` steps, `r = ι + α + β`):

```
factor = [1 - (1-r)^n] / r        (when r ≠ 0)
μₙ = μ + ιπ·factor
ηₙ = η + απ·factor
νₙ = ν + βπ·factor
πₙ = (1-r)^n · π
```

When `ι + α + β = 0`, the picture fuzzy number is unchanged.

## Features

- Picture fuzzy number validation
- Uncertainty (refusal) calculation
- Score and accuracy functions
- Explainable three-way decisions with configurable thresholds
- Picture Fuzzy Point Operator simulation (single-step and iterative)
- Iterative uncertainty tracking table
- Interactive command-line interface
- CSV batch processing
- Automated test suite (pytest), including a thesis-inspired numerical example

## Installation

Requires Python 3.11+.

Using [uv](https://github.com/astral-sh/uv):

```bash
uv sync
```

Using standard `pip` (inside a virtual environment):

```bash
python -m venv .venv
.venv\Scripts\activate      # on Windows
source .venv/bin/activate   # on macOS/Linux
pip install -e ".[dev]"
```

## Usage

### Interactive CLI

```bash
python -m three_way_fuzzy.cli
```

or, after installation:

```bash
three-way-fuzzy
```

You will be prompted for `μ`, `η`, `ν`, and shown the score, accuracy, refusal degree, decision and explanation. You can optionally apply the Picture Fuzzy Point Operator and view how uncertainty evolves over several iterations.

### Batch CSV mode

```bash
three-way-fuzzy --batch sample_data/example_cases.csv --output results.csv
```

Input CSV format:

```csv
case_id,positive,neutral,negative
case_1,0.70,0.10,0.05
case_2,0.20,0.20,0.50
case_3,0.35,0.25,0.20
```

### As a library

```python
from three_way_fuzzy.model import PictureFuzzyNumber
from three_way_fuzzy.decision import make_decision

value = PictureFuzzyNumber(positive=0.70, neutral=0.10, negative=0.05)
result = make_decision(value)

print(result.decision)      # Decision.ACCEPT
print(result.explanation)   # "ACCEPT because the score (0.55) exceeds..."
```

See [`examples/example_usage.py`](examples/example_usage.py) for a fuller worked example, including the thesis-inspired PFPO trajectory.

## Example

For `t = (0.70, 0.10, 0.05)`:

```
Picture Fuzzy Assessment
-------------------------
Positive membership: 0.70
Neutral membership:  0.10
Negative membership: 0.05
Refusal/uncertainty: 0.15

Score: 0.55
Accuracy/certainty: 0.85

Decision: ACCEPT

Explanation:
ACCEPT because the score (0.55) exceeds the acceptance threshold (0.30)
and refusal uncertainty (0.15) is below the allowed commitment
threshold (0.25).
```

## Project Structure

```text
three-way-fuzzy-decision-system/
│
├── README.md
├── pyproject.toml
├── .gitignore
│
├── src/
│   └── three_way_fuzzy/
│       ├── __init__.py     # Public package API
│       ├── model.py        # PictureFuzzyNumber: validation, refusal, score, accuracy
│       ├── decision.py     # Three-way decision policy (ACCEPT/DEFER/REJECT) + explanations
│       ├── pfpo.py         # Picture Fuzzy Point Operator (single-step and iterative)
│       ├── batch.py        # CSV batch processing
│       └── cli.py          # Interactive command-line interface
│
├── examples/
│   └── example_usage.py    # Worked library usage example
│
├── sample_data/
│   └── example_cases.csv   # Sample CSV for batch mode
│
└── tests/
    ├── test_model.py       # PictureFuzzyNumber tests
    ├── test_decision.py    # Decision policy tests
    └── test_pfpo.py        # PFPO tests, incl. thesis-inspired numerical example
```

## Academic Integrity / Scope

This repository is a computational portfolio project inspired by selected concepts from my MPhil research. It is not presented as a complete reproduction of the thesis or as a novel published research contribution.

The default decision thresholds used in `decision.py` (e.g. `accept_score_threshold = 0.30`) are illustrative demonstration values chosen for this software, not results derived from the thesis. The decision policy is intentionally isolated in its own module so it can be replaced with a more rigorous decision-theoretic model (e.g. one based on loss functions over rough approximations, as studied in the thesis) without affecting the rest of the codebase.

## Future Work

- Decision-theoretic loss matrices for the three-way decision rule
- Learning thresholds from data rather than fixing them by hand
- Uncertainty calibration
- Comparison with probabilistic approaches to decision-making under uncertainty
- Integration with machine-learning model outputs (e.g. treating predictive confidence as a picture fuzzy number)
- Uncertainty-aware autonomous decision systems that defer to a human when confidence is insufficient
