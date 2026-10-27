# Module 7 Lab — Decision Models: single tree vs. bagging vs. boosting

See the whole module's argument happen on one dataset: a single tree **overfits**,
a random forest **reduces variance**, gradient boosting **reduces bias**, and
trees can tell you **why**. scikit-learn only, runs on CPU in seconds.

## Run it
```bash
pip3 install scikit-learn
python3 decision_models.py
```

Dataset: the classic `load_breast_cancer` set (569 samples, 30 numeric features,
2 classes) that ships with scikit-learn — nothing to download.

---

## What you'll see (and what it means)

### 1. A single deep tree overfits
```
DecisionTree (unbounded)     train=100.0%  test= 92.3%  AUC=0.923  (train-test gap +7.7)
```
Training accuracy is a perfect 100% but test accuracy is lower, and there's a
visible **train–test gap**. That gap *is* overfitting — the tree memorized the
training rows. This is the high-variance weakness from the guide, made concrete.

### 2. A shallow tree trades a little fit for stability
```
DecisionTree (max_depth=3)   train= ~96%   test= ~94%   ...
```
Capping depth is the simplest bias/variance knob: training accuracy drops but the
gap shrinks. You've traded a bit of flexibility for a more honest model.

### 3. Bagging — Random Forest reduces variance
```
RandomForest (200 trees)     train=100.0%  test= 95.8%  AUC=0.995  (gap smaller)
```
200 decorrelated trees, averaged. Test accuracy and AUC jump and the gap tightens
versus the single tree — **variance reduced by bagging**, with no increase in
bias. This is your robust, low-tuning baseline.

### 4. Boosting — Gradient Boosting reduces bias
```
GradientBoosting (200)       train=~99%    test= 95.8%  AUC=0.993
```
Shallow trees trained sequentially, each fixing the last ensemble's residuals.
Typically the strongest test score / AUC on tabular data — **bias reduced by
boosting**. (On this small, easy dataset RF and GB land very close; the gap
usually widens in GB's favor on harder, larger problems.)

### 5. Interpretability — feature importances
```
worst perimeter          0.17 #################
worst concave points     0.15 ###############
...
```
Which features the forest actually leaned on. Useful as a guide — but it's
*associational, not causal*, and biased toward high-cardinality features. Treat
it as a hint, not a fact.

### 6. A single, readable decision path
```
|--- worst concave points <= 0.14
|   |--- worst area <= 957.45
|   |   |--- class: 1
...
```
The literal if/else path a shallow tree uses. This is the "why" neural nets can't
hand you — and the reason trees win in regulated, high-stakes decisions.

---

## Exercises
1. **Make overfitting worse, then fix it.** Re-run the unbounded tree a few times
   with different `random_state` values and watch the test score jump around
   (high variance). Then set `max_depth=4, min_samples_leaf=5` and watch it
   stabilize.
2. **Tune the booster.** Change `learning_rate` to `0.2` and then `0.01` (keep
   `n_estimators=200`). Note how a too-high LR overfits and a too-low LR underfits
   — the core boosting tradeoff.
3. **Switch to a real gradient-boosting library.** `pip3 install xgboost`, swap in
   `XGBClassifier`, and compare test AUC. This is what you'd actually ship.
4. **Add SHAP (harder).** `pip3 install shap`, compute `shap_values` for the random
   forest, and print the top contributors for one prediction. Compare SHAP's
   per-prediction story to the global feature importances.
5. **Regression variant.** Swap `load_breast_cancer` for `load_diabetes`, switch
   to the `*Regressor` classes and an error metric (MAE/RMSE), and confirm the
   same bagging-vs-boosting story holds for a numeric target.

---

## Takeaways
- A single tree: high train accuracy, bigger gap → **overfitting (high variance)**.
- Random forest: smaller gap → **variance reduced by bagging**.
- Gradient boosting: strong test/AUC → **bias reduced by boosting**.
- Trees expose **why** (importances, SHAP, readable paths) — a real, shippable
  advantage over black-box models.

## Tie it together
- For **tabular** problems, start here before any neural net (Module 2).
- Pair with an **LLM** (Modules 3–4) to turn messy text into features, then let a
  boosted tree make the decision.
- Wrap the output with **guardrails and evals** (Module 6) before anything acts on
  it.
