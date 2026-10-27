---
marp: true
theme: default
paginate: true
header: "AI for Developers · Module 2 — How ML Actually Works"
---

# Module 2
## How ML Actually Works

The training loop — and watching a model learn, live.

---

## The one-sentence version

> ML = **adjust a model's parameters over and over until its predictions
> stop being wrong.**

Everything else is detail.

---

## Four ingredients

1. **Data** — inputs (features X) + correct answers (labels y)
2. **Model** — a function with adjustable **parameters**
3. **Loss** — a number: how wrong are we? (lower = better)
4. **Optimizer** — the rule that nudges parameters (gradient descent)

---

## The training loop (heartbeat of all ML)

```
repeat (each pass = one "epoch"):
   1. FORWARD   inputs → predictions
   2. LOSS      how wrong?
   3. BACKWARD  each parameter's share of the error (gradients)
   4. UPDATE    nudge parameters to reduce loss
```

Thousands of times → loss falls → that's **learning**.

---

## Gradient descent, intuitively

Foggy hill. Want the lowest point.
Feel which way is downhill → step → repeat.

- **Gradient** = which way is downhill for the loss
- **Learning rate** = how big a step
  - too small → slow
  - too big → overshoot / diverge

---

## Why non-linearity matters

Only straight-line math → can only learn straight lines.
(100 linear layers still = a line.)

Add a **non-linear activation** (ReLU) between layers → the network can bend to
fit complex patterns.

**You'll prove it:** spiral dataset →
with non-linearity ~99%, without it ~50%.

---

## The discipline that saves you: train/test split

- Model can **memorize** training data → 100% there, useless on new data
- That's **overfitting**
- So **hold out** a test set the model never sees → evaluate on *that*

> "99% on training, 61% on test" = memorized, not learned.
> The **test** score is the real one.

---

## Kinds of ML

- **Supervised** — labeled X → y (classification, regression) ← most common
- **Unsupervised** — find structure, no labels (clustering, embeddings)
- **Reinforcement** — learn by reward/trial

LLMs = "predict the next token" (supervised) + human-feedback tuning —
same loop, enormous scale.

---

## Lab

1. Run `neural-net-from-scratch` → watch loss fall, accuracy rise
2. Remove the non-linearity → watch it collapse to ~50%
3. Run `ml-training-pipeline` → see train vs. test honesty

**Next:** Module 3 — LLMs for Developers (your first LLM call)
