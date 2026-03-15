# 🔍 Hallucination Detection in LLM Outputs

> **Status in knowledge map:** 🟡 Partial — explored during hackathon, gaps remain
> **Hands-on experience:** ✅ Applied to educational QA dataset (hackathon)

---

## The Problem

When an LLM responds to a question it was given **context** for, there are several possible failure modes:

| Label | Meaning |
|---|---|
| ✅ **Factual** | Response is correct and grounded in the provided context |
| ❌ **Contradiction** | Response is factually incorrect (hallucinated or wrong) |
| 🚫 **Irrelevant** | Response has nothing to do with the question |

The core eval challenge: **given (question, context, answer) → predict the label as a 3-class classification.**

---

## My Hackathon Task — Data4Good Competition (4th Annual)

**Competition**: University Data4Good Challenge — 6,000 points available  
**Domain**: AI-generated educational content factuality detection

### Dataset
| Split | Size | Columns |
|---|---|---|
| Train | 21,021 examples | `question`, `context`, `answer`, `type` |
| Test | 2,000 examples | `question`, `context`, `answer`, `id` (predict `type`) |

**Labels**: `Factual` / `Contradiction` / `Irrelevant`

### Scoring
- Custom weighted confusion matrix
- **Equal weight per class: 33.3% each**
- Key implication: being bad at detecting Irrelevant costs just as much as being bad at Factual or Contradiction

### What I Did
- Used **AlignScore** on (context, answer) pairs
- Got a continuous [0,1] faithfulness score
- Thresholded the score to predict the 3 classes
- Result: mostly working — picked up Factual vs Contradiction reasonably well

---

## 🔍 Retrospective — What Actually Happened & What Would Have Won

### Why AlignScore Was a Partial Solution

AlignScore measures **context faithfulness**: does the answer align with the context?

| Class | AlignScore Signal | Reliability |
|---|---|---|
| **Factual** | High alignment score | ✅ Good |
| **Contradiction** | Low alignment score | ✅ Good |
| **Irrelevant** | ❓ Unpredictable | ❌ Poor |

