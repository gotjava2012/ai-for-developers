# Module 7 — Decision Models: Trees & Ensembles

> **Goal:** Understand the model family that quietly wins most *tabular* problems
> in industry — decision trees and their ensembles (random forests, gradient
> boosting). You'll learn how a tree actually decides, why single trees are weak
> and ensembles are strong, the bagging-vs-boosting distinction, and when to reach
> for these over a neural network. Then train and interpret one.
>
> Note on terminology: "decision model" is overloaded. This module covers the
> **ML** sense (tree-based predictive models). §7.7 briefly maps the
> **decision-theory** sense (expected-value trees, MDPs) so you can tell them
> apart.

---

## 7.1 Why this module exists

Deep learning dominates perception and language, but for **structured/tabular
data** — the rows-and-columns of most business systems — **gradient-boosted
trees (XGBoost, LightGBM, CatBoost) remain the state of the art**, routinely
beating neural nets while training in seconds on a CPU. If you're doing fraud
scoring, churn, pricing, ranking, risk, or most "predict a column" problems,
this is the family you reach for first. Knowing it is not optional for an applied
AI engineer.

---

## 7.2 A single decision tree — how it decides

A decision tree is a learned hierarchy of **if/else splits on features**. To
predict, you route an example from the root down to a leaf; the leaf holds the
prediction (a class or a value).

**How it's learned (greedy recursive partitioning):**
- At each node, consider candidate splits (feature, threshold).
- Pick the split that most **reduces impurity** in the resulting children.
  - Classification impurity: **Gini** or **entropy** (how mixed the labels are).
  - Regression: **variance / MSE** reduction.
- Recurse on each child until a stopping rule (max depth, min samples per leaf,
  no further impurity gain).

**Properties that matter to you:**
- **Interpretable** — you can read the decision path; "why" is inspectable.
- **No scaling needed** — splits are threshold-based, so feature scale/monotonic
  transforms don't matter (unlike neural nets / linear models).
