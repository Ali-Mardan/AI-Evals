# 🛡️ Robustness

> **Status in knowledge map:** ❌ → Update when reviewed

---

## Core Concept

**Robustness** = a model's ability to maintain correct, safe behavior under distribution shift, unexpected inputs, or deliberate adversarial manipulation.

---

## Types of Robustness

### Distributional Robustness
Model performs well on data that differs from its training distribution.
- Example: model trained on formal text should still handle informal text or typos

### Adversarial Robustness
Model resists deliberate, crafted inputs designed to cause failure.
- **Adversarial examples**: small, imperceptible perturbations to input that flip model output
- **Prompt injection**: adversarial inputs in LLMs that override instructions

### Specification Robustness
Model doesn't exploit loopholes in its reward/objective (see alignment → specification gaming)

---

## Key Attacks

| Attack | Description |
|---|---|
| FGSM (Fast Gradient Sign Method) | Classic adversarial example attack on image classifiers |
| Prompt injection | Hidden instructions in user input override system prompt |
| Jailbreaking | Prompting techniques that bypass safety training |
| Data poisoning | Corrupting training data to embed a backdoor |

---

## Key Defenses

| Defense | Idea |
|---|---|
| Adversarial training | Include adversarial examples during training |
| Certified defenses | Provably bound model behavior within perturbations |
| Input preprocessing | Sanitize or transform inputs before feeding to model |
| Constitutional AI / RLHF | Reduce harmful outputs through fine-tuning |

---

## Open Questions

- Can we certify robustness for large language models?
- Is there an inherent tradeoff between robustness and performance?
- How do we evaluate robustness against unknown future attacks?

---

*Notes | Add your own understanding here as you learn*
