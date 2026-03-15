# LLM-as-a-Judge Evaluation Pipeline

A minimal but production-minded pipeline that evaluates frontier AI models against a **multi-layered rubric**, using GPT-4o-mini as the judge.

Built to demonstrate the core architecture of automated model evaluation — the problem Rise Data Labs is solving at scale.

---

## What It Does

1. **Sends the same 5 reasoning questions** to two models (`gpt-3.5-turbo` and `gpt-4o-mini`)
2. **Judges each response** using a GPT-4o-mini judge with a structured, multi-dimensional rubric
3. **Outputs scored results** to `results.csv` with per-dimension scores and judge reasoning
4. **Prints a comparison summary** showing which model performs better across dimensions

---

## Architecture

```
run_eval.py          ← orchestrates the pipeline
   ├── calls models to evaluate (gpt-3.5, gpt-4o-mini)
   ├── passes each response to judge.py
   └── aggregates results → results.csv

judge.py             ← the judge
   ├── builds prompt via rubric.py
   ├── calls gpt-4o-mini at temperature=0
   └── extracts JSON scores with retry on parse failure

rubric.py            ← rubric definition
   ├── 4 dimensions: accuracy, reasoning_quality, completeness, conciseness
   └── anchored 1-5 scales + CoT-before-verdict prompt pattern
```

---

## Key Design Decisions

| Decision | Rationale |
|---|---|
| `temperature=0` for judge | Deterministic, reproducible scores |
| Chain-of-thought before scoring | Reduces anchoring bias; forces reasoning |
| JSON structured output | Eliminates ambiguous free-text parsing |
| Retry + fallback regex | LLM outputs are non-deterministic; hard failures happen |
| Separate judge model from evaluated models | Avoids self-enhancement bias |
| Anchored scales (not just 1-5) | Each score value is defined, reducing inter-judge variance |

---

## Setup

```bash
pip install openai
export OPENAI_API_KEY=your_key_here
```

## Run

```bash
# Standard run
python run_eval.py

# With judge reasoning printed
python run_eval.py --verbose

# Custom output file
python run_eval.py --output my_results.csv
```

---

## Output

`results.csv` columns:
- `question_id`, `domain`, `question`, `model`, `response`
- `accuracy`, `reasoning_quality`, `completeness`, `conciseness`, `overall` (scores 1-5)
- `*_reason` — judge's one-sentence justification per dimension

Console summary:
```
📊 SUMMARY — Average Scores by Model
Dimension              gpt-3.5-turbo       gpt-4o-mini
accuracy               3.80                4.40
reasoning_quality      3.20                4.20
completeness           4.00                4.60
conciseness            3.60                4.00
overall                3.65                4.30
```

---

## Extending This

- **Add more models**: append to `MODELS_TO_EVALUATE` in `run_eval.py`
- **Add context-grounded eval**: pass `context=` to `judge_response()` in `judge.py`
- **Add pairwise comparison**: modify `judge.py` to compare Response A vs B directly
- **Bias check**: swap model order and re-run; scores should be stable (position bias check)
- **Calibrate against human labels**: compare judge scores to ground-truth labels using Cohen's Kappa
