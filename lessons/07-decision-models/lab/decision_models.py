"""
Module 7 Lab — Decision Models: single tree vs. bagging vs. boosting.

Demonstrates, on the same dataset, the core lessons from the guide:
  - a single deep tree OVERFITS (train >> test)
  - a random forest (bagging) reduces variance -> better, robust test score
  - gradient boosting reduces bias -> typically the best test score
  - feature importances, and a single decision path you can read

Runs on CPU in seconds. scikit-learn only.
    pip3 install scikit-learn
    python3 decision_models.py
"""

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, roc_auc_score


def evaluate(name, model, Xtr, Xte, ytr, yte):
    model.fit(Xtr, ytr)
    tr = accuracy_score(ytr, model.predict(Xtr))
    te = accuracy_score(yte, model.predict(Xte))
    # AUC where we have probabilities (better than accuracy on many problems)
    try:
        auc = roc_auc_score(yte, model.predict_proba(Xte)[:, 1])
    except Exception:
        auc = float("nan")
    gap = tr - te
    print(f"  {name:28s} train={tr*100:5.1f}%  test={te*100:5.1f}%  "
          f"AUC={auc:.3f}  (train-test gap {gap*100:+.1f})")
    return model


def main():
    data = load_breast_cancer()
    X, y, feats = data.data, data.target, data.feature_names
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25,
                                          random_state=42, stratify=y)
    print(f"Dataset: {X.shape[0]} samples, {X.shape[1]} features, 2 classes "
          f"(train {len(ytr)} / test {len(yte)})\n")

    print("=== A single deep tree OVERFITS (memorizes train, worse on test) ===")
    deep_tree = evaluate("DecisionTree (unbounded)",
                         DecisionTreeClassifier(random_state=42),
                         Xtr, Xte, ytr, yte)
    print("  ^ note train ~100% but a larger train-test gap = high variance\n")

    print("=== A shallow tree underfits less dramatically (bias/variance knob) ===")
    evaluate("DecisionTree (max_depth=3)",
             DecisionTreeClassifier(max_depth=3, random_state=42),
             Xtr, Xte, ytr, yte)
    print()

    print("=== Bagging: Random Forest reduces VARIANCE (robust, less overfit) ===")
    rf = evaluate("RandomForest (200 trees)",
                  RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
                  Xtr, Xte, ytr, yte)
    print()

    print("=== Boosting: Gradient Boosting reduces BIAS (often best accuracy) ===")
    gb = evaluate("GradientBoosting (200)",
                  GradientBoostingClassifier(n_estimators=200, learning_rate=0.05,
                                             max_depth=3, random_state=42),
                  Xtr, Xte, ytr, yte)
    print()

    print("=== Interpretability: top feature importances (Random Forest) ===")
    importances = sorted(zip(feats, rf.feature_importances_),
                         key=lambda x: -x[1])[:8]
    for name, imp in importances:
        bar = "#" * int(imp * 100)
        print(f"  {name:24s} {imp:.3f} {bar}")
    print()

    print("=== Read a single decision path (shallow tree, human-readable) ===")
    small = DecisionTreeClassifier(max_depth=2, random_state=42).fit(Xtr, ytr)
    print(export_text(small, feature_names=list(feats), max_depth=2))

    print("TAKEAWAYS")
    print("  - single tree: high train acc, bigger gap  = overfitting (high variance)")
    print("  - random forest: smaller gap               = variance reduced by bagging")
    print("  - gradient boosting: strong test/AUC        = bias reduced by boosting")
    print("  - trees expose WHY (importances + readable paths) — a real advantage")


if __name__ == "__main__":
    main()
