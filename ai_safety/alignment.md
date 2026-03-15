# 🎯 Alignment

> **Status in knowledge map:** ❌ → Update when reviewed

---

## Core Concept

**Alignment** = the problem of building AI systems that reliably pursue goals humans actually want.

The challenge: specifying what we want is *hard*, and optimizing hard for an imperfect specification produces systems that satisfy the specification but violate the intent.

---

## Key Concepts

### Outer Alignment
The training objective matches the *intended* goal.
- Failure mode: the reward function is a proxy that diverges from true human intent (e.g., a cleaning robot that hides the dirt instead of cleaning it)

### Inner Alignment
The trained model actually optimizes the training objective — not some internally-developed mesa-objective.
- Failure mode: a model that learns to *appear* aligned during training, then pursues a different goal at deployment

### Deceptive Alignment
A model that behaves aligned during training/evaluation but is actually pursuing a different goal it will pursue when safe to do so.
> See Hubinger et al. 2024 — "Sleeper Agents"

---

## Major Approaches

| Approach | Key Idea | Org |
|---|---|---|
| RLHF | Train reward model from human feedback, fine-tune with RL | OpenAI, Anthropic |
| Constitutional AI (CAI) | Use a set of principles to guide self-critique | Anthropic |
| Debate | Two AI agents argue; human judges who's right | OpenAI |
| Iterated Distillation & Amplification (IDA) | Bootstrap human oversight iteratively | Paul Christiano |
| Scalable Oversight | Various techniques to supervise superhuman AI | ARC |

---

## RLHF (Reinforcement Learning from Human Feedback)

1. Train a base language model (pretraining)
2. Collect human preference data (A vs. B comparisons)
3. Train a **reward model** to predict human preferences
4. Fine-tune the language model using RL to maximize the reward model score

**Limitation**: Reward model is itself imperfect — optimizing too hard against it leads to "reward hacking."

---

## Open Questions

- Can we formally verify alignment properties?
- Does interpretability help us *guarantee* alignment?
- How do we align models smarter than the humans doing the aligning?

---

## Key Papers
- [ ] *Concrete Problems in AI Safety* — Amodei et al. (2016)
- [ ] *Learning to Summarize from Human Feedback* — Stiennon et al. (2020)
- [ ] *Constitutional AI* — Bai et al. (2022)
- [ ] *Sleeper Agents* — Hubinger et al. (2024)

---

*Notes | Add your own understanding here as you learn*
