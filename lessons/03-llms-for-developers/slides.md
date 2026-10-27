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

```svg
<svg viewBox="0 0 600 140" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <text x="30" y="35" font-size="15" fill="#333">"tokenization"  →</text>
  <g font-size="15" font-weight="bold">
    <rect x="175" y="18" width="55" height="26" rx="4" fill="#dbe7ff" stroke="#6b8fd6"/><text x="202" y="36" text-anchor="middle" fill="#1f2a44">token</text>
    <rect x="236" y="18" width="40" height="26" rx="4" fill="#dbe7ff" stroke="#6b8fd6"/><text x="256" y="36" text-anchor="middle" fill="#1f2a44">iz</text>
    <rect x="282" y="18" width="52" height="26" rx="4" fill="#dbe7ff" stroke="#6b8fd6"/><text x="308" y="36" text-anchor="middle" fill="#1f2a44">ation</text>
  </g>
  <text x="355" y="36" font-size="14" fill="#555">→ IDs [15496, 1634, 341]</text>
  <text x="30" y="82" font-size="13" fill="#333">English ≈ 1.3 tok/word</text>
  <rect x="30" y="92" width="120" height="16" fill="#2a7d5f"/>
  <text x="300" y="82" font-size="13" fill="#333">code / JSON / non-English = more tokens</text>
  <rect x="300" y="92" width="260" height="16" fill="#c0392b"/>
  <text x="300" y="124" font-size="11" fill="#c0392b" font-weight="bold">same meaning, higher cost →</text>
</svg>
```
<p class="diagram-caption">Text is split into subword tokens → integer IDs. Everything is billed per token.</p>

- Content-dependent: English ≈1.3 tok/word; **code/JSON/non-English cost more**
- Context limits, pricing, latency are **all** token-denominated
- Explains classic failures: char-counting, digit arithmetic, string reversal —
  the model never sees characters

---

## Context window = hard, quadratic-cost resource

Attention ≈ **O(n²)** in length. The window must hold:
system + instructions + few-shot + retrieved evidence + history + output room.

```svg
<svg viewBox="0 0 560 170" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <text x="160" y="22" text-anchor="middle" font-size="14" font-weight="bold" fill="#1f2a44">What fills the context window</text>
  <g font-size="12" fill="#1a1a1a">
    <rect x="30" y="32" width="260" height="20" fill="#1f2a44"/><text x="36" y="47" fill="#fff">system + instructions</text>
    <rect x="30" y="54" width="260" height="20" fill="#3a5c99"/><text x="36" y="69" fill="#fff">few-shot examples</text>
    <rect x="30" y="76" width="260" height="20" fill="#6b8fd6"/><text x="36" y="91" fill="#fff">retrieved evidence (RAG)</text>
    <rect x="30" y="98" width="260" height="20" fill="#a9c0e8"/><text x="36" y="113">conversation history</text>
    <rect x="30" y="120" width="260" height="20" fill="#2a7d5f"/><text x="36" y="135" fill="#fff">room for the output</text>
  </g>
  <!-- cost curve O(n^2) -->
  <line x1="340" y1="140" x2="540" y2="140" stroke="#333" stroke-width="2"/>
  <line x1="340" y1="140" x2="340" y2="30" stroke="#333" stroke-width="2"/>
  <path d="M340 140 Q490 140 530 36" fill="none" stroke="#c0392b" stroke-width="3"/>
  <text x="440" y="158" text-anchor="middle" font-size="12" fill="#333">length n →</text>
  <text x="470" y="60" font-size="13" fill="#c0392b" font-weight="bold">cost ∝ n²</text>
</svg>
```
<p class="diagram-caption">The window is a fixed budget everything shares — and attention cost grows with its square.</p>

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
