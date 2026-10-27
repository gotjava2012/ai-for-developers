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

```svg
<svg viewBox="0 0 560 210" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <!-- loss bowl -->
  <path d="M40 40 Q280 260 520 40" fill="none" stroke="#1f2a44" stroke-width="3"/>
  <text x="280" y="30" text-anchor="middle" font-size="14" fill="#1f2a44">loss L(θ)</text>
  <!-- descending ball positions along the curve -->
  <circle cx="90"  cy="78"  r="9" fill="#f0a500"/>
  <circle cx="150" cy="128" r="9" fill="#f0a500" opacity=".8"/>
  <circle cx="210" cy="162" r="9" fill="#f0a500" opacity=".65"/>
  <circle cx="265" cy="178" r="9" fill="#f0a500" opacity=".5"/>
  <circle cx="280" cy="181" r="11" fill="#2a7d5f"/>
  <!-- step arrows -->
  <g stroke="#c0392b" stroke-width="2.5" fill="none" marker-end="url(#g1)">
    <path d="M99 84 L142 122"/><path d="M159 134 L202 157"/><path d="M219 166 L258 176"/>
  </g>
  <text x="185" y="120" font-size="12" fill="#c0392b">step = −η·∇L</text>
  <text x="300" y="186" font-size="13" fill="#2a7d5f" font-weight="bold">minimum</text>
  <text x="80" y="70" font-size="12" fill="#555">start (random θ)</text>
  <text x="280" y="205" text-anchor="middle" font-size="13" fill="#333">θ (parameters)</text>
  <defs><marker id="g1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#c0392b"/></marker></defs>
</svg>
```
<p class="diagram-caption">Gradient descent: step downhill against the gradient until loss bottoms out.</p>

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

```svg
<svg viewBox="0 0 560 130" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <rect x="30" y="40" width="330" height="50" rx="6" fill="#2a7d5f"/>
  <text x="195" y="70" text-anchor="middle" font-size="15" fill="#fff" font-weight="bold">TRAIN  (~70%)</text>
  <text x="195" y="110" text-anchor="middle" font-size="12" fill="#555">fit θ</text>
  <rect x="368" y="40" width="100" height="50" rx="6" fill="#f0a500"/>
  <text x="418" y="70" text-anchor="middle" font-size="14" fill="#fff" font-weight="bold">VAL</text>
  <text x="418" y="110" text-anchor="middle" font-size="12" fill="#555">tune</text>
  <rect x="476" y="40" width="84" height="50" rx="6" fill="#c0392b"/>
  <text x="518" y="70" text-anchor="middle" font-size="14" fill="#fff" font-weight="bold">TEST</text>
  <text x="518" y="110" text-anchor="middle" font-size="12" fill="#555">once</text>
  <text x="295" y="26" text-anchor="middle" font-size="13" fill="#333">one dataset, split — and kept separate</text>
</svg>
```
<p class="diagram-caption">Keep the splits separate: peek at test repeatedly and it stops being honest.</p>

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
