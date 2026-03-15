"""
run_eval.py — End-to-end evaluation pipeline.

Sends the same questions to two models (gpt-3.5-turbo vs gpt-4o-mini),
then judges both responses using our multi-layered rubric judge.

This directly mirrors Rise Data Labs' goal:
  "automate evaluation of frontier models against complex, multi-layered rubrics"

Usage:
    python run_eval.py                  # runs full eval, saves results.csv
    python run_eval.py --verbose        # prints judge reasoning
"""

import argparse
import csv
import os
import time
from openai import OpenAI
from judge import judge_response

client = OpenAI()

# ── Sample Questions ─────────────────────────────────────────────────────────
# Reasoning-focused questions across domains.
# These exercise multi-step thinking, the core of "benchmarking model reasoning."
EVAL_QUESTIONS = [
    {
        "id": "q1",
        "domain": "math_reasoning",
        "question": (
            "A store reduces its prices by 20%, then later increases the reduced price by 25%. "
            "Is the final price higher, lower, or the same as the original? By what percentage?"
        ),
    },
    {
        "id": "q2",
        "domain": "logical_reasoning",
        "question": (
            "All mammals are warm-blooded. Whales are mammals. Dolphins are warm-blooded. "
            "Does it follow that dolphins are mammals? Explain your reasoning."
        ),
    },
    {
        "id": "q3",
        "domain": "causal_reasoning",
        "question": (
            "A city installs more streetlights and notices crime drops in those areas. "
            "A reporter headlines: 'Streetlights reduce crime.' "
            "What are at least two alternative explanations the reporter is ignoring?"
        ),
    },
    {
        "id": "q4",
        "domain": "math_reasoning",
        "question": (
            "If you flip a fair coin 3 times, what is the probability of getting "
            "at least 2 heads? Show your reasoning."
        ),
    },
    {
        "id": "q5",
        "domain": "commonsense_reasoning",
        "question": (
            "You have a 3-liter jug and a 5-liter jug and unlimited water. "
            "How do you measure exactly 4 liters? Give step-by-step instructions."
        ),
    },
]

MODELS_TO_EVALUATE = [
    "gpt-3.5-turbo",
    "gpt-4o-mini",
]


def get_model_response(model: str, question: str) -> str:
    """Get a plain response from the model being evaluated."""
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer the question clearly and show your reasoning."
            },
            {"role": "user", "content": question}
        ],
        temperature=0.7,
        max_tokens=500,
    )
    return completion.choices[0].message.content


def run_pipeline(verbose: bool = False) -> list[dict]:
    """
    Full pipeline:
    1. For each question, get responses from all models under evaluation
    2. Judge each response with our multi-layered rubric
    3. Return all results
    """
    results = []

    for q in EVAL_QUESTIONS:
        print(f"\n{'='*60}")
        print(f"Question [{q['id']}] ({q['domain']}): {q['question'][:80]}...")
        print('='*60)

        for model in MODELS_TO_EVALUATE:
            print(f"\n  📤 Getting response from {model}...")
            try:
                response = get_model_response(model, q["question"])
            except Exception as e:
                print(f"  ❌ Failed to get response from {model}: {e}")
                continue

            if verbose:
                print(f"\n  --- {model} Response ---\n  {response[:300]}...")

            print(f"  ⚖️  Judging {model} response...")
            scores = judge_response(
                question=q["question"],
                response=response,
                verbose=verbose
            )

            if scores:
                row = {
                    "question_id": q["id"],
                    "domain": q["domain"],
                    "question": q["question"],
                    "model": model,
                    "response": response,
                    "accuracy": scores.get("accuracy", {}).get("score"),
                    "reasoning_quality": scores.get("reasoning_quality", {}).get("score"),
                    "completeness": scores.get("completeness", {}).get("score"),
                    "conciseness": scores.get("conciseness", {}).get("score"),
                    "overall": scores.get("overall"),
                    "accuracy_reason": scores.get("accuracy", {}).get("reason"),
                    "reasoning_reason": scores.get("reasoning_quality", {}).get("reason"),
                    "completeness_reason": scores.get("completeness", {}).get("reason"),
                    "conciseness_reason": scores.get("conciseness", {}).get("reason"),
                }
                results.append(row)
                print(
                    f"  ✅ Scores — accuracy:{row['accuracy']} | "
                    f"reasoning:{row['reasoning_quality']} | "
                    f"completeness:{row['completeness']} | "
                    f"conciseness:{row['conciseness']} | "
                    f"overall:{row['overall']}"
                )
            time.sleep(0.5)  # rate limit buffer

    return results


def save_results(results: list[dict], output_path: str = "results.csv"):
    """Save results to CSV."""
    if not results:
        print("No results to save.")
        return

    fieldnames = list(results[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"\n💾 Results saved to {output_path}")


def print_summary(results: list[dict]):
    """Print a model comparison summary."""
    if not results:
        return

    print("\n" + "="*60)
    print("📊 SUMMARY — Average Scores by Model")
    print("="*60)

    from collections import defaultdict
    model_scores = defaultdict(lambda: defaultdict(list))
    dims = ["accuracy", "reasoning_quality", "completeness", "conciseness", "overall"]

    for row in results:
        for dim in dims:
            if row.get(dim) is not None:
                model_scores[row["model"]][dim].append(float(row[dim]))

    print(f"\n{'Dimension':<22} " + "  ".join(f"{m:<18}" for m in MODELS_TO_EVALUATE))
    print("-" * (22 + 22 * len(MODELS_TO_EVALUATE)))

    for dim in dims:
        row_str = f"{dim:<22} "
        for model in MODELS_TO_EVALUATE:
            vals = model_scores[model][dim]
            avg = sum(vals) / len(vals) if vals else 0
            row_str += f"{avg:<20.2f}"
        print(row_str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM-as-a-Judge Evaluation Pipeline")
    parser.add_argument("--verbose", action="store_true", help="Print judge reasoning")
    parser.add_argument("--output", default="results.csv", help="Output CSV path")
    args = parser.parse_args()

    print("🏗️  LLM-as-a-Judge Evaluation Pipeline")
    print(f"   Judge model:      {' gpt-4o-mini'}")
    print(f"   Models evaluated: {', '.join(MODELS_TO_EVALUATE)}")
    print(f"   Questions:        {len(EVAL_QUESTIONS)}")
    print(f"   Total judgments:  {len(EVAL_QUESTIONS) * len(MODELS_TO_EVALUATE)}")

    results = run_pipeline(verbose=args.verbose)
    save_results(results, args.output)
    print_summary(results)
