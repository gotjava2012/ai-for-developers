---
marp: true
theme: default
paginate: true
header: "AI for Developers · Module 3 — LLMs for Developers"
---

# Module 3 — LLMs for Developers
### Enough mechanism to debug, cost, and optimize one

---

## The core object

`P(next_token | tokens_so_far)` → sample → append → repeat

```
context → model → logits over vocab → sampling → next token → (repeat)
```

- Generation is **sequential, O(tokens)** → output latency ∝ tokens produced
- **No cross-request state** unless you supply it — chat "memory" is prior turns
  re-sent (and re-paid) every turn

---

## Tokenization — the unit of everything

Models see **tokens** (BPE subwords), not chars/words. Vocab ~50k–200k.

- Content-dependent: English ≈1.3 tok/word; **code/JSON/non-English cost more**
- Context limits, pricing, latency are **all** token-denominated
- Explains classic failures: char-counting, digit arithmetic, string reversal —
  the model never sees characters

---

## Context window = hard, quadratic-cost resource

Attention ≈ **O(n²)** in length. The window must hold:
system + instructions + few-shot + retrieved evidence + history + output room.

- Bigger ≠ free: ↑latency, ↑cost, and often ↓quality
- **Lost-in-the-middle**: better attention at the ends than the middle
- Context management (truncate / summarize / retrieve / order) is real engineering

---

## Sampling controls — what the knobs do

- **Temperature** — scales logits; T→0 ≈ greedy, high T flattens (diverse, error-prone)
- **top-p (nucleus)** — smallest set with cumulative prob ≥ p
- **top-k** — restrict to k most probable
- **frequency/presence penalties** — curb repetition
- **stop / max_tokens** — hard termination & cost bound

> Determinism needs T=0 **and** pinned version — and still isn't guaranteed.

---

## Prompting = context engineering

- **System prompt** — persistent rules / output contract / refusal behavior
- **Structured output** — schema + exemplar + provider JSON/tool mode
- **Few-shot** — 2–5 examples steer the distribution > prose instructions
- **Delimit instructions vs. data** — first defense vs. prompt injection
- **CoT / decomposition** — improves multi-step; can hide or offload to cheaper model

Expect & test: instruction drift, phrasing/order sensitivity, silent format breaks.

---

## Hallucination, precisely

Model samples `P(plausible)` ≠ `P(true)` → fabrication is **intrinsic**, not a bug.

Manage rate + blast radius (by leverage):
1. **Ground it** (RAG) — highest leverage
2. **Constrain output** — schemas, enums, validated tool args
3. **Lower temperature** for facts
4. **Verify** — citations, cross-check
5. **Evaluate** — measure fabrication rate, track across changes

> Put the cost of a wrong answer behind a gate proportional to that cost.

---

## Deployment surface — tradeoffs

- **Hosted frontier** — top capability, per-token $, data egress, vendor lock
- **Open-weight self-host** — control/privacy/fixed cost/fine-tunable; you own ops
- **Local** (Ollama/llama.cpp) — free, private, offline, smaller/weaker
- **Quantization** (8/4-bit) — small quality hit for big memory/latency win

Increasingly a **routing** decision: cheap for easy, frontier for hard.

---

## Next

**Lab:** drive a model from code; watch prefill vs decode latency; move
temperature/top-p; force structured output; reproduce a fabrication.

**Module 4:** grounding & customization — RAG vs fine-tuning, with failure modes
and eval metrics.
