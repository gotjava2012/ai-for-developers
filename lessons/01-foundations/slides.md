---
marp: true
theme: default
paginate: true
header: "AI for Developers · Module 1 — Foundations"
---

# AI for Developers
## Module 1 — Foundations

Build the right mental model before writing any AI code.

---

## The term soup, settled

```
AI  ⊃  Machine Learning  ⊃  Deep Learning  ⊃  (Generative AI, LLMs)
```

- **AI** — make machines do human-like tasks (umbrella)
- **ML** — learn patterns from data instead of hand-coding rules
- **Deep Learning** — ML with many-layered neural networks
- **Generative AI / LLMs** — generate new text/code/images

> When someone says "AI," ask: *a trained model, or an LLM behind an API?*

---

## Why now?

Old ideas + three new ingredients:

1. **Data** — the internet
2. **Compute** — GPUs
3. **The transformer** (2017) — scales with data + compute

No magic. Just scale meeting one key architecture.

---

## The distinction that matters most

# Training ≠ Inference

---

## Training — building the model

- Feed data → model adjusts millions/billions of **parameters**
- Expensive, slow, done **rarely** (GPUs, weeks, $$$)
- Output: a **trained model**

## Inference — using the model

- Input → trained model → output
- Cheap, fast, done **constantly**
- **This is where 95% of developers work**

---

## The flow

```
[ lots of data ]
      │  TRAINING  (rare, expensive)
      ▼
[ trained model ]
      │  INFERENCE (constant, an API call)
      ▼
[ your app's output ]
```

You almost always **use** a model (inference), not train one.

---

## What AI is good at

- Pattern recognition (images, speech, anomalies)
- Generating & transforming text/code
- Summarizing, classifying, extracting structure

## What it can't do

- Guarantee **truth** (hallucination)
- Know your private data / post-cutoff facts (unless you supply them)
- Be deterministic without guardrails

---

## The mental model

> Treat an LLM like a **brilliant, fast, confident intern**
> who sometimes makes things up.
>
> Useful everywhere. Trusted nowhere without verification.

---

## Where you'll spend your time

1. Inference & prompting
2. Grounding with your data (RAG, fine-tuning)
3. Agents & tools
4. Evals, guardrails, cost, security
5. Training (rarely — usually fine-tuning)

---

## Lab + next up

**Lab:** read the key terms, then do the `lab/` exercise (a no-code concept
sorting + a first look at a model file).

**Next:** Module 2 — *How ML Actually Works* → you'll run a neural network and
watch it learn.
