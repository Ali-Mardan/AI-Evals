# 📊 Evals — Overview

> **Status in knowledge map:** ❌ → Update when reviewed

---

## What Are Evals?

**Evaluations (evals)** are structured tests used to measure properties of AI models — their capabilities, behavior, risks, and alignment.

They are the primary tool for answering the question: *"Is this model safe/capable/aligned enough to deploy?"*

---

## Two Main Types

### Capability Evals
Measure *what a model can do*.
- Performance on benchmarks (code, math, reasoning, language)
- Example: MMLU, HumanEval, MATH, BIG-Bench

### Safety / Alignment Evals
Measure *how a model behaves* — does it follow guidelines, avoid harmful outputs, resist misuse?
- Example: TruthfulQA, BBQ (bias), WMDP (dangerous knowledge), uplift evals

---

## Why Evals Matter

- **Pre-deployment gates**: Should this model be released?
- **Red-teaming**: Find failure modes before attackers do
- **Regulatory compliance**: Governments increasingly require evals (EU AI Act, US EO)
- **Tracking progress**: Are models getting safer over time?

---

## The Eval Lifecycle

1. **Define the property** you want to measure (capability, safety, bias, etc.)
2. **Design the test** (prompts, scenarios, automated checks, human labeling)
3. **Run the eval** across model versions
4. **Interpret results** — what does the score actually mean?
5. **Act on results** — gate deployment, retrain, fine-tune

---

## Key Challenges

- **Goodhart's Law**: Models train on benchmarks → benchmarks stop measuring what they should
- **Benchmark saturation**: Models score near 100% → need harder evals
- **Unknown unknowns**: You can only eval for what you think to test
- **Specification gap**: Evals measure proxy metrics, not true safety

---

## Key Orgs Doing Evals Work

| Org | Focus |
|---|---|
| METR (formerly ARC Evals) | Autonomous capability & dangerous capability evals |
| Anthropic | Red-teaming, safety evals, constitutional AI |
| OpenAI | Alignment evals, Preparedness Framework |
| AISI (UK) | Government-level safety evals |
| Scale AI | Third-party eval benchmarking |

---

*See also: [`benchmarks.md`](./benchmarks.md) | [`methodologies.md`](./methodologies.md) | [`hallucination_detection.md`](./hallucination_detection.md)*
