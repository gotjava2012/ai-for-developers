# Module 2 — How ML Actually Works

> **Goal:** Make the "learned function" from Module 1 fully concrete. You'll
> understand the optimization loop at the level of *what is actually computed*,
> why it generalizes (or doesn't), and then watch θ converge by running real
> code. This grounds fine-tuning, hallucination, and evaluation later — none of
> which are black boxes once this is solid.

---

## 2.1 Training as optimization

Training is numerical optimization of a scalar objective over parameters:

```
minimize over θ:   L(θ) = (1/N) Σ loss( f(xᵢ; θ), yᵢ )   +  regularization
```

- **f(x; θ)** — the model (Module 1).
- **loss** — a per-example penalty (cross-entropy for classification, MSE for
  regression). Choice of loss defines what "wrong" means.
- **L(θ)** — the empirical risk: average loss over the training set.
- You are doing high-dimensional minimization of a **non-convex** surface. There
  is no closed-form solution and no guarantee of a global minimum — you use
  iterative, gradient-based methods and accept good local minima.

---

## 2.2 Gradient descent, at the level of what's computed

The gradient ∇L(θ) is the vector of partial derivatives — for each parameter,
how L changes if you nudge that parameter. The update:

```
θ ← θ − η · ∇L(θ)
```

η is the **learning rate**. That's the whole algorithm; the engineering is in
the variants:

- **Batch vs. stochastic vs. mini-batch** — computing ∇L over all N each step is
  expensive and smooth; over one example is cheap and noisy; **mini-batch**
  (32–1024) is the standard compromise and the noise actually *helps* escape bad
  minima.
- **Momentum / Adam** — plain SGD is slow and sensitive. Modern optimizers
  (Adam/AdamW) keep running estimates of the gradient's mean and variance to
  adapt per-parameter step sizes. This is why Adam "just works" where raw SGD
  stalls — and why it costs extra memory (optimizer state ≈ 2× params, the
  reason training memory ≫ inference memory from Module 1).
- **Learning-rate schedules** — warmup then decay; η is the single most impactful
  hyperparameter. Too high → divergence; too low → crawl or stall in a poor
  minimum.

---

## 2.3 Backpropagation — the chain rule as a systems technique

You never compute ∇L by hand. **Backprop** computes it exactly and efficiently
by applying the chain rule backward through the computation graph:

1. **Forward pass** — compute f(x; θ) and the loss, caching intermediate
   activations.
2. **Backward pass** — propagate ∂L/∂(output) back through each operation,
   multiplying local Jacobians, to get ∂L/∂θ for every parameter in roughly the
   same cost as the forward pass.

Modern frameworks (PyTorch, JAX) do this via **autograd**: you define only the
forward computation; the framework records the graph and differentiates it. The
from-scratch lab implements backprop manually once so autograd is never magic
to you again. For a concrete payoff: softmax + cross-entropy has the clean
gradient `∂L/∂logits = (softmax(logits) − onehot(y))`, which you'll see in the
code.

---

## 2.4 Generalization — the actual goal, and why it's not training loss

Minimizing training loss is a *proxy*. The real objective is low error on unseen
data (**generalization**). The gap between them is where ML engineering lives.

- **Capacity vs. fit.** A model with enough parameters can memorize the training
  set (drive training loss to ~0) while learning nothing transferable —
  **overfitting**. Too little capacity → **underfitting** (can't even fit the
  signal). You're navigating the **bias–variance tradeoff**.
- **The protocol:** split data into **train / validation / test**. Train on
  train; tune hyperparameters against validation; report once on test. The test
  set is touched *last* and *rarely* — every time you make a decision from it,
  it leaks and stops being an honest estimate.
- **Regularization** — techniques that trade a little training fit for better
  generalization: L2 weight decay, dropout, early stopping, data augmentation.
- **Cross-validation** — k-fold averaging for a lower-variance estimate when data
  is scarce.

> Any accuracy number is meaningless without the question "on which split, and
> how many times did you look at it?" This is the single most common way ML
> results mislead.

---

## 2.5 How this scales to LLMs (so later modules connect)

Same machinery, different framing:

- **Objective:** self-supervised next-token prediction — the "label" is just the
  next token in the corpus, so no manual labeling is needed, which is what
  unlocked internet-scale training.
- **Then alignment:** supervised fine-tuning on curated instruction/response
  pairs, followed by preference optimization (RLHF / DPO) to make outputs
  helpful and safe. Still gradient descent on a loss — just a different objective
  on different data.
- **Generalization at scale** shows up as **emergent capability** and, on the
  failure side, as memorization of training data and sensitivity to distribution
  shift. The train/test discipline you learn here is the same discipline behind
  LLM **evals** (Module 6).

---

## Terms, at working precision
- **Empirical risk L(θ)** — mean loss over training data; what you minimize.
- **Non-convex optimization** — no global-minimum guarantee; you accept good local minima.
- **Mini-batch SGD** — gradient estimated on a small batch; noise aids optimization.
- **Adam/AdamW** — adaptive optimizer with per-parameter step sizes; extra memory for state.
- **Backprop / autograd** — reverse-mode differentiation of the computation graph.
- **Bias–variance / over- vs under-fitting** — the capacity-vs-generalization tradeoff.
- **Train/val/test** — fit / tune / report-once; the integrity protocol.

## Check yourself
1. Why is mini-batch SGD preferred over full-batch, beyond just cost?
2. What does Adam track that plain SGD doesn't, and what does that cost you?
3. In one line, what does backprop compute and at what cost relative to the forward pass?
4. Distinguish the roles of the validation set and the test set. Why does repeatedly consulting the test set invalidate it?
5. LLM pretraining uses "no labels." In what sense is that true, and in what sense is it still supervised next-token prediction?

➡️ **Lab:** run a from-scratch network and watch L(θ) fall as θ converges; prove
the non-linearity claim empirically; then run a real train/val/test pipeline and
read precision/recall/confusion-matrix — not just accuracy.
