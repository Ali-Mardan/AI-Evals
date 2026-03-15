# 🔧 Eval Methodologies

> **Status in knowledge map:** ❌ → Update when reviewed

---

## How to Design a Good Eval

A good eval should be:
- **Valid**: actually measures the property you care about
- **Reliable**: consistent results across runs
- **Sensitive**: can detect real differences between models
- **Resistant to gaming**: hard to score well without truly having the property

---

## Methodology Types

### 1. Multiple Choice / Classification
- Prompt the model with a question + options, score by correct answer selection
- Easy to automate, fast, cheap
- Risk: model may choose correct answer without real understanding (position bias, etc.)

### 2. Open-ended Generation + LLM-as-Judge
- Model generates a free-text response
- A separate LLM (e.g., GPT-4) scores the response
- Scales well; risk of judge bias, inconsistency

### 3. Human Evaluation
- Human raters assess model outputs
- Most valid but expensive, slow, hard to scale
- Used for final safety checks, alignment assessment

### 4. Automated Code Execution
- Model writes code; run it against test cases
- Ground-truth signal; used in HumanEval, SWE-Bench

### 5. Agent/Task Completion Evals
- Model operates in an environment (web, OS, tool use)
- Binary or graded success on multi-step tasks
- Used in METR evals, SWE-Bench, GAIA

---

## Red-Teaming

A **red team** adversarially probes a model to find failure modes before deployment.

Types:
- **Manual red-teaming**: Human experts try to elicit harmful behavior
- **Automated red-teaming**: Use another model to generate adversarial prompts
- **Structured red-teaming**: Systematic protocol across risk categories (CBRN, CSAM, cyberweapons, etc.)

Key frameworks:
- Anthropic's model card disclosures
- OpenAI's Preparedness Framework
- METR's autonomous capability evaluations

---

## Eval Pitfalls

| Pitfall | Description |
|---|---|
| **Data contamination** | Test set appears in training data |
| **Prompt sensitivity** | Results change with minor prompt rewording |
| **Metric-target mismatch** | High score doesn't mean safe/aligned |
| **Distribution shift** | Eval doesn't reflect real deployment conditions |
| **Clever Hans** | Model uses spurious cues, not the intended skill |

---

## Emerging Best Practices

- Run evals across multiple prompting formats (zero-shot, few-shot, chain-of-thought)
- Use multiple evals for the same property
- Track results across model versions to detect regression
- Be transparent about eval limitations in model cards

---

*Notes | Update `knowledge_map.md` when reviewed*
