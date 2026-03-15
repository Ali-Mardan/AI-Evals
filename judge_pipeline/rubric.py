"""
rubric.py — Multi-layered evaluation rubric for LLM-as-a-Judge pipeline.

Defines the rubric dimensions and builds the judge prompt.
Design decisions:
- Chain-of-thought BEFORE scoring (reduces anchoring bias)
- Structured JSON output (deterministic parsing)
- Explicit dimension definitions with anchored scales (1-5)
- Role framing as domain expert
"""

RUBRIC_DIMENSIONS = {
    "accuracy": {
        "description": "Is the information in the response factually correct?",
        "scale": {
            1: "Completely wrong or fabricated",
            2: "Mostly incorrect with some correct elements",
            3: "Partially correct but with notable errors",
            4: "Mostly correct with minor issues",
            5: "Fully accurate with no factual errors"
        }
    },
    "reasoning_quality": {
        "description": "Does the response show clear, logical reasoning to reach its answer?",
        "scale": {
            1: "No reasoning shown, or reasoning is incoherent",
            2: "Weak or flawed reasoning",
            3: "Some reasoning present but incomplete or superficial",
            4: "Clear reasoning with minor gaps",
            5: "Thorough, well-structured reasoning that clearly supports the answer"
        }
    },
    "completeness": {
        "description": "Does the response fully address all parts of the question?",
        "scale": {
            1: "Does not address the question at all",
            2: "Addresses a small part of the question",
            3: "Addresses the question partially",
            4: "Mostly complete with minor omissions",
            5: "Fully addresses all aspects of the question"
        }
    },
    "conciseness": {
        "description": "Is the response appropriately concise without unnecessary padding or repetition?",
        "scale": {
            1: "Extremely bloated, padded, or repetitive",
            2: "Too verbose with significant unnecessary content",
            3: "Acceptable length but could be tighter",
            4: "Mostly concise with minor verbosity",
            5: "Perfectly concise — says exactly what's needed, nothing more"
        }
    }
}


def build_judge_prompt(question: str, response: str, context: str = None) -> str:
    """
    Build the full judge prompt.
    Instructs the judge to reason first, then score (CoT-before-verdict pattern).
    Uses JSON output for deterministic parsing.
    """
    context_block = f"\n<context>\n{context}\n</context>\n" if context else ""

    dimensions_text = ""
    for dim, info in RUBRIC_DIMENSIONS.items():
        scale_text = "\n".join(
            f"      {score}: {meaning}"
            for score, meaning in info["scale"].items()
        )
        dimensions_text += f"""
  - **{dim.upper()}**: {info["description"]}
    Scale:
{scale_text}
"""

    return f"""You are an expert AI response evaluator. Your task is to evaluate a response given by an AI model to a question.

First, think through your evaluation carefully. Then provide your scores in the required JSON format.
{context_block}
<question>
{question}
</question>

<response_to_evaluate>
{response}
</response_to_evaluate>

## Evaluation Dimensions
{dimensions_text}

## Instructions
1. First, briefly reason about each dimension (2-3 sentences each).
2. Then output a JSON block with your final scores.

Your reasoning:
[Think through each dimension here before scoring]

After your reasoning, output ONLY this JSON (no extra text after it):
```json
{{
  "accuracy": {{"score": <1-5>, "reason": "<one sentence>"}},
  "reasoning_quality": {{"score": <1-5>, "reason": "<one sentence>"}},
  "completeness": {{"score": <1-5>, "reason": "<one sentence>"}},
  "conciseness": {{"score": <1-5>, "reason": "<one sentence>"}},
  "overall": <average of the four scores, rounded to 1 decimal>
}}
```"""
