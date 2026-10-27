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

```svg
<svg viewBox="0 0 620 200" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <text x="160" y="22" text-anchor="middle" font-size="16" font-weight="bold" fill="#1f2a44">Classical software</text>
  <rect x="40" y="36" width="90" height="40" rx="6" fill="#eef4ff" stroke="#b9c4da"/><text x="85" y="61" text-anchor="middle" font-size="13">rules + data</text>
  <rect x="190" y="36" width="90" height="40" rx="6" fill="#1f2a44"/><text x="235" y="61" text-anchor="middle" font-size="13" fill="#fff">computer</text>
  <rect x="115" y="110" width="90" height="40" rx="6" fill="#2a7d5f"/><text x="160" y="135" text-anchor="middle" font-size="13" fill="#fff">answers</text>
  <path d="M130 56 H190" stroke="#1f2a44" stroke-width="2.5" fill="none" marker-end="url(#f1)"/>
  <path d="M235 76 V110 H205" stroke="#1f2a44" stroke-width="2.5" fill="none" marker-end="url(#f1)"/>
  <text x="460" y="22" text-anchor="middle" font-size="16" font-weight="bold" fill="#2a7d5f">Machine learning</text>
  <rect x="340" y="36" width="90" height="40" rx="6" fill="#eef4ff" stroke="#b9c4da"/><text x="385" y="54" text-anchor="middle" font-size="12">data +</text><text x="385" y="69" text-anchor="middle" font-size="12">answers</text>
  <rect x="490" y="36" width="90" height="40" rx="6" fill="#1f2a44"/><text x="535" y="61" text-anchor="middle" font-size="13" fill="#fff">computer</text>
  <rect x="415" y="110" width="90" height="40" rx="6" fill="#2a7d5f"/><text x="460" y="128" text-anchor="middle" font-size="12" fill="#fff">rules</text><text x="460" y="143" text-anchor="middle" font-size="11" fill="#cfe9df">(learned f)</text>
  <path d="M430 56 H490" stroke="#2a7d5f" stroke-width="2.5" fill="none" marker-end="url(#f2)"/>
  <path d="M535 76 V110 H505" stroke="#2a7d5f" stroke-width="2.5" fill="none" marker-end="url(#f2)"/>
  <defs>
    <marker id="f1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#1f2a44"/></marker>
    <marker id="f2" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#2a7d5f"/></marker>
  </defs>
</svg>
```
<p class="diagram-caption">ML inverts the inputs: you give data + answers, it outputs the rules (a learned function).</p>

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

```svg
<svg viewBox="0 0 620 170" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <!-- training side -->
  <rect x="30" y="30" width="250" height="110" rx="10" fill="#fdf3e6" stroke="#f0a500" stroke-width="2"/>
  <text x="155" y="52" text-anchor="middle" font-size="15" font-weight="bold" fill="#b9770a">TRAINING (rare, offline)</text>
  <text x="155" y="78" text-anchor="middle" font-size="13" fill="#333">forward → loss → backward → update θ</text>
  <text x="155" y="100" text-anchor="middle" font-size="12" fill="#555">memory ≈ several × |θ|</text>
  <text x="155" y="120" text-anchor="middle" font-size="12" fill="#555">cost: GPU-hours, data scale</text>
  <!-- inference side -->
  <rect x="340" y="30" width="250" height="110" rx="10" fill="#eafaf3" stroke="#2a7d5f" stroke-width="2"/>
  <text x="465" y="52" text-anchor="middle" font-size="15" font-weight="bold" fill="#1d6a4f">INFERENCE (constant, online)</text>
  <text x="465" y="78" text-anchor="middle" font-size="13" fill="#333">forward only → output</text>
  <text x="465" y="100" text-anchor="middle" font-size="12" fill="#555">memory ≈ |θ| (+ KV cache)</text>
  <text x="465" y="120" text-anchor="middle" font-size="12" fill="#555">cost: tokens/requests, latency SLOs</text>
  <path d="M280 85 H340" stroke="#1f2a44" stroke-width="3" fill="none" marker-end="url(#t1)"/>
  <text x="310" y="76" text-anchor="middle" font-size="12" fill="#1f2a44">ship θ</text>
  <defs><marker id="t1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#1f2a44"/></marker></defs>
</svg>
```
<p class="diagram-caption">Two different workloads — you almost always own the right-hand one.</p>

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
