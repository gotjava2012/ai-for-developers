---
marp: true
theme: default
paginate: true
header: "AI for Developers · Module 2 — How ML Actually Works"
---

# Module 2 — How ML Actually Works
### The learned function, made concrete

Training as optimization — at the level of what's actually computed.

---

## Training = optimization

```
minimize over θ:  L(θ) = (1/N) Σ loss(f(xᵢ;θ), yᵢ) + regularization
```

- **loss** defines what "wrong" means (cross-entropy, MSE)
- **L(θ)** = empirical risk = mean training loss
- High-dimensional, **non-convex** → no closed form, no global-min guarantee
- → iterative gradient methods, accept good local minima

---

## Gradient descent, concretely

```
θ ← θ − η · ∇L(θ)
```

∇L = for each parameter, how L moves if you nudge it. η = learning rate.

- **Mini-batch** (32–1024): cheaper than full-batch; its **noise helps** escape bad minima
- **Adam/AdamW**: per-parameter adaptive steps (tracks grad mean+variance)
  → "just works"; costs ~2× params in optimizer state (why train memory ≫ inference)
- **LR schedule** (warmup→decay): the highest-impact hyperparameter

---

## Backprop = chain rule, systematized

- **Forward:** compute f(x;θ) + loss, cache activations
- **Backward:** propagate ∂L/∂output back through the graph, multiply local
  Jacobians → ∂L/∂θ for every parameter, ≈ cost of one forward pass

Frameworks do this via **autograd** — you write only the forward pass.
(Lab implements it by hand once, so autograd is never magic.)

Clean result you'll see: `∂L/∂logits = softmax(logits) − onehot(y)`

---

## Generalization is the real goal

Training loss is a **proxy**. You want low error on **unseen** data.

- Enough capacity → can **memorize** (train loss ~0, learns nothing) = **overfit**
- Too little → **underfit**. You navigate the **bias–variance tradeoff**
- **Regularization** trades train-fit for generalization: weight decay, dropout,
  early stopping, augmentation

---

## The integrity protocol: train / val / test

- **train** — fit θ
- **validation** — tune hyperparameters
- **test** — touched **last and rarely**; report once

> Consult the test set repeatedly → it leaks → it's no longer an honest estimate.

Any accuracy number without "which split, how many looks?" is meaningless.

---

## How this scales to LLMs

- **Pretraining:** self-supervised next-token prediction (label = next token → no
  manual labeling → internet scale)
- **Alignment:** SFT on instruction/response, then preference optimization (RLHF/DPO)
- Still gradient descent on a loss — different objective, different data
- Train/test discipline here = **LLM evals** later (Module 6)

---

## Next

**Lab:**
1. Run a from-scratch net → watch L(θ) fall as θ converges
2. Kill the non-linearity → accuracy collapses (empirical proof)
3. Run a real train/val/test pipeline → read precision/recall/confusion matrix

**Module 3:** LLMs — tokenization, attention cost, sampling, and prompting as
context engineering.
