---
marp: true
theme: default
paginate: true
header: "AI for Developers · Module 1 — Foundations"
---

# Module 1 — Foundations
### An accurate mental model of how modern AI is built and deployed

For engineers who ship systems. No software basics; just the parts that change
your architecture.

---

## The shift that matters

- **Classical software** — you author explicit logic
- **Machine learning** — you author the *objective, data, architecture*; optimization
  fits a **parameterized function** you can't fully introspect

> You're shipping a **learned function** with opaque internals and a nonzero
> error distribution — not deterministic code.

Everything hard downstream (eval, guardrails, hallucination, drift) follows from
that single fact.

---

## The parameterized-function model

```
f(x; θ) = layer_n(… layer_2(layer_1(x)))      θ = all weights
per layer:   h = σ(Wx + b)
```

- σ (ReLU/GELU) is **load-bearing**: without it, any depth collapses to one
  affine map → only hyperplanes
- With it: **universal function approximator**
- **Training** = search for θ that fits the data (you'll run it in Module 2)

---

## Training vs. inference — a systems distinction

| | Training | Inference |
|---|---|---|
| Work | forward + backward + optimizer state | forward only |
| Memory | ≈ several× \|θ\| | ≈ \|θ\| (+ KV cache) |
| Cadence | rare, offline, batch | constant, online, latency-bound |
| Cost driver | GPU-hours, data scale | tokens/requests, SLOs |
| You own | rarely | **almost always** |

Your leverage is in **how you use** the model, not the weights.

---

## Why transformers specifically

Not "nets got bigger" — architecture-specific:

- **Self-attention** — every token conditions on every other, in parallel,
  content-dependent weighting → long-range dependencies
- **Parallel across sequence** → saturates accelerators → internet-scale
  pretraining became economical
- Capability tracks **scaling laws** (loss ↓ as power law in params/data/compute)

Two consequences you live with: **context is quadratic-cost & finite**; failure
modes are **statistical**, not bugs.

---

## A foundation model, stated precisely

An LLM is a conditional next-token distribution **P(token | context)**, sampled
autoregressively.

- "Knowledge" = lossy parametric compression of the corpus — **not** a queryable store
- → fluent, often right, **confidently wrong at a nonzero rate no prompt removes**
- No access to truth / your data / post-cutoff facts unless it's **in the context** (→ why RAG exists)
- Sampling is **stochastic**; determinism needs temp 0 + pinned version (and still isn't guaranteed)

---

## The engineering stance

> Treat model output as an **untrusted, probabilistic input** with a known
> nonzero error rate — constrain it, validate it, evaluate it.

The same discipline you'd apply to any unreliable upstream dependency.

---

## Where the effort actually goes

1. **Context engineering** — what's in the window (dominant quality lever)
2. **Grounding & customization** — RAG vs fine-tune vs long-context
3. **Orchestration** — tools, agents, control flow
4. **Evaluation & reliability** — evals, guardrails, cost/latency, security
5. **Training/fine-tuning** — rare, targeted, last resort

Note what's #5. You compete on **systems around the model**, not the model.

---

## Next

**Lab:** make "learned function / parameters / inference" concrete; ground the
scaling intuition (2 params → 1B params, same idea).

**Module 2:** drop a level — run gradient descent, watch θ converge, so training
is never a black box.
