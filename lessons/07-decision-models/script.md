# Module 7 — Decision Models: Trees & Ensembles · Script

*Runtime: ~9–11 min. [brackets] map to slides.md.*

---

[Slide: title]

Everyone's attention is on neural nets and LLMs, so here's something that might
surprise you: for the rows-and-columns data that runs most businesses —
transactions, customers, prices, risk scores — the models that win are usually
not deep learning. They're decision trees and their ensembles. Fraud scoring,
churn, pricing, ranking, credit risk: reach for gradient-boosted trees first,
and they'll often beat a neural net while training in seconds on a laptop CPU.
In this module you'll learn how a tree actually decides, why one tree is weak but
many trees are strong, the difference between bagging and boosting, and when to
pick this family over a neural net or an LLM. Then you'll train and interpret one.

One terminology note up front, because "decision model" is overloaded. We're
doing the machine-learning sense — tree-based predictive models. There's a second
sense from decision theory — expected-value trees and Markov decision processes —
and I'll draw that line clearly near the end so you never conflate the two.

---

[Slide: how a tree decides]

Start with a single decision tree. It's a learned hierarchy of if/else splits on
your features. To make a prediction you drop an example in at the root and route
it down — "is this feature above this threshold? go left, else right" — until it
lands in a leaf, and the leaf holds the answer, a class or a number.

How does it learn where to split? Greedily. At each node it looks at candidate
splits — a feature and a threshold — and picks the one that most reduces
*impurity* in the two children it creates. For classification, impurity is Gini
or entropy: a measure of how mixed the labels are. For regression, it's variance
or mean-squared-error reduction. Then it recurses on each child, and keeps going
until a stopping rule kicks in — max depth, minimum samples in a leaf, or no
split that helps anymore.

Two properties make trees genuinely pleasant to work with. They're interpretable
— you can read the exact path a prediction took. And they need no feature
scaling, because splits are just thresholds; multiply a feature by a thousand and
the tree is unchanged. They also handle mixed data types and non-linear
interactions natively.

---

[Slide: the one weakness]

But a single deep tree has one serious weakness, and it's the whole reason the
rest of this module exists: high variance. Left to grow fully, a tree will
memorize the training set — drive training accuracy to basically a hundred
percent — and then change dramatically if you perturb the data even slightly.
That's overfitting, the bias–variance tradeoff from Module 2 made concrete. A
model that nails the training data and stumbles on new data has learned noise,
not signal. So the question becomes: how do we keep the flexibility of trees but
kill the variance? The answer is ensembles.

---

[Slide: bagging → random forests]

The first strategy is bagging, and it gives you the random forest. The idea:
instead of one tree, train *many* deep trees, but inject randomness so they don't
all make the same mistakes. Each tree trains on a bootstrap sample — a random
resample of the rows — and at each split it only gets to consider a random subset
of the features. Then you predict by averaging for regression or voting for
classification.

Here's the intuition for why it works. Those deep trees are individually
high-variance, but the randomness makes their errors *decorrelated*. When you
average a bunch of noisy, decorrelated estimators, the noise cancels — variance
drops — and because each tree was still low-bias, you don't pay for it in bias.
That's the free lunch: a forest generalizes exactly where a single tree overfit.
And it's forgiving — trees are independent so training parallelizes, there are
few knobs to get wrong, and you get feature importance and an out-of-bag
validation estimate for free. Random forest is your strong, low-effort baseline.

---

[Slide: boosting → gradient boosting]

The second strategy is boosting, and it attacks the opposite problem. Where
bagging reduces variance by averaging independent deep trees, boosting reduces
*bias* by building shallow trees *sequentially*, each one correcting the previous
ensemble's mistakes. Concretely: fit a weak shallow tree, look at where it's
wrong — the residual errors — and train the next tree to predict those residuals.
Add it in, scaled down by a learning rate, and repeat. Mathematically that's
gradient descent in function space on your loss function, which is where the name
gradient boosting comes from.