**The Irrelevant problem**: an irrelevant answer (one that doesn't address the question at all) might still accidentally align with the context passage — AlignScore has no way to detect topic mismatch between the *question* and the *answer*. This likely hurt performance on the 33.3% of the score that depended on Irrelevant detection.

**What Irrelevant actually needs**: semantic similarity between the **question** and **answer** (not context and answer). A response that's off-topic will be semantically distant from the question regardless of context.

### What the Missed Step Was
With 21K labeled training examples, the calibration approach alone was too limited. Better approaches:

#### Option 1: Two-Stage Pipeline (Most Practical)
```
1. Compute AlignScore(context, answer)  → detects Factual vs Contradiction
2. Compute cosine_sim(question, answer) → detects Irrelevant
3. Rule: if sim(Q,A) < threshold → Irrelevant
         elif alignscore < threshold  → Contradiction
         else                         → Factual
4. Calibrate thresholds on train set  → maximize per-class F1
```

#### Option 2: Fine-tuned NLI/Classifier (Would Have Won)
- Input: concatenate [question, context, answer] as a single sequence
- Fine-tune a **DeBERTa** or **RoBERTa** model on the 21K train examples
- Directly predicts the 3-way label
- 21K examples is enough to fine-tune well; NLI models transfer perfectly to this task
- This would have been the competition winner approach

#### Option 3: Zero-Shot LLM Classification
```python
prompt = f"""
Classify the answer as Factual, Contradiction, or Irrelevant.
Question: {question}
Context: {context}
Answer: {answer}
Respond with exactly one word: Factual, Contradiction, or Irrelevant."""
```
- More accurate than AlignScore for Irrelevant
- Too slow for 21K + 2K with rate limits (but viable for 2K test set if train isn't needed)

### Key Lessons
1. **Equal-weight scoring exposed my Irrelevant gap** — I likely scored well on Factual/Contradiction but poorly on Irrelevant
2. **AlignScore only covers one dimension** — faithfulness to context ≠ relevance to question
3. **21K labeled examples = a fine-tuning opportunity**, not just a calibration set
4. **Always check per-class scores**, not just overall accuracy

---

## Methods I Explored

### 1. ✅ AlignScore ← *used in hackathon, worked well*

**What it is**: A reference-based faithfulness metric. Given a *context* and a *claim* (the model's response), AlignScore outputs a score [0, 1] indicating how well the claim is *supported* by the context.

**How it works**:
- Fine-tuned NLI (Natural Language Inference) model
- Breaks response into sentences/claims → checks each against the context
- Returns alignment score per claim, aggregated to document level

**Strengths**:
- Doesn't require a separate LLM call (cheaper, faster)
- Grounded in NLI research (principled)
- Works well for factual consistency checking

**Weaknesses**:
- Can miss subtle hallucinations that are contextually plausible
- May penalize correct responses that go *beyond* the context (even if true)
- Not great at irrelevance detection

**When to use**: When you have a reference context and want to check if the response is *faithful* to it. Best for RAG (Retrieval-Augmented Generation) pipelines.

**Paper**: AlignScore: Evaluating Factual Consistency with a Unified Alignment Function (Zha et al., 2023)

---

### 2. 🟡 LLM-as-a-Judge ← *evaluated but not used — too slow*

**What it is**: Use a capable LLM (e.g., GPT-4, Claude) to evaluate another LLM's response, given a rubric or criteria.

**How it works**:
```
Prompt to judge LLM:
"Given the following context: [CONTEXT]
And the following question: [QUESTION]
Evaluate whether this response is accurate, hallucinated, or irrelevant:
[RESPONSE]
Respond with: label, confidence, and brief justification."
```

**Variants**:
- **Single judge**: one LLM scores the response
- **Reference-based**: judge compares response to a gold answer
- **Pairwise**: judge picks the better of two responses (used in LMSYS Chatbot Arena)

**Strengths**:
- Flexible — can evaluate nuanced properties (relevance, helpfulness, tone)
- Easy to prototype; minimal setup
- Can return explanations, not just scores

**Weaknesses**:
- Expensive (API costs per evaluation)
- **Slow** — each eval requires an LLM API call; not practical for large datasets *(confirmed in hackathon)*
- **Position bias**: judge tends to prefer first response in pairwise evals
- **Self-enhancement bias**: GPT-4 tends to prefer GPT-4 outputs
- Not deterministic — results vary across runs
- Can be wrong in confident-sounding ways

**When to use**: When you need flexible, nuanced evaluation and can afford API costs. Good for final-stage eval or when no reference context is available.

**Key paper**: *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* (Zheng et al., 2023)

---

### 3. 🟡 Inspect AI (UK AISI)

**What it is**: An open-source **evaluation framework** built by the UK AI Safety Institute (AISI). It's infrastructure for running evals, not a specific eval method.

**What it provides**:
- Structured way to define eval tasks, datasets, solvers (models), and scorers
- Built-in support for multiple model providers
- Logging, reproducibility, and result tracking
- Can plug in LLM-as-a-Judge or custom scorers

**Key distinction**: Inspect AI is a *framework* — it tells you how to *run* your eval pipeline, not *how to score* responses. You still need to choose your scoring method (AlignScore, LLM-as-judge, etc.).

**When to use**: When building a repeatable, structured eval pipeline across multiple models or datasets. Overkill for a one-off hackathon, but excellent for systematic eval work.

**Docs**: [inspect.ai](https://inspect.ai)

---

## Comparison Table

| Method | Type | Needs Context? | Needs Gold Answer? | Cost | Flexibility |
|---|---|---|---|---|---|
| AlignScore | Automated metric | ✅ Yes | ❌ No | Low | Low |
| LLM-as-Judge | LLM-powered | Optional | Optional | Medium–High | High |
| Inspect AI | Framework | Depends on scorer | Depends | Low (infra only) | High |

---

## What I Still Want to Learn

- [ ] How does AlignScore compare to other faithfulness metrics (BERTScore, BLEURT, SelfCheckGPT)?
- [ ] What are the best practices for designing judge prompts to minimize bias?
- [ ] How does RAGAS (RAG evaluation framework) fit into this landscape?
- [ ] What did the hackathon results show — which method performed best on my dataset?
- [ ] How does Inspect AI handle multi-turn conversation evals?

---

## Related Concepts

- **RAG (Retrieval-Augmented Generation)**: Architecture where an LLM is given retrieved context — faithfulness evals are critical here
- **NLI (Natural Language Inference)**: Backbone of AlignScore; classifies (premise, hypothesis) as entailment / neutral / contradiction
- **Factual consistency**: The property that a response doesn't contradict or fabricate facts relative to a source
- **Groundedness**: Response only makes claims supported by the provided context

---

*Notes | Updated: March 2026 | Hackathon experience*
