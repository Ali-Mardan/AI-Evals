# 🔬 Mechanistic Interpretability

> **Status in knowledge map:** ❌ → Update when reviewed

---

## Core Concept

**Mechanistic interpretability** (mech interp) aims to understand *how* neural networks compute what they compute — reverse-engineering the algorithms implemented by model weights.

Goal: go from "the model outputs X" → "the model outputs X *because* neurons A, B, C are implementing circuit Z."

---

## Why It Matters for Safety

- If we can understand what a model is doing internally, we can:
  - Detect deceptive alignment
  - Verify that a model isn't pursuing hidden goals
  - Build trust in high-stakes deployments

---

## Key Concepts

### Features
Individual directions in activation space that correspond to human-interpretable concepts (e.g., "is this a banana?", "is this code?").

### Circuits
Subgraphs of the network (specific attention heads + MLPs) that implement discrete algorithms.
> Famous example: "Indirect Object Identification" circuit in GPT-2

### Superposition
Models represent *more features than they have dimensions* by encoding features across multiple neurons simultaneously. Makes interpretation harder.

### Sparse Autoencoders (SAEs)
A technique to decompose activations into sparse, interpretable features — a major current research direction at Anthropic.

---

## Key Research (Anthropic's Interpretability Team)

| Paper/Post | Key Finding |
|---|---|
| *Zoom In: An Introduction to Circuits* (Olah et al.) | Neurons implement detectable, human-interpretable features |
| *In-context Learning and Induction Heads* | Identified a circuit responsible for pattern completion |
| *Towards Monosemanticity* | SAEs can find clean, monosemantic features |
| *Scaling Monosemanticity* | Scaled SAE findings to Claude Sonnet |

---

## Current Limitations

- Circuit analysis is extremely labor-intensive
- Most work is on small models or narrow tasks
- Unclear if mech interp can scale to frontier models

---

## Open Questions

- Can we build automated circuit discovery tools?
- Is superposition a fundamental barrier?
- Can mech interp findings translate to safety guarantees?

---

*Notes | Add your own understanding here as you learn*
