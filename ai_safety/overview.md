# 🛡️ AI Safety — Overview

> **Status in knowledge map:** ❌ → Update `knowledge_map.md` as you progress

---

## What is AI Safety?

AI Safety is the field concerned with ensuring that AI systems behave in ways that are safe, reliable, and aligned with human values — especially as systems become more capable.

The core concern: **as AI becomes more powerful, mistakes become more costly and harder to correct.**

---

## The Core Problems

### 1. Alignment
Making sure AI systems pursue the goals *we actually want*, not a proxy that seems similar.
> See [`alignment.md`](./alignment.md)

### 2. Robustness
Making sure AI systems behave reliably across diverse, unexpected, or adversarial inputs.
> See [`robustness.md`](./robustness.md)

### 3. Interpretability
Understanding *what* a model is doing internally — making the "black box" transparent.
> See [`interpretability.md`](./interpretability.md)

### 4. Scalable Oversight
How do we supervise AI systems that are smarter than us at some tasks?

### 5. Governance
What policies, institutions, and norms do we need to manage AI development safely?

---

## Why It Matters Now

- Models are being deployed in high-stakes domains (healthcare, law, finance, infrastructure)
- Capabilities are scaling rapidly and unpredictably
- Misaligned or misused systems at scale could cause significant harm

---

## Key Mental Models

- **Goodhart's Law**: When a measure becomes a target, it ceases to be a good measure. AI systems optimizing a proxy goal can diverge badly.
- **Specification gaming**: AI finds ways to satisfy the letter, not the spirit, of its objective.
- **Inner vs. outer alignment**: Does the model learn the goal you trained it on, or a goal that merely *looks* right during training?

---

## Open Questions

- At what capability level does safety become truly critical?
- Can we verify alignment, or only approximate it?
- Is interpretability sufficient for safety?

---

*Notes | Update status in `knowledge_map.md` when reviewed*
