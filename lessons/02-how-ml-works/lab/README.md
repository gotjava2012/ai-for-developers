# Module 2 Lab — Watch a Model Learn (hands-on)

You'll run two real projects and *see* the concepts from the guide happen live:
the training loop, falling loss, why non-linearity matters, and train/test honesty.

Two ways to get the code:
```bash
# clone the companion repos (or use your local copies)
git clone https://github.com/gotjava2012/neural-net-from-scratch.git
git clone https://github.com/gotjava2012/ml-training-pipeline.git
```

---

## Part A — Watch a neural network learn (the training loop, live)

```bash
cd neural-net-from-scratch
pip3 install numpy
python3 src/neural_net.py
```

**What to watch:** every 100 epochs it prints loss and accuracy. You are
watching the training loop from the guide: loss **falls** (1.09 → ~0.07) while
accuracy **rises** (~64% → ~99%). That falling number *is* learning.

Map it to the guide:
- Each printed line = progress after more passes (**epochs**)
- The dropping **loss** = gradient descent working
- Rising **accuracy** = the model fitting the spiral data

---

## Part B — Prove why non-linearity matters (one-line experiment)

Open `src/neural_net.py`. Find the `relu` function:
```python
def relu(x):
    return np.maximum(0, x)
```
Temporarily break the non-linearity by making it return its input unchanged:
```python
def relu(x):
    return x          # <-- linear: no non-linearity
```
Re-run `python3 src/neural_net.py`.

**What you'll see:** accuracy collapses toward ~50% (near guessing). You just
proved the guide's claim — without the non-linearity, the network can only draw
straight lines and *cannot* learn the spiral.

➡️ **Put the `relu` back** to `np.maximum(0, x)` when you're done.

---

## Part C — Train/test honesty (a real workflow)

```bash
cd ../ml-training-pipeline
pip3 install scikit-learn
python3 src/train.py train
```

**What to watch for in the output:**
- **Cross-validation accuracy** (on training folds)
- **Held-out TEST accuracy** — the honest number
- A **classification report** and **confusion matrix** (accuracy isn't the whole story)
- **Feature importances** (which inputs mattered)

Then make a prediction on new data:
```bash
python3 src/train.py predict 6.3 3.3 6.0 2.5
```
That's **inference** (Module 1) using the model you just **trained** (Module 2).

---

## Exercises
1. In Part A, change `epochs` or the learning rate `lr` in `neural_net.py`.
   What happens with `lr` very small (e.g. 0.01) vs. very large (e.g. 5.0)?
2. In Part C, change `test_size` from 0.25 to 0.5 — does less training data hurt
   the test accuracy?
3. Explain, in your own words, why the test accuracy is the number that matters.

## Takeaway
You've now *seen* the training loop reduce loss, *proven* why non-linearity is
essential, and *measured* the difference between training and test performance.
Every ML model — including the LLMs in the next module — is this, scaled up.

➡️ **Next:** Module 3 — LLMs for Developers. You'll make your first LLM call.
