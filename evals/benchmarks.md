# 📐 Benchmarks

> **Status in knowledge map:** ❌ → Update when reviewed

---

## What Is a Benchmark?

A **benchmark** is a standardized dataset + evaluation protocol used to compare AI models on a defined task. Benchmarks enable reproducible, apples-to-apples comparisons across model versions and organizations.

---

## 🧠 General Capability Benchmarks

| Benchmark | What It Tests | Notes |
|---|---|---|
| **MMLU** | Multi-task language understanding (57 subjects) | Most widely used; near-saturated by frontier models |
| **BIG-Bench** | Diverse tasks beyond standard NLP | 204 tasks, harder tail |
| **HELM** | Holistic evaluation (accuracy + fairness + efficiency) | Stanford's broad framework |
| **GPQA** | Graduate-level Q&A in science | Very hard; PhD-level |
| **ARC-Challenge** | Grade-school science (hard subset) | |

---

## 💻 Coding & Math

| Benchmark | What It Tests | Notes |
|---|---|---|
| **HumanEval** | Python coding from docstrings | OpenAI; widely used |
| **MBPP** | Mostly Basic Python Programming | Google |
| **MATH** | Competition math | Hard; AMC/AIME level |
| **GSM8K** | Grade-school math word problems | Now near-saturated |
| **SWE-Bench** | Real GitHub issues → code fixes | Agent-level coding |

---

## 🛡️ Safety & Alignment Benchmarks

| Benchmark | What It Tests | Notes |
|---|---|---|
| **TruthfulQA** | Does model give truthful answers vs. popular misconceptions? | |
| **BBQ** | Bias in question answering | Social bias across demographics |
| **WMDP** | Dangerous knowledge (bio, chem, cyber) | Used as proxy for uplift risk |
| **HarmBench** | Standardized red-teaming benchmark | |
| **MACHIAVELLI** | Does model pursue power/resources in agent tasks? | |

---

## 🤖 Agent / Autonomous Capability Evals

| Benchmark | What It Tests | Notes |
|---|---|---|
| **GAIA** | Real-world general assistant tasks | Hard for current models |
| **AgentBench** | Operating system, web, DB agent tasks | |
| **METR's Task Suite** | Autonomous replication & resource acquisition | Key for dangerous capability evals |

---

## Benchmark Limitations

- **Contamination**: Training data may include benchmark test sets
- **Saturation**: Frontier models score 90%+ → no longer differentiates
- **Gaming**: Models optimized for benchmarks may not generalize
- **Narrow scope**: Each benchmark tests a slice; no single holistic score

---

*Notes | Update `knowledge_map.md` when reviewed*
