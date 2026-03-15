# 🗺️ Knowledge Map

Track your understanding across all topics. Update this regularly as you learn.

**Status Legend:**
- ✅ Solid — I can explain this clearly
- 🟡 Partial — I have a rough understanding but gaps remain
- ❌ Gap — Haven't covered this yet / very weak
- 🔄 In Progress — Actively studying this now

---

## 🚨 Priority: Rise Data Labs Internship (LLM-as-a-Judge)

> Crash course: [`evals/llm_judge_architecture.md`](./evals/llm_judge_architecture.md) | Email draft: [`rise_data_labs_reply.md`](./rise_data_labs_reply.md)

| Topic | Status | Notes |
|---|---|---|
| LLM-as-a-Judge architecture patterns | 🔄 | Single, reference-based, pairwise — see crash course |
| Multi-layered rubric design | 🔄 | Atomic criteria, anchored scales, CoT-before-verdict |
| Judge bias types & mitigation | 🔄 | Position, verbosity, self-enhancement bias |
| MT-Bench paper (Zheng et al. 2023) | ❌ | **Must read** — foundational paper for this role |
| G-Eval paper (Liu et al. 2023) | ❌ | Rubric-based structured eval with GPT-4 |
| Reasoning benchmarks (GSM8K, MATH, BBH) | ❌ | See crash course section 4 |
| CoT faithfulness evaluation | ❌ | Does the model actually use its reasoning? |
| Inter-rater reliability (Cohen's Kappa) | ❌ | How to measure judge vs. human agreement |
| RAGAS / LangSmith / Braintrust | ❌ | Production eval frameworks |

---

## AI Safety


| Topic | Status | Notes / Next Step |
|---|---|---|
| Why AI Safety matters | ❌ | Start with `ai_safety/overview.md` |
| Alignment problem | ❌ | What does it mean for AI to be "aligned"? |
| RLHF (Reinforcement Learning from Human Feedback) | ❌ | Key technique behind ChatGPT etc. |
| Constitutional AI | ❌ | Anthropic's approach |
| Scalable oversight | ❌ | How do we supervise AI smarter than us? |
| Mechanistic interpretability | ❌ | Understanding what's inside the model |
| Adversarial robustness | ❌ | Making models resistant to attacks |
| Mesa-optimization / inner alignment | ❌ | Emergent goals inside trained models |
| Deceptive alignment | ❌ | Model behaves well during training, not deployment |
| AI governance & policy | ❌ | Regulations, institutions, frameworks |

---

## Evals

| Topic | Status | Notes / Next Step |
|---|---|---|
| What evals are and why they matter | ❌ | Start with `evals/overview.md` |
| Standard benchmarks (MMLU, HellaSwag, etc.) | ❌ | See `evals/benchmarks.md` |
| Capability evaluations | ❌ | Measuring what a model *can* do |
| Safety evaluations | ❌ | Measuring alignment/safety properties |
| Red-teaming | ❌ | Adversarial probing of model behavior |
| Eval design methodology | ❌ | How to build a good eval |
| Limitations of current evals | ❌ | Goodhart's law, benchmark saturation |
| Model cards & transparency | ❌ | Standardized reporting |
| **Hallucination detection** | 🟡 | Hands-on hackathon experience — see `evals/hallucination_detection.md` |
| **AlignScore** | ✅ | Used in hackathon, worked well; understand NLI basis, strengths, and latency advantage over LLM-as-Judge |
| **LLM-as-a-Judge** | 🟡 | Core pattern understood; know biases; gaps in best-practice prompt design |
| **Inspect AI (UK AISI)** | 🟡 | Know it's a framework, not a scorer; haven't built a pipeline with it yet |
| Faithfulness vs. factual accuracy distinction | ❌ | What's the difference? How do metrics handle this? |
| RAGAS (RAG eval framework) | ❌ | How does it compare to AlignScore / LLM-as-Judge? |

---

## Key Organizations to Know

| Org | Status | Notes |
|---|---|---|
| OpenAI | ❌ | Safety team, superalignment initiative |
| Anthropic | ❌ | Constitutional AI, interpretability |
| DeepMind | ❌ | Spec gaming, agent safety |
| ARC (Alignment Research Center) | ❌ | Evals for dangerous capabilities |
| METR (formerly ARC Evals) | ❌ | Autonomous replication evals |
| Redwood Research | ❌ | Adversarial training |
| Center for AI Safety (CAIS) | ❌ | Policy + technical safety |

---

## Open Questions I Want to Answer

> Add your open questions here as you go

- How does AlignScore compare to BERTScore, BLEURT, and SelfCheckGPT for hallucination detection?
- What are best practices for designing judge prompts for LLM-as-a-Judge to reduce position/self-enhancement bias?
- How does RAGAS fit into the faithfulness eval landscape?
- Which method (AlignScore vs. LLM-as-Judge) performed better on my hackathon dataset — and why?
- At what capability level does safety eval become critical vs. capability eval?
- 

---

*Updated: March 2026 — added hallucination detection section from hackathon experience*
