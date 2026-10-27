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

```svg
<svg viewBox="0 0 520 190" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <!-- nodes -->
  <g>
    <rect x="200" y="20" width="120" height="34" rx="6" fill="#1f2a44"/><text x="260" y="42" text-anchor="middle" font-size="12" fill="#fff">worst area ≤ 880?</text>
    <rect x="80"  y="80" width="120" height="34" rx="6" fill="#3a5c99"/><text x="140" y="102" text-anchor="middle" font-size="12" fill="#fff">concave ≤ .14?</text>
    <rect x="320" y="80" width="120" height="34" rx="6" fill="#3a5c99"/><text x="380" y="102" text-anchor="middle" font-size="11" fill="#fff">texture ≤ .47?</text>
    <rect x="30"  y="142" width="80" height="30" rx="6" fill="#2a7d5f"/><text x="70" y="162" text-anchor="middle" font-size="12" fill="#fff">benign</text>
    <rect x="150" y="142" width="80" height="30" rx="6" fill="#c0392b"/><text x="190" y="162" text-anchor="middle" font-size="12" fill="#fff">malignant</text>
    <rect x="300" y="142" width="80" height="30" rx="6" fill="#2a7d5f"/><text x="340" y="162" text-anchor="middle" font-size="12" fill="#fff">benign</text>
    <rect x="400" y="142" width="80" height="30" rx="6" fill="#c0392b"/><text x="440" y="162" text-anchor="middle" font-size="12" fill="#fff">malignant</text>
  </g>
  <g stroke="#888" stroke-width="2">
    <line x1="235" y1="54" x2="150" y2="80"/><line x1="285" y1="54" x2="370" y2="80"/>
    <line x1="120" y1="114" x2="80" y2="142"/><line x1="160" y1="114" x2="190" y2="142"/>
    <line x1="360" y1="114" x2="340" y2="142"/><line x1="400" y1="114" x2="440" y2="142"/>
  </g>
  <text x="165" y="64" font-size="11" fill="#2a7d5f" font-weight="bold">yes</text><text x="358" y="64" font-size="11" fill="#c0392b" font-weight="bold">no</text>
</svg>
```
<p class="diagram-caption">A tree routes each example through if/else splits down to a leaf prediction — fully readable.</p>

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

```svg
<svg viewBox="0 0 600 190" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <!-- Bagging: parallel trees -->
  <text x="150" y="20" text-anchor="middle" font-size="14" font-weight="bold" fill="#2a7d5f">Bagging (Random Forest)</text>
  <g fill="#2a7d5f">
    <polygon points="40,45 25,80 55,80"/><polygon points="100,45 85,80 115,80"/><polygon points="160,45 145,80 175,80"/><polygon points="220,45 205,80 235,80"/>
  </g>
  <text x="20" y="98" text-anchor="start" font-size="16" fill="#888">⋯</text>
  <text x="255" y="70" text-anchor="end" font-size="11" fill="#333" font-style="italic">independent, parallel</text>
  <rect x="70" y="125" width="120" height="30" rx="6" fill="#2a7d5f"/><text x="130" y="145" text-anchor="middle" font-size="12" fill="#fff">average / vote</text>
  <g stroke="#2a7d5f" stroke-width="1.5"><line x1="40" y1="80" x2="110" y2="125"/><line x1="100" y1="80" x2="120" y2="125"/><line x1="160" y1="80" x2="145" y2="125"/><line x1="220" y1="80" x2="160" y2="125"/></g>
  <text x="130" y="173" text-anchor="middle" font-size="11" fill="#2a7d5f" font-weight="bold">↓ variance</text>
  <!-- divider -->
  <line x1="300" y1="30" x2="300" y2="175" stroke="#ccc" stroke-width="1"/>
  <!-- Boosting: sequential -->
  <text x="450" y="20" text-anchor="middle" font-size="14" font-weight="bold" fill="#c0392b">Boosting (Gradient Boosting)</text>
  <g fill="#c0392b">
    <polygon points="350,55 338,80 362,80"/><polygon points="420,55 408,80 432,80"/><polygon points="490,55 478,80 502,80"/><polygon points="560,55 548,80 572,80"/>
  </g>
  <g stroke="#c0392b" stroke-width="2" fill="none" marker-end="url(#b1)">
    <path d="M362 68 H408"/><path d="M432 68 H478"/><path d="M502 68 H548"/>
  </g>
  <g font-size="10" fill="#555" text-anchor="middle"><text x="385" y="100">fix</text><text x="455" y="100">fix</text><text x="525" y="100">fix</text></g>
  <text x="455" y="130" text-anchor="middle" font-size="12" fill="#333">each tree fixes prior errors</text>
  <text x="455" y="150" text-anchor="middle" font-size="11" fill="#c0392b">↓ bias</text>
  <defs><marker id="b1" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#c0392b"/></marker></defs>
</svg>
```
<p class="diagram-caption">Bagging averages many independent trees (↓variance); boosting chains trees that fix each other (↓bias).</p>

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