This produces the highest accuracy you'll typically get on tabular data. The cost
is that it's sequential, so slower to train, and it's sensitive — the learning
rate, tree depth, number of trees, and regularization all matter, and if you
boost too long it *will* overfit. So you tune, and you use early stopping on a
validation set. In practice you won't hand-roll this; you'll use XGBoost,
LightGBM, or CatBoost. They add regularization, histogram-based splitting that's
fast on big data, and graceful categorical handling — LightGBM for speed at
scale, CatBoost when you have lots of categorical features.

So the rule of thumb: random forest when you want a robust baseline with almost
no tuning; gradient boosting when you want maximum accuracy and you're willing to
invest in tuning and early stopping.

---

[Slide: interpretability]

Now the reason trees often win even when a black box is a hair more accurate:
they tell you *why*. Three levels. Feature importance ranks how much each feature
reduced impurity across the ensemble — useful as a guide, though it's biased
toward high-cardinality features, so don't over-read it. SHAP values are the
rigorous version — per-prediction feature attributions with real theoretical
backing — and for anything you have to justify, like credit or health or risk,
SHAP is the standard. And at the simplest level, you can print the actual if/else
decision path for a single prediction and hand it to a human. For regulated,
high-stakes decisions, that explainability is frequently the deciding factor over
a neural net.

---

[Slide: gotchas]

A few failure modes to keep in your head. Overfitting — from a single unbounded
tree or an over-boosted ensemble — controlled with depth limits, min-samples, and
early stopping. Extrapolation — trees literally cannot predict outside the range
of target values they saw, because a leaf can only output values it observed, so
they're bad for trending beyond your data. Imbalanced classes — accuracy lies, so
use class weights and look at precision, recall, and AUC. Leakage — a feature
that secretly encodes the label will make your offline numbers look fantastic and
then collapse in production; it's the number one cause of "great in dev, broken
live." And remember importance is association, not causation — don't tell a
stakeholder a feature *causes* the outcome just because the model leaned on it.

---

[Slide: when to use what]

Zooming out — when do you reach for this family versus the others? Tabular data,
predicting a column: gradient-boosted trees, first choice. Need interpretability
or a regulatory justification: trees plus SHAP. Images, audio, raw signals:
neural nets. Text understanding or generation with few labels: an LLM, with
prompting or RAG from Modules 3 and 4. Small or medium data, CPU-only, fast
iteration: trees, again. And an increasingly common pattern in the AI era — they
*compose*: use an LLM to extract clean structured features out of messy text,
then feed those into a gradient-boosted tree that makes the actual decision.
Don't default to the fanciest model; default to the one that fits the data and
the constraints.

---

[Slide: the other "decision models"]

Quick disambiguation so you're never caught out in a meeting. "Decision models"
also names a body of work in decision theory and operations research, and it's
*prescriptive*, not predictive. Decision trees in that world enumerate your
choices and uncertain outcomes with probabilities and payoffs, and you pick the
branch with the best expected value. Decision matrices score options against
weighted criteria. And Markov decision processes — states, actions, rewards,
transitions — are the formal foundation of reinforcement learning. Those answer
"what should I *do* under uncertainty?" The ML trees in this module answer "what
will *happen*?" You often combine them — predict with ML, decide with decision
theory — but they are not the same thing.

---

[Slide: lab]

To the lab. On one dataset you'll train a single unbounded tree and watch it hit
near-perfect training accuracy with a visible train-test gap — overfitting you
can see. Then a random forest, and you'll watch that gap shrink as bagging kills
the variance. Then a gradient-boosted model, usually the best test score and AUC,
bias reduced by boosting. Finally you'll print the forest's feature importances
and read a single human-readable decision path — because a model that can tell
you *why* is a model you can actually ship into a decision that matters. That's
the module. You now know the family that quietly runs most of applied machine
learning.
