# Module 2 — How ML Actually Works · Script

*Runtime: ~9–11 min. [brackets] map to slides.md.*

---

[Slide: title]

In Module 1 we said you rarely train models yourself — you mostly use them. True.
But if you don't understand *how* a model learns, then fine-tuning, hallucination,
and evaluation will all feel like magic later. So this module is a short, honest
tour of training. And we won't just talk about it — at the end you'll run a real
network and watch it learn, live.

---

[Slide: one-sentence version]

Here's all of machine learning in one sentence: adjust a model's parameters,
over and over, until its predictions stop being wrong. That's it. Everything
else — all the math, all the frameworks — is detail on top of that sentence.

---

[Slide: four ingredients]

You need four things. Data: inputs, which we call features or X, and usually the
correct answers, called labels or y. A model: a function with adjustable
parameters that turns X into a prediction. A loss function: a single number
telling you how wrong the predictions are — lower is better. And an optimizer:
the rule for nudging the parameters to make that loss smaller. The classic
optimizer is gradient descent.

---

[Slide: training loop]

Now the heartbeat of all machine learning — the training loop. Four steps,
repeated. Forward: run the inputs through the model to get predictions. Loss:
measure how wrong they are. Backward: figure out how much each parameter
contributed to that error — those are the gradients. Update: nudge every
parameter a little to reduce the loss. Repeat thousands of times, and the loss
falls, predictions improve. That falling loss *is* learning. There's no secret
fifth step. A two-parameter line and a billion-parameter LLM both learn with
exactly this loop.

---

[Slide: gradient descent]

Let me make gradient descent intuitive. Picture standing on a foggy hill,
trying to get to the lowest point. You can't see far, but you can feel which way
is downhill, so you step that way, and repeat. That's it. The gradient is "which
way is downhill for the loss." The learning rate is how big a step you take. Too
small and training crawls. Too big and you overshoot the valley and bounce
around, maybe never settling. Picking a good learning rate is one of the first
knobs you'll ever tune.

---

[Slide: non-linearity]

Here's the idea that makes deep learning actually work. If your model is only
straight-line math, it can only learn straight-line relationships. And stacking
a hundred linear layers doesn't help — mathematically it's still just a line.
But real data — images, language — isn't linear.

The fix is to insert a non-linear activation function, like ReLU, between the
layers. That's what lets a network bend and fold to fit complex shapes. And
you're going to *prove* this yourself in the lab: a network with the
non-linearity learns a spiral-shaped dataset to about 99% accuracy. Delete that
one non-linearity and it collapses to around 50% — basically guessing. One line
of code, enormous difference.

---

[Slide: train/test split]

Now the discipline that separates people who understand ML from people who get
fooled by it. A model can simply memorize its training data — score a perfect
100% on it — and be completely useless on anything new. That's overfitting.

So you hold out some data the model never sees during training — the test set —
and you measure success on that. If a model scores 99% on training data but 61%
on the test set, it didn't learn, it memorized. The test number is the only one
that's honest. From now on, whenever anyone quotes you an accuracy, your reflex
should be: "on training data, or a held-out set?"

---

[Slide: kinds of ML]

Quick map of the territory. Supervised learning uses labeled examples, X to y —
that's classification and regression, and it's most of what you'll meet.
Unsupervised finds structure with no labels — clustering, and embeddings, which
we'll use heavily in Module 4. Reinforcement learning learns by trial and
reward. And LLMs? They're trained to predict the next token — that's supervised —
plus a round of tuning from human feedback. Same loop. Just an astonishing scale.

---

[Slide: lab]

Now go do it. In the lab you'll run the neural-net-from-scratch project and
actually watch the loss drop and accuracy climb epoch by epoch. Then you'll
delete the non-linearity and watch performance collapse — proving why it
matters. Then you'll run the scikit-learn pipeline and see the gap between
training and test accuracy with your own eyes. After that, Module 3: we get into
LLMs, and you'll make your first AI call from code.
