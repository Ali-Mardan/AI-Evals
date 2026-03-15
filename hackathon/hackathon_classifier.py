"""
hackathon_classifier.py
=======================
Data4Good Competition — AI-Generated Educational Content Factuality Detection

Task: Classify each (question, context, answer) as:
  - factual       : answer is correct
  - contradiction : answer is incorrect / hallucinated
  - irrelevant    : answer has nothing to do with the question

Approach: Two-stage local pipeline (no API key required)
  Stage 1: Detect Irrelevant — cosine similarity between question and answer
           (irrelevant answers are off-topic, so semantically distant from Q)
  Stage 2: Detect Contradiction vs Factual — NLI model on (context, answer)
           (contradiction = context contradicts answer)

Models used (free, run locally via HuggingFace):
  - sentence-transformers/all-MiniLM-L6-v2  (fast cosine similarity)
  - cross-encoder/nli-deberta-v3-small       (NLI classifier)

Threshold calibration:
  - Thresholds are optimized on the train set to maximize macro F1
  - Equal-weight scoring (33.3% per class) → we optimize macro F1 not accuracy

Usage:
  python hackathon_classifier.py
"""

import json
import numpy as np
from pathlib import Path
from collections import Counter
from sklearn.metrics import classification_report, f1_score

# ── Config ───────────────────────────────────────────────────────────────────
TRAIN_PATH = "hackathon/train.json"
TEST_PATH  = "hackathon/test.json"
OUTPUT_PATH = "hackathon/predictions.json"
MAX_CONTEXT_CHARS = 512   # NLI models have token limits; truncate long contexts
BATCH_SIZE = 64

# ── Load Data ─────────────────────────────────────────────────────────────────
print("📂 Loading data...")
with open(TRAIN_PATH, encoding="utf-8") as f:
    train_data = json.load(f)
with open(TEST_PATH, encoding="utf-8") as f:
    test_data = json.load(f)

# Normalize labels to lowercase
for row in train_data:
    row["type"] = row["type"].lower().strip()

print(f"   Train: {len(train_data):,} rows | Test: {len(test_data):,} rows")
print(f"   Label distribution: {dict(Counter(r['type'] for r in train_data))}")


# ── Load Models ───────────────────────────────────────────────────────────────
print("\n🤖 Loading models (first run will download ~150MB)...")

from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
nli_pipe  = pipeline(
    "text-classification",
    model="cross-encoder/nli-deberta-v3-small",
    device=-1,  # CPU
    batch_size=BATCH_SIZE,
)
print("   ✅ Models loaded")


# ── Feature Extraction ────────────────────────────────────────────────────────
def get_qa_similarity(questions, answers):
    """Cosine similarity between question and answer embeddings."""
    print("   Computing Q-A cosine similarities...")
    q_embs = embedder.encode(questions, batch_size=BATCH_SIZE, show_progress_bar=True)
    a_embs = embedder.encode(answers,   batch_size=BATCH_SIZE, show_progress_bar=True)
    sims = [float(util.cos_sim(q, a)) for q, a in zip(q_embs, a_embs)]
    return np.array(sims)


def get_nli_scores(contexts, answers):
    """
    NLI entailment score: does the context ENTAIL (support) the answer?
    High entailment → Factual
    Contradiction label → Contradiction
    """
    print("   Running NLI on (context, answer) pairs...")
    pairs = [
        f"{ctx[:MAX_CONTEXT_CHARS]} [SEP] {ans}"
        for ctx, ans in zip(contexts, answers)
    ]
    results = nli_pipe(pairs, truncation=True, max_length=512)
    # Returns list of {"label": "ENTAILMENT"/"CONTRADICTION"/"NEUTRAL", "score": float}
    entailment_scores = []
    contradiction_scores = []
    for r in results:
        label = r["label"].upper()
        score = r["score"]
        if label == "ENTAILMENT":
            entailment_scores.append(score)
            contradiction_scores.append(1 - score)
        elif label == "CONTRADICTION":
            entailment_scores.append(1 - score)
            contradiction_scores.append(score)
        else:  # NEUTRAL
            entailment_scores.append(0.5)
            contradiction_scores.append(0.5)
    return np.array(entailment_scores), np.array(contradiction_scores)


# ── Two-Stage Classifier ──────────────────────────────────────────────────────
def classify(qa_sims, contradiction_scores, irr_threshold, contra_threshold):
    """
    Stage 1: if Q-A similarity < irr_threshold → Irrelevant
    Stage 2: else if contradiction_score > contra_threshold → Contradiction
    Stage 3: else → Factual
    """
    preds = []
    for sim, contra in zip(qa_sims, contradiction_scores):
        if sim < irr_threshold:
            preds.append("irrelevant")
        elif contra > contra_threshold:
            preds.append("contradiction")
        else:
            preds.append("factual")
    return preds


# ── Threshold Calibration on Train Set ────────────────────────────────────────
print("\n🔧 Extracting features from train set...")
train_questions = [r["question"] for r in train_data]
train_answers   = [r["answer"]   for r in train_data]
train_contexts  = [r["context"]  for r in train_data]
train_labels    = [r["type"]     for r in train_data]

train_qa_sims = get_qa_similarity(train_questions, train_answers)
train_ent, train_contra = get_nli_scores(train_contexts, train_answers)

print("\n🎯 Calibrating thresholds on train set...")
best_f1 = 0
best_irr_thr = 0.3
best_contra_thr = 0.5

# Grid search over thresholds
for irr_thr in np.arange(0.10, 0.65, 0.05):
    for contra_thr in np.arange(0.30, 0.85, 0.05):
        preds = classify(train_qa_sims, train_contra, irr_thr, contra_thr)
        f1 = f1_score(train_labels, preds, average="macro", zero_division=0)
        if f1 > best_f1:
            best_f1 = f1
            best_irr_thr = irr_thr
            best_contra_thr = contra_thr

print(f"   Best irr_threshold:    {best_irr_thr:.2f}")
print(f"   Best contra_threshold: {best_contra_thr:.2f}")
print(f"   Best macro F1 (train): {best_f1:.4f}")

# Full train classification report
train_preds = classify(train_qa_sims, train_contra, best_irr_thr, best_contra_thr)
print("\n📊 Train Classification Report:")
print(classification_report(train_labels, train_preds, digits=4))


# ── Predict on Test Set ───────────────────────────────────────────────────────
print("\n🔮 Predicting on test set...")
test_questions = [r["question"] for r in test_data]
test_answers   = [r["answer"]   for r in test_data]
test_contexts  = [r["context"]  for r in test_data]

test_qa_sims = get_qa_similarity(test_questions, test_answers)
test_ent, test_contra = get_nli_scores(test_contexts, test_answers)

test_preds = classify(test_qa_sims, test_contra, best_irr_thr, best_contra_thr)
pred_dist = Counter(test_preds)
print(f"   Prediction distribution: {dict(pred_dist)}")


# ── Write Output ──────────────────────────────────────────────────────────────
print(f"\n💾 Writing predictions to {OUTPUT_PATH}...")
output = []
for row, pred in zip(test_data, test_preds):
    output.append({
        "ID": row["ID"],
        "answer": row["answer"],
        "type": pred,
        "context": row["context"],
        "question": row["question"],
    })

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"   ✅ Saved {len(output)} predictions to {OUTPUT_PATH}")
print("\n🏁 Done!")
