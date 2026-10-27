# Module 1 — Foundations

> **Goal:** Build the correct mental model of what AI is, clear up the term
> soup, and understand the one distinction that matters most for developers:
> **training vs. inference.**

---

## 1.1 The term soup, settled

These words get used interchangeably and it causes real confusion. Here's the
clean hierarchy:

- **Artificial Intelligence (AI)** — the broad field: making machines do things
  that normally need human intelligence. An umbrella term.
- **Machine Learning (ML)** — a *subset* of AI: instead of hand-coding rules,
  you let a program *learn patterns from data*. This is where almost all modern
  "AI" actually lives.
- **Deep Learning** — a *subset* of ML that uses **neural networks** with many
  layers. It's what made image recognition, speech, and language models work.
- **Generative AI** — applications of deep learning that *generate* new content
  (text, images, audio, code) rather than just classifying or predicting.
- **Large Language Models (LLMs)** — generative models trained on huge amounts
  of text (GPT, Claude, Llama). The thing most people mean today when they say
  "AI."

```
AI  ⊃  Machine Learning  ⊃  Deep Learning  ⊃  (Generative AI, LLMs)
```

**Developer takeaway:** when someone says "AI," ask "do you mean a trained ML
model, or an LLM behind an API?" The engineering is very different.

---

## 1.2 Why now? (the honest history in 60 seconds)

The ideas behind neural networks are decades old. Three things changed recently
and made modern AI explode:

1. **Data** — the internet produced massive training datasets.
2. **Compute** — GPUs made training huge models practical.
3. **The transformer** (2017) — a neural-network architecture that scales
   extremely well with data and compute. Every modern LLM is a transformer.

That's it. No magic — just old ideas meeting enough data and hardware, plus one
key architectural breakthrough.

---

## 1.3 The distinction that matters most: training vs. inference

This is the single most important mental model for a developer. AI has **two
completely separate phases**, with different costs, tools, and skills:

### Training (building the model)
- You feed a model lots of data and it adjusts millions/billions of internal
  numbers (**parameters**) to minimize its errors.
- Expensive, slow, done rarely. Big LLMs cost millions of dollars and weeks of
  GPU time to train.
- Output: a **model** (a big file of learned parameters).

### Inference (using the model)
- You give the already-trained model an input and it produces an output.
- Cheap-ish, fast, done constantly. This is what happens every time you call an
  LLM API or run a model locally.
- **This is where 95% of developers work.** You rarely train a model from
  scratch; you *use* one via inference.

```
   [ lots of data ]
          │  TRAINING  (rare, expensive, GPUs)
          ▼
   [ trained model ]
          │  INFERENCE (constant, cheap, an API call)
          ▼
   [ your app's output ]
```

**Why this matters:** when you build an AI feature, you're almost always doing
**inference** against a model someone else trained (GPT, Claude, Llama). Your
job is prompting, retrieval, tool integration, evaluation, and cost control —
not training from scratch. Knowing this keeps you from over-engineering (and
from being intimidated by the "you need a PhD and a GPU cluster" myth).

---

## 1.4 What AI is genuinely good at — and what it is not

Set expectations correctly up front; it saves you from building the wrong thing.

**Good at:**
- Pattern recognition (images, speech, anomalies)
- Generating and transforming text/code
- Summarizing, classifying, extracting structure from messy input
- Working across language and modality

**Genuinely bad at / cannot do:**
- **Guaranteeing truth.** LLMs predict plausible text; they will state false
  things confidently (**hallucination** — Module 3).
- **Real reasoning about facts it wasn't trained on** (unless you give it the
  facts — that's RAG, Module 4).
- **Determinism.** The same prompt can give different outputs. Don't use a raw
  LLM where you need exact, repeatable results without guardrails.
- **Knowing anything after its training cutoff**, or your private data, unless
  you supply it.

**Developer takeaway:** treat an LLM like a brilliant, fast, confident intern
who sometimes makes things up — useful everywhere, trusted nowhere without
verification.

---

## 1.5 Where you'll spend your time as an AI developer

In rough order of how often you'll do each:
1. **Inference & prompting** — calling models, designing prompts (Module 3)
2. **Grounding with your data** — RAG and fine-tuning (Module 4)
3. **Agents & tools** — letting models take actions (Module 5)
4. **Evaluation, guardrails, cost, security** — making it production-ready (Module 6)
5. **Training** — occasionally, and usually *fine-tuning*, not from scratch (Module 4)

Modules 2 is a short detour *into* training — not because you'll do it daily,
but because understanding how a model learns makes everything above make sense.

---

## Key terms from this module
- **Model** — a file of learned parameters that maps inputs to outputs.
- **Parameters / weights** — the numbers a model adjusts during training.
- **Training** — the (expensive) process of learning those numbers from data.
- **Inference** — using a trained model to produce output (what your app does).
- **Transformer** — the neural-network architecture behind modern LLMs.
- **Hallucination** — when a model produces confident but false output.

## Check yourself
1. Put these in order from broadest to narrowest: Deep Learning, AI, LLM, ML.
2. When you call the OpenAI API, are you doing training or inference?
3. Give one task an LLM is great at and one it should not be trusted with.
4. Why don't most AI developers train models from scratch?

➡️ **Next:** Module 2 — *How ML Actually Works*, where you'll run a neural
network and watch it learn. See the `lab/` folder for this module's hands-on
exercise first.
