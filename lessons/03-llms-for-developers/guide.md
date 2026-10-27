# Module 3 — LLMs for Developers

> **Goal:** Understand an LLM at the level you'd need to debug, cost, and
> optimize one in production — tokenization, the autoregressive loop, the
> sampling controls, context as a managed resource, and prompting as *context
> engineering* with characterizable failure modes. Then drive one from code.

---

## 3.1 The core object: an autoregressive conditional distribution

An LLM computes `P(next_token | tokens_so_far)` over a fixed vocabulary, then
generates by sampling one token, appending it, and repeating:

```
context → model → logits over vocab → sampling → next token → (append, repeat)
```

Two implications engineers under-appreciate:
- **Generation is sequential and O(tokens):** output latency scales with the
  number of tokens produced; input can be processed in parallel (prefill) but
  output is decoded one token at a time.
- **There is no state between requests** unless you supply it. "Memory" in a
  chat is just prior turns re-sent in the context. Conversation history is a
  thing *you* manage and pay for every turn.

---

## 3.2 Tokenization — the unit of everything

Models operate on **tokens**, not characters or words. A tokenizer (typically
**byte-pair encoding**) maps text to integer IDs from a fixed vocabulary
(~50k–200k). Practical consequences:

- Tokenization is **language- and content-dependent**: English prose is ~1.3
  tokens/word; code, JSON, non-English, and rare strings tokenize far less
  efficiently (more tokens → more cost and context used).
- **Everything is denominated in tokens** — context limits, pricing, latency.
  Estimating token counts for your actual payloads is a real budgeting step, not
  a rounding error.
- Tokenization artifacts explain classic failures (character-counting,
  arithmetic on digits, reversing strings) — the model never sees characters.

---

## 3.3 Context window — a hard, quadratic-cost resource

Attention cost scales ~**quadratically** with sequence length, so the context
window is a bounded resource with real price/latency implications. You are
always managing a budget that must hold: system prompt + instructions + few-shot
examples + retrieved evidence + conversation history + the room for the output.

- **Larger windows ≠ free.** Long context raises latency and cost and can *lower*
  quality — models exhibit **"lost in the middle"**, attending better to the
  start and end than the middle. More context is not strictly better.
- **Context management is an engineering task:** truncation, summarization of old
  turns, retrieval of only relevant chunks (Module 4), and ordering matters.

---

## 3.4 The sampling controls — what the knobs actually do

Decoding converts logits into a token. The knobs:

- **Temperature** — scales the logits before softmax. T→0 approaches greedy
  (argmax), high T flattens the distribution toward uniform (more diverse, more
  error). Low for extraction/structured output; higher for ideation.
- **top-p (nucleus)** — sample only from the smallest set of tokens whose
  cumulative probability ≥ p. Adaptively truncates the tail.
- **top-k** — restrict to the k most probable tokens.
- **frequency/presence penalties** — discourage repetition.
- **stop sequences / max_tokens** — hard termination controls; `max_tokens`
  bounds cost and runaway output.

Determinism requires T=0 **and** a pinned model version — and even then can vary
across providers/hardware due to floating-point and batching nondeterminism.
Don't design on an assumption of bit-reproducible output.

---

## 3.5 Prompting is context engineering

A prompt is the model's entire input state; treat it with the rigor of an API
contract. Techniques, with *why* they work:

- **System prompt** sets a persistent instruction/role separate from user input.
  Use it to establish rules, output contract, and refusal behavior.
- **Structured output** — specify a schema and show an exemplar; pair with
  provider features (JSON mode, function/tool schemas) rather than hoping.
- **Few-shot** — in-context examples steer the output distribution far more
  reliably than prose instructions; 2–5 well-chosen examples often dominate.
- **Delimit instructions from data** — untrusted content goes in clearly marked
  regions so the model (and you) can distinguish commands from payload. This is
  also your first line against **prompt injection** (Module 6).
- **Chain-of-thought / decomposition** — eliciting intermediate steps improves
  multi-step tasks; for latency/cost you can keep the reasoning hidden or move it
  to a cheaper model.

Failure modes to expect and test for: instruction drift over long contexts,
sensitivity to phrasing/ordering, silent format violations, and
over-confident fabrication.

---

## 3.6 Hallucination, precisely — and the mitigation hierarchy

A model samples from `P(plausible continuation)`, which is **not** `P(true
statement)`. Fabrication is therefore an intrinsic property, not a defect to be
patched. You manage its *rate and blast radius*:

1. **Ground it** — supply the facts in-context and instruct answer-only-from-
   context (RAG, Module 4). The highest-leverage mitigation.
2. **Constrain the output** — schemas, enums, tool calls with validated args,
   refusal paths.
3. **Lower temperature** for factual tasks.
4. **Verify** — require citations and check them; cross-check against sources.
5. **Evaluate** — measure the fabrication rate on a golden set; track it across
   prompt/model changes (Module 6).

> The architectural error is treating output as authoritative. Design for a
> known, nonzero fabrication rate and put the cost of a wrong answer behind a
> validation or human-in-the-loop gate proportional to that cost.

---

## 3.7 Deployment surface — the real tradeoffs

- **Hosted frontier APIs** (OpenAI, Anthropic, Google) — highest capability,
  per-token pricing, data egress and vendor dependence; fastest to build.
- **Open-weight models** (Llama, Qwen, Mistral) self-hosted or via inference
  providers — control, privacy, fixed infra cost, fine-tunable; you own ops,
  scaling, and quality gaps.
- **Local runtimes** (Ollama, llama.cpp) — free, private, offline; smaller models
  and lower quality, ideal for dev/prototyping and privacy-bound workloads.
- **Quantization** (8-/4-bit) trades a little quality for large memory/latency
  wins — what makes capable models run on modest hardware.

Selection is a cost/capability/privacy/ops tradeoff, and increasingly a
**routing** decision (cheap model for easy calls, frontier for hard ones —
Module 6).

---

## Terms, at working precision
- **Autoregressive decoding** — generate one token at a time, each conditioned on all prior.
- **BPE tokenization** — subword vocabulary; the unit of context, cost, latency.
- **Prefill vs. decode** — parallel input processing vs. sequential output generation.
- **Temperature / top-p / top-k** — the sampling-distribution controls.
- **Context budget** — finite, quadratic-cost window you allocate across prompt/evidence/history/output.
- **Lost-in-the-middle** — degraded attention to mid-context content.

## Check yourself
1. Why does output latency scale with tokens generated while input mostly doesn't?
2. Give two reasons a longer context window can *hurt* rather than help.
3. Distinguish temperature, top-p, and top-k in terms of how each shapes the sampling set.
4. Why is "character counting / string reversal" a predictable weak spot, given tokenization?
5. State hallucination as a statement about two different distributions, and rank the mitigations by leverage.

➡️ **Lab:** drive a model from code; observe prefill/decode latency; manipulate
temperature/top-p; force structured output; and reproduce a fabrication to
internalize the failure mode.
