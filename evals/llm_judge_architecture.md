# 🏗️ LLM-as-a-Judge Architecture — Crash Course

> **Context**: Crash course for Rise Data Labs internship — building a platform that automates evaluation of frontier models using LLM-as-a-Judge with multi-layered rubrics.
> **Status in knowledge map:** 🔄 In Progress

---

## What This Role Is Really About

Rise Data Labs wants to build a **scalable eval pipeline** that:
- Takes a model's output (from GPT-4, Claude, Gemini, etc.)
- Runs it through a judge LLM using structured, multi-criteria rubrics
- Returns a score/verdict *automatically*, replacing slow human reviewers

This is production eval engineering, not just research.

---

## 1. LLM-as-a-Judge: Architecture Patterns

There are three main architectural patterns:

### Pattern A: Single-Model Absolute Scoring
```
Input: [System Prompt with Rubric] + [Question] + [Model Response]
Output: Score (1-5) + Justification
```
- Simple, scalable
- Risk: judge score may not correlate with human scores

### Pattern B: Reference-Based Scoring
```
Input: [Rubric] + [Question] + [Model Response] + [Gold Answer]
Output: Score + Justification
```
- More accurate when ground truth exists
- Requires curated reference answers

### Pattern C: Pairwise Comparison
```
Input: [Rubric] + [Question] + [Response A] + [Response B]
Output: "A is better" / "B is better" / "Tie" + Justification
```
- More reliable signal than absolute scoring
- Scales poorly (O(n²) comparisons)
- Used by: LMSYS Chatbot Arena, MT-Bench

---

## 2. Multi-Layered Rubrics — The Core Skill

A **multi-layered rubric** breaks evaluation into multiple independent criteria instead of one overall score.

### Example: Educational QA Rubric
```
You are an expert evaluator. Score the following response on 4 dimensions:

1. ACCURACY (1-5): Is the information factually correct?
2. GROUNDEDNESS (1-5): Is the response supported by the given context?
3. HELPFULNESS (1-5): Does it actually answer the student's question?
4. SAFETY (1-5): Is the response appropriate for an educational setting?

For each dimension, provide:
- Score: [1-5]
- Reason: [one sentence]

Context: {context}
Question: {question}
Response: {response}
```

### Why Multi-Layered Matters
- Decomposing evaluation → **more reliable** (judge can focus on one thing at a time)
- **Debuggable**: if accuracy is high but groundedness is low, you know the model is hallucinating
- **Granular**: you can weight dimensions differently for different use cases

### Design Principles for Good Rubrics
1. **Atomic criteria**: each dimension should test exactly one thing
2. **Anchored scales**: define what each score number means (don't just say 1-5)
3. **Examples in prompt**: few-shot examples dramatically improve consistency
4. **Chain-of-Thought before verdict**: ask judge to reason before scoring (reduces errors)
5. **Role framing**: "You are an expert in X" improves domain-specific reliability

---

## 3. Judge Bias — The Key Technical Problem

The biggest challenge in building a judge system is **controlling for bias**:

| Bias Type | What It Is | How to Mitigate |
|---|---|---|
| **Position bias** | Prefers Response A over B just because it's listed first | Swap order, average both scores |
| **Verbosity bias** | Prefers longer responses | Explicit rubric criterion against verbosity |
| **Self-enhancement bias** | GPT-4 judge prefers GPT-4 responses | Use different judge model from evaluated model |
| **Sycophancy** | Judge agrees with the user's implied preference | Neutral, unbiased system prompt framing |
| **Anchoring** | First score influences later scores | Evaluate each criterion independently |

### Mitigation Strategies in Practice
- **Multi-judge consensus**: run 3 judges, take majority vote
- **Temperature = 0**: deterministic output, more consistent
- **Calibration set**: test judge against known human labels, adjust
- **Structured output**: force JSON output (score + reason) to reduce noise

---

## 4. Benchmarking Model Reasoning

"Benchmarking model reasoning" specifically = evaluating how well models do **multi-step logical thinking**.

### Key Reasoning Benchmarks

| Benchmark | What It Tests | Why It's Hard |
|---|---|---|
| **GSM8K** | Grade-school math word problems | Multi-step arithmetic + language |
| **MATH** | Competition math | AMC/AIME level; models still struggle |
| **ARC-Challenge** | Science reasoning (grade school, hard subset) | Requires background knowledge |
| **GPQA** | Graduate-level science Q&A | PhD-level; very hard |
| **BBH (BIG-Bench Hard)** | 23 hard reasoning tasks | Logical deduction, temporal reasoning |
| **HellaSwag** | Commonsense inference | Now saturated by frontier models |

### Chain-of-Thought (CoT) Evaluation
- A key eval question: *does the model's reasoning trace actually support its answer?*
- **Faithfulness of CoT**: does the model use the reasoning it wrote, or is the reasoning post-hoc?
- See: *Measuring Faithfulness in Chain-of-Thought Reasoning* (Lanham et al., 2023)

---

## 5. Building the Pipeline (What They'll Actually Have You Do)

A minimal LLM-as-a-Judge pipeline looks like:

```python
# Pseudocode structure
def evaluate(question, context, model_response, rubric):
    prompt = format_judge_prompt(rubric, question, context, model_response)
    judge_output = call_llm(model="gpt-4", prompt=prompt, temperature=0)
    scores = parse_json(judge_output)  # {accuracy: 4, groundedness: 3, ...}
    return scores

# For a dataset:
results = [evaluate(**row) for row in dataset]
aggregate_scores(results)
compare_to_human_labels(results, ground_truth)
```

### Key Engineering Challenges
- **Prompt versioning**: track which rubric version produced which results
- **Cost management**: GPT-4 calls add up; cache results, use cheaper models where possible
- **Failure handling**: LLM outputs are non-deterministic; parse failures happen
- **Evaluation of the evaluator**: how do you know your judge is good? → compare to human labels (Cohen's Kappa, correlation)

---

## 6. Frameworks to Know

| Tool | What It Is | Relevance |
|---|---|---|
| **Inspect AI** (UK AISI) | Open-source eval framework | Good for structured pipelines |
| **RAGAS** | RAG evaluation library | Has LLM-as-Judge built in |
| **OpenAI Evals** | OpenAI's eval format | Industry standard format |
| **LangChain / LangSmith** | LLM tooling + eval tracing | Common in industry pipelines |
| **Braintrust** | Eval + tracing platform | Increasingly popular for prod evals |

---

## 7. Key Papers to Know (Skim, Not Deep-Read)

- [ ] *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* — Zheng et al. (2023) — **THE foundational paper**
- [ ] *Calibrating LLM-Based Evaluator* — Liu et al. (2023) — bias mitigation
- [ ] *G-Eval: NLG Evaluation using GPT-4* — Liu et al. (2023) — rubric-based structured eval
- [ ] *Measuring Faithfulness in Chain-of-Thought* — Lanham et al. (2023)

---

## My Knowledge Gaps for This Role

- [ ] Haven't built a full judge pipeline end-to-end
- [ ] Need to understand JSON-mode prompting for structured output
- [ ] Haven't read the MT-Bench paper (the key one)
- [ ] Need to understand how to measure inter-rater reliability between judge and humans

---

*Crash course for Rise Data Labs internship | March 2026*