- **Handles mixed types and non-linear interactions** natively.
- **But: high variance.** A single deep tree memorizes the training set —
  small data changes → very different tree. Left unchecked it **overfits**
  badly (Module 2's bias–variance tradeoff, concretely).

That last weakness is the whole motivation for ensembles.

---

## 7.3 Ensembles — turning weak trees into strong models

The core idea: **combine many trees so their errors cancel.** Two fundamentally
different strategies.

### Bagging → Random Forests (reduce variance)
- Train many **deep** (low-bias, high-variance) trees, each on a **bootstrap
  sample** of the data, and at each split consider only a **random subset of
  features**.
- Predict by **averaging** (regression) or **voting** (classification).
- The randomness **decorrelates** the trees; averaging decorrelated
  high-variance estimators drives variance down without raising bias. That's why
  a forest generalizes where one tree overfits.
- **Parallel** (trees are independent), robust, few knobs, a strong default.
- Bonus: **out-of-bag** samples give a built-in validation estimate; feature
  importance comes for free.

### Boosting → Gradient Boosting (reduce bias)
- Train trees **sequentially**, each **shallow** (weak, high-bias) tree fitting
  the **residual errors** of the current ensemble — i.e. gradient descent in
  function space on the loss.
- Add each tree scaled by a **learning rate** (shrinkage); more trees + smaller
  learning rate = better generalization, up to a point.
- Produces the **highest accuracy** on tabular data, but is **sequential**,
  **sensitive to hyperparameters**, and **can overfit** if over-trained → needs
  early stopping and tuning.
- Modern implementations — **XGBoost, LightGBM, CatBoost** — add regularization,
  smart histogram-based splitting, and categorical handling; LightGBM is fast on
  large data, CatBoost handles categoricals gracefully.

| | Random Forest (bagging) | Gradient Boosting |
|---|---|---|
| Trees | deep, independent, parallel | shallow, sequential, each fixes prior errors |
| Attacks | **variance** | **bias** |
| Tuning | forgiving | sensitive (LR, depth, #trees, regularization) |
| Speed | parallel, fast to train | sequential; fast libs mitigate |
| Typical result | strong, robust baseline | best-in-class accuracy (if tuned) |

**Rule of thumb:** random forest for a fast, robust baseline with minimal tuning;
gradient boosting (XGBoost/LightGBM) when you want to squeeze out maximum
accuracy and will invest in tuning + early stopping.

---

## 7.4 Interpretability — a real advantage

Unlike neural nets, tree models expose *why*:
- **Feature importance** — how much each feature reduced impurity across the
  ensemble (useful but biased toward high-cardinality features; treat as a guide).
- **SHAP values** — the rigorous, model-agnostic approach: per-prediction feature
  attributions with sound theoretical backing. For tabular decisions you must
  justify (credit, risk, health), SHAP is the standard.
- **Single-tree surrogate / decision path** — you can literally print the
  if/else path for an individual prediction.

For regulated or high-stakes decisions, this interpretability is often why trees
are chosen *over* a marginally more accurate black box.

---

## 7.5 Failure modes & gotchas
- **Overfitting with a single tree or over-boosted ensemble** — control depth,
  min-samples, #trees; use early stopping (boosting) and a validation set.
- **Extrapolation** — trees can't predict outside the range of training targets
  (leaves output seen values); bad for trends beyond observed data.
- **Imbalanced classes** — accuracy misleads; use class weights and
  precision/recall/AUC (Module 2 metrics).
- **Leakage** — a feature that encodes the label inflates offline scores and
  collapses in production; the usual #1 cause of "great in dev, broken live."
- **Importance misread as causation** — importance is associational, not causal.

---

## 7.6 When to use trees vs. neural nets vs. LLMs

| Situation | Reach for |
|---|---|
| Tabular/structured data, "predict a column" | **Gradient-boosted trees** (first choice) |
| Need interpretability / regulatory justification | **Trees + SHAP** |
| Images, audio, raw signals | **Neural nets (deep learning)** |
| Text understanding/generation, few labels | **LLMs** (prompt/RAG, Modules 3–4) |
| Small/medium data, fast iteration, CPU-only | **Trees** (train in seconds) |

Practical note for the AI era: trees and LLMs **compose** — e.g. use an LLM to
extract structured features from messy text, then a gradient-boosted tree to make
the actual decision. Don't default to the fanciest model; default to the one that
fits the data and the constraints.

---

## 7.7 "Decision models" in the other sense (so you can disambiguate)
The phrase also refers to **decision theory / operations research**, which is
*prescriptive*, not predictive:
- **Decision trees (OR)** — enumerate choices/outcomes with probabilities and
  payoffs; choose the branch maximizing **expected value**.
- **Decision matrices / multi-criteria analysis** — score options against
  weighted criteria.
- **Markov Decision Processes (MDPs)** — states, actions, rewards, transitions;
  the formal basis of **reinforcement learning**.

These answer "what should I *do*?" under uncertainty; the ML trees in this module
answer "what will *happen*?" They're often combined (predict with ML, decide with
decision theory), but don't conflate them.

---

## Terms, at working precision
- **Impurity (Gini/entropy/variance)** — the quantity a split reduces.
- **Bagging** — bootstrap + feature subsampling + averaging → variance reduction (random forest).
- **Boosting** — sequential residual-fitting with shrinkage → bias reduction (gradient boosting).
- **XGBoost/LightGBM/CatBoost** — production gradient-boosting libraries.
- **SHAP** — principled per-prediction feature attributions.
- **Leakage** — a feature that smuggles in the label; inflates offline metrics.
- **MDP** (decision-theory sense) — states/actions/rewards; basis of RL.

## Check yourself
1. Mechanically, how does a tree choose a split, and what does it minimize?
2. Why does a single deep tree overfit, and how does bagging fix it without adding bias?
3. Contrast what bagging and boosting each attack (variance vs. bias) and why that follows from deep-parallel vs. shallow-sequential trees.
4. For a credit-decision model you must explain to a regulator, what model + interpretability tool, and why over a neural net?
5. Distinguish the ML sense of "decision model" from the decision-theory sense in one sentence each.

➡️ **Lab:** train a single tree (watch it overfit), then a random forest and a
gradient-boosted model on the same data; compare test accuracy; read feature
importances; and inspect a single decision path.
