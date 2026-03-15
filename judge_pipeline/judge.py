"""
judge.py — Core LLM judge: formats prompt, calls gpt-4o-mini, parses structured output.

Design decisions:
- temperature=0 for deterministic, reproducible scoring
- response_format=json_object: guarantees valid JSON output (gpt-4o-mini supports this)
- Brace-balanced JSON extraction as fallback (handles nested objects correctly)
- Returns None on hard failure rather than crashing the pipeline
"""

import json
import os
import re
import time
from pathlib import Path
from openai import OpenAI
from rubric import build_judge_prompt

# ── API Key Loading ───────────────────────────────────────────────────────────
# Tries in order:
#  1. Environment variable (already set externally)
#  2. .env file in THIS script's directory (judge_pipeline/.env)
SCRIPT_DIR = Path(__file__).parent

if not os.environ.get("OPENAI_API_KEY"):
    env_path = SCRIPT_DIR / ".env"
    if env_path.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(dotenv_path=env_path)
        except ImportError:
            for line in env_path.read_text().splitlines():
                if line.startswith("OPENAI_API_KEY="):
                    os.environ["OPENAI_API_KEY"] = line.split("=", 1)[1].strip()

client = OpenAI()  # reads OPENAI_API_KEY from environment

JUDGE_MODEL = "gpt-4o-mini"
MAX_RETRIES = 2


def extract_json(text: str) -> dict | None:
    """
    Extract the outermost JSON object from the judge's response.
    Uses brace-counting to handle nested objects correctly.
    """
    # First try: direct parse (when JSON mode returns clean JSON)
    try:
        return json.loads(text.strip())
    except Exception:
        pass

    # Second try: find ```json ... ``` block
    match = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", text)
    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            pass

    # Third try: brace-balanced search for outermost {...}
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    for i, ch in enumerate(text[start:], start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start : i + 1])
                except Exception:
                    break
    return None


def judge_response(
    question: str,
    response: str,
    context: str = None,
    verbose: bool = False
) -> dict | None:
    """
    Call gpt-4o-mini as a judge to score a single response.

    Returns a dict with scores per dimension, or None on failure.
    """
    prompt = build_judge_prompt(question, response, context)

    for attempt in range(MAX_RETRIES + 1):
        try:
            completion = client.chat.completions.create(
                model=JUDGE_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert AI evaluator. Always respond with valid JSON only."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=900,
                response_format={"type": "json_object"},  # guarantees JSON output
            )
            raw_output = completion.choices[0].message.content

            if verbose:
                print(f"\n--- Judge Raw Output ---\n{raw_output}\n")

            scores = extract_json(raw_output)
            if scores:
                scores["raw_output"] = raw_output
                return scores
            else:
                print(f"  [Attempt {attempt+1}] JSON parse failed, retrying...")
                time.sleep(1)

        except Exception as e:
            print(f"  [Attempt {attempt+1}] API error: {e}")
            time.sleep(2)

    print(f"  ❌ Judge failed after {MAX_RETRIES+1} attempts")
    return None
