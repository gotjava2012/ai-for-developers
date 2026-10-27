# Module 1 Lab — Foundations (hands-on)

Two short exercises. The first is no-code (lock in the mental model); the second
is a tiny script that makes "model," "parameters," and "inference" concrete.

---

## Exercise 1 — Sort the concepts (no code, 2 min)

Without looking back at the guide, label each item as **AI**, **ML**,
**Deep Learning**, or **LLM/Generative** — and for each tool, say whether using
it is **training** or **inference**:

1. A spam filter that learned from labeled emails → _ML or DL? training or inference when it checks a new email?_
2. Calling the OpenAI API to summarize a document → _which phase?_
3. A hand-written `if/else` rules engine with no learning → _is this even AI/ML?_
4. GPT-4 generating code → _which category?_
5. Spending 3 weeks on GPUs to build a model → _which phase?_

<details>
<summary>Answers</summary>

1. ML (specifically could be DL); checking a new email is **inference**.
2. **Inference** (the model was already trained).
3. Not ML — it's hand-coded rules. (It's arguably "AI" by the loosest
   definition, but there's no *learning*.)
4. Generative AI / LLM (a subset of deep learning).
5. **Training.**
</details>

---

## Exercise 2 — Make "inference" real (10 lines of code)

You don't need a giant model to understand inference. A trained model is just
**parameters** (numbers) plus a rule for turning input into output. Here's the
smallest possible "model": a linear model `y = w*x + b`, already "trained"
(we just set the parameters by hand).

Run it:
```bash
python3 tiny_model.py
```

Open `tiny_model.py` and notice:
- `w` and `b` are the **parameters** (what training would learn).
- `predict()` is **inference** — using the parameters to produce output.
- We *set* the parameters manually here; in Module 2 you'll watch a real network
  *learn* them from data.

### Then: look at a real model's parameters
If you have Ollama installed, run:
```bash
ollama list          # see models you have (each is a file of learned parameters)
```
A small model like `llama3.2:1b` has ~1 **billion** parameters. Your
`tiny_model.py` has exactly **2** (`w` and `b`). Same idea — just a difference
of a billion-ish. That's the whole secret: scale.

---

## What you should take away
- A "model" = parameters + a function that uses them.
- **Training** = finding good parameter values from data (Module 2).
- **Inference** = running the function with those values (what your apps do).
- Big models are the same concept at massive scale.

➡️ **Next:** Module 2 — you'll train a real neural network and watch the
parameters improve, live.
