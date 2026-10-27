# Module 1 — Foundations

> **Audience:** experienced engineers who haven't built AI systems yet. We don't
> rehearse software basics. We build an accurate working model of how modern AI
> is actually constructed and deployed, and the engineering decisions that follow
> from it.

---

## 1.1 A precise definition, not a taxonomy lecture

The term hierarchy (AI ⊃ ML ⊃ deep learning ⊃ LLMs) is real but low-value. The
distinction that actually affects your architecture:

- **Classical software** encodes *explicit* logic: you write the rules.
- **Machine learning** fits a *parameterized function* to data: you specify an
  objective and let optimization find parameters that minimize error. You no
  longer author the logic; you author the objective, the data, and the
  architecture, and you inherit a function you cannot fully introspect.

That last clause is the whole shift. An ML component is a **learned function
with opaque internals and a non-trivial error distribution**. Everything hard
about AI engineering — evaluation, guardrails, hallucination, drift — follows
from the fact that you're shipping a statistical function, not deterministic
code.

**Deep learning** is the subset where that function is a many-layer neural
network trained by gradient descent. **LLMs** are deep networks (transformers)
trained on next-token prediction over internet-scale corpora. Generative models
are the ones whose output space is content (text/image/audio) rather than a
label or number.

---

## 1.2 The parameterized-function mental model

A neural network is a composition of differentiable operations:

```
f(x; θ) = layer_n(... layer_2(layer_1(x)))      θ = all the weights
```

Each layer is typically an **affine transform followed by a non-linearity**:
`h = σ(Wx + b)`. The non-linearity σ (ReLU, GELU) is load-bearing — without it,
any depth collapses to a single affine map (composition of linear maps is
linear), and the network can only represent hyperplanes. With it, the network is
a **universal function approximator**: given enough width/depth, it can
approximate arbitrary continuous functions. Training is the search for θ that
makes f fit your data.

You will internalize this concretely in Module 2 by reading and running a
backprop implementation.

---

## 1.3 Training vs. inference — a systems-level distinction

These are different workloads with different cost models, hardware profiles, and
operational characteristics. Conflating them produces bad architecture.

| | **Training** | **Inference** |
|---|---|---|
| What | Solve for θ that minimizes loss over a dataset | Evaluate f(x; θ) for a new x |
| Compute | Forward + backward pass + optimizer state; memory ≈ several× parameter count | Forward pass only; memory ≈ parameter count (+ KV cache for LLMs) |
| Frequency | Rare, batch, offline | Constant, often latency-sensitive, online |
| Cost driver | GPU-hours, dataset scale | Tokens/requests, latency SLOs |
| Who owns it | Labs / specialized teams | **You**, almost always |

The practical consequence: as an application engineer you operate almost
entirely in the **inference** regime against a foundation model someone else
trained for seven or eight figures. Your leverage is in *how you use it* —
context construction, retrieval, tool integration, routing, caching,
evaluation — not in the weights. Training enters your world as **fine-tuning**
(Module 4), which is a comparatively small, targeted optimization.

---

## 1.4 Why transformers, specifically

Modern capability is not a generic "neural nets got bigger" story — it's
architecture-specific. Two properties of the transformer matter to you:

1. **Self-attention** lets every token condition on every other token in the
   context in parallel, with learned, content-dependent weighting. This replaced
   the sequential bottleneck of RNNs and made it possible to model long-range
   dependencies.
2. **It parallelizes across the sequence**, so training saturates modern
   accelerators — which is what made internet-scale pretraining economically
   feasible. Capability then tracks **scaling laws**: loss falls predictably as
   a power law in parameters, data, and compute.

You don't need to derive attention today, but hold two consequences:
- The **context window** is a hard architectural resource (attention is roughly
  quadratic in sequence length), so context is finite and costly — a budget you
  manage, not an afterthought.
- Capability emerges from scale and data, which is *why* these models are
  general-purpose and *why* their failure modes (hallucination, prompt
  sensitivity) are statistical rather than fixable bugs.

---

## 1.5 What a foundation model is and isn't, stated precisely

An LLM is a **conditional next-token distribution** `P(token | context)`,
sampled autoregressively. Reframing the usual "it's good at X / bad at Y" list
in those terms:

- It models the *distribution of plausible continuations* of its training
  corpus. "Knowledge" is lossy, parametric compression of that corpus — not a
  queryable store. Hence: fluent, frequently correct, and **confidently wrong at
  a non-zero rate that no prompt eliminates**.
- It has **no epistemic access to truth, your private data, or post-cutoff
  facts** unless you place them in the context. This is precisely why retrieval
  (RAG) exists — not as a feature, but as the mechanism for grounding a
  distribution in facts.
- Sampling is **stochastic** (temperature, top-p). Determinism requires
  temperature 0 *and* a fixed model version, and even then isn't guaranteed
  across providers/hardware.
- It is **not an agent, planner, or reasoner by construction**. Apparent
  reasoning is next-token prediction that has learned to emit reasoning-shaped
  text; it improves with technique (chain-of-thought, tools) but remains
  fallible.

Engineering stance that follows: treat model output as an **untrusted,
probabilistic input** to your system, with a known-nonzero error rate, that must
be constrained, validated, and evaluated — the same discipline you'd apply to
any unreliable upstream dependency.

---

## 1.6 Where the engineering actually lives

Ranked by where you'll spend effort building real systems:

1. **Context engineering** — what you put in the window: prompts, retrieved
   evidence, tool results, history. The dominant lever on quality (Modules 3–4).
2. **Grounding & customization** — RAG vs. fine-tuning vs. long-context, and the
   cost/freshness/attribution tradeoffs among them (Module 4).
3. **Orchestration** — tools, agents, control flow, when to let the model drive
   vs. when to constrain it (Module 5).
4. **Evaluation & reliability** — eval harnesses, guardrails, observability, cost
   and latency budgets, security. This is what separates a demo from production
   (Module 6).
5. **Training/fine-tuning** — occasional, targeted, usually parameter-efficient
   (LoRA), and the last resort after prompting + retrieval (Module 4).

Module 2 drops one level down to make the "learned function" concrete — you'll
run gradient descent and watch θ converge — because the rest of the course
(fine-tuning, hallucination, evals) only makes sense if training isn't a black
box to you.

---

## Terms, defined at working precision
- **Parameters (θ) / weights** — the fitted numbers defining f; "model size" ≈ |θ|.
- **Affine + non-linearity** — the per-layer primitive `σ(Wx+b)`; σ is what buys expressivity.
- **Autoregressive sampling** — generating one token at a time, each conditioned on all prior tokens.
- **Context window** — the finite token budget attention operates over; quadratic cost in length.
- **Scaling laws** — loss falls as a power law in params/data/compute; the basis of the capability boom.
- **Foundation model** — a large pretrained model used as a base for many downstream tasks via inference or fine-tuning.

## Check yourself
1. Why does stacking linear layers without a non-linearity gain you nothing?
2. State the training/inference distinction in terms of compute and memory, not just "build vs. use."
3. Why is the context window a hard resource rather than a soft limit?
4. Reframe "LLMs hallucinate" as a statement about distributions. Why does that reframing predict that no prompt fully fixes it?
5. Given 1.6, where would you expect to spend most engineering effort on a real LLM product — and why *not* on training?

➡️ **Lab:** make "learned function," "parameters," and "inference" concrete,
then compare a 2-parameter model to a billion-parameter one to ground the
scaling intuition.
