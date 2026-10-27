# Module 2 — How ML Actually Works

> **Goal:** Understand how a model *learns* — data, parameters, loss, and
> gradient descent — well enough to reason about any ML system. Then watch it
> happen live by running two real projects.

You won't train models from scratch often (Module 1), but understanding the
training loop makes every later topic — fine-tuning, why models hallucinate,
why evaluation matters — click into place.

---

## 2.1 The one-sentence version

> Machine learning = **adjust a model's numbers (parameters) over and over until
> its predictions stop being wrong.**

Everything else is detail. Let's unpack that detail.

---

## 2.2 The four ingredients

1. **Data** — examples of inputs and (usually) the correct outputs.
   - *Features (X)* — the inputs (e.g. flower measurements, pixel values).
   - *Labels (y)* — the correct answers (e.g. the flower species).
2. **Model** — a function with adjustable **parameters** that maps X → prediction.
3. **Loss function** — a number measuring how wrong the predictions are. Lower
   is better. Training's whole job is to make this number small.
4. **Optimizer** — the rule for nudging parameters to reduce the loss. The
   classic one is **gradient descent**.

---

## 2.3 The training loop (the heartbeat of all ML)

Every ML model — from a 2-parameter line to a billion-parameter LLM — learns
with the same loop:

```
repeat many times (each pass = one "epoch"):
    1. FORWARD:  run inputs through the model → predictions
    2. LOSS:     measure how wrong the predictions are
    3. BACKWARD: compute how each parameter contributed to the error (gradients)
    4. UPDATE:   nudge each parameter a little to reduce the loss
```

Do this thousands of times and the loss falls, the predictions improve — that's
**learning**. There is no magic step. It's this loop.

### Gradient descent, intuitively
Imagine standing on a foggy hill, wanting to reach the lowest point. You can't
see far, but you can feel which way is downhill under your feet, and you step
that way. Repeat. That's gradient descent: the **gradient** is "which way is
downhill for the loss," and the **learning rate** is how big a step you take.

- Learning rate too small → painfully slow.
- Learning rate too big → you overshoot and bounce around (or diverge).

---

## 2.4 Why non-linearity matters (the thing that makes deep learning work)

A model made only of straight-line math can only learn straight-line
relationships — stack a hundred linear layers and you still get a line. Real
data (images, language) is not linear.

The fix: put a **non-linear activation function** (like ReLU) between layers.
That's what lets a neural network bend and fold its decision boundaries to fit
complex patterns. You'll *prove* this in the lab: a network with the
non-linearity hits ~99% on a spiral dataset; remove it and it collapses to ~50%.

---

## 2.5 The most important discipline: train/test split

Here's where beginners get fooled. A model can memorize its training data and
score 100% on it — while being useless on anything new. That's **overfitting.**

So you **hold out** some data the model never sees during training, and measure
success on *that*:
- **Training set** — the model learns from this.
- **Test set** — you evaluate on this. This is the honest number.

> A model that scores 100% on training data and 60% on test data hasn't learned
> — it has memorized. The test score is the one that matters.

**Developer takeaway:** any time someone quotes an accuracy number, ask "on the
training set or a held-out set?" If they don't know, don't trust the number.

---

## 2.6 Kinds of ML (quick map)

- **Supervised** — learn from labeled examples (X → y). Most of what you'll
  meet: classification, regression. (The labs are supervised.)
- **Unsupervised** — find structure in unlabeled data (clustering, embeddings).
- **Reinforcement** — learn by trial, reward, and error (robotics, game-playing,
  and part of how modern LLMs are tuned).

LLMs are trained with a flavor of supervised learning ("predict the next token")
plus reinforcement from human feedback — but it's the *same loop* at enormous
scale.

---

## Key terms
- **Features (X) / labels (y)** — inputs and correct answers.
- **Epoch** — one full pass over the training data.
- **Loss** — how wrong the model is (training minimizes this).
- **Gradient descent** — nudge parameters downhill on the loss.
- **Learning rate** — step size of each nudge.
- **Overfitting** — memorizing training data, failing on new data.
- **Train/test split** — hold out data to measure honestly.

## Check yourself
1. What are the four steps of the training loop?
2. What does the loss function measure, and does training push it up or down?
3. Why can't a purely linear model learn complex patterns?
4. A model scores 99% on training data and 61% on test data. What's happening?

➡️ **Do the `lab/`** — you'll run a neural network from scratch and watch loss
fall live, then run a real scikit-learn pipeline and see train vs. test honesty.
