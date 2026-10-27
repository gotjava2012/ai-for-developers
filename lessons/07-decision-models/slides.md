---
marp: true
theme: default
paginate: true
header: "AI for Developers · Module 7 — Decision Models: Trees & Ensembles"
---

# Module 7 — Decision Models
### Trees & Ensembles

The family that quietly wins most **tabular** problems.

---

## Why this module

- Deep learning → perception & language
- **Tabular / "predict a column"** → **gradient-boosted trees** are still SOTA
- Fraud, churn, pricing, ranking, risk: trees first, train in seconds on CPU

> "Decision model" is overloaded — this is the **ML** sense (predictive trees).
> §last slide maps the **decision-theory** sense (expected value, MDPs).

---

## A single decision tree

Learned hierarchy of **if/else splits on features**; route example → leaf → prediction.

**Learned greedily:** at each node pick the split that most **reduces impurity**
(Gini/entropy for classification, variance for regression); recurse until a stop rule.

- ✅ interpretable, no scaling needed, handles mixed types & interactions
- ❌ **high variance** — a deep tree memorizes the training set → overfits

---

## Ensembles: cancel the errors

### Bagging → Random Forest (attacks **variance**)
- many **deep** trees, each on a bootstrap sample + random feature subset
- average/vote → decorrelated trees → variance down, bias flat
- parallel, robust, few knobs, strong default

### Boosting → Gradient Boosting (attacks **bias**)
- **shallow** trees in **sequence**, each fits the prior ensemble's residuals
- shrinkage (learning rate); XGBoost / LightGBM / CatBoost
- best tabular accuracy — but sequential, tuning-sensitive, can overfit

---

## Bagging vs. Boosting

| | Random Forest | Gradient Boosting |
|---|---|---|
| trees | deep, independent, parallel | shallow, sequential, residual-fitting |
| attacks | **variance** | **bias** |
| tuning | forgiving | sensitive |
| result | robust baseline | best-in-class (if tuned) |

> RF for a fast robust baseline; GBM when you'll tune for max accuracy.

---

## Interpretability — a real edge

- **Feature importance** — impurity reduction per feature (biased to high-cardinality; a guide)
- **SHAP** — principled per-prediction attributions; the standard for high-stakes
- **Decision path** — literally print the if/else path for one prediction

> Often *why* trees are chosen over a slightly-more-accurate black box
> (credit, risk, health).

---

## Gotchas

- **Overfitting** — control depth/min-samples/#trees; early stopping (boosting)
- **Extrapolation** — can't predict beyond the training target range
- **Imbalance** — accuracy lies; use class weights, precision/recall/AUC
- **Leakage** — a feature smuggling the label → #1 "great in dev, broken live"
- importance ≠ causation

---

## Trees vs. nets vs. LLMs

| Data / need | Use |
|---|---|
| tabular "predict a column" | **gradient-boosted trees** |
| interpretability / regulation | **trees + SHAP** |
| images / audio / signals | **neural nets** |
| text, few labels | **LLMs** (prompt/RAG) |
| small data, CPU, fast | **trees** |

> They **compose**: LLM extracts features from text → tree makes the decision.

---

## The *other* "decision models" (don't conflate)

Decision theory / OR — **prescriptive**, not predictive:
- **Decision trees (OR)** — choices × probabilities × payoffs → max **expected value**
- **Decision matrices** — weighted multi-criteria scoring
- **MDPs** — states/actions/rewards → basis of **reinforcement learning**

> ML trees: "what will *happen*?"  ·  Decision theory: "what should I *do*?"

---

## Lab

Same dataset, three models:
1. single tree → watch it **overfit** (train≫test)
2. random forest → **variance** down
3. gradient boosting → **bias** down, best AUC
4. read feature importances + a decision path

**Course complete** — next steps in the README.
