---
marp: true
theme: default
paginate: true
header: "AI for Developers · Module 6 — Production & Responsible AI"
---

# Module 6 — Production & Responsible AI Engineering
### The discipline that separates a demo from a trustworthy system

---

## Evaluation — hardest, most skipped

Non-deterministic, open-ended output → no exact-match tests. Build an **eval
system** that **gates changes**:

- **Golden sets** — curated fixtures = regression suite
- **Programmatic checks** — schema, required fields, must-cite, forbidden content
- **Reference metrics** — exact match / F1 / embedding similarity
- **LLM-as-judge** — scales, but biased + nondeterministic → **validate vs humans**, pin the judge
- **Human eval** — ground truth for high-stakes

---

## Offline vs online

- **Offline** evals gate deploys (quality CI)
- **Online** — A/B, user signals, trace sampling — catches drift offline misses

> The question for any number: *which dataset, which metric, does it gate
> releases?* Unmeasured quality = unmonitored production change.

---

## Guardrails — layered control architecture

- **Input** — injection detect, PII redaction, topic/abuse, size limits
- **Output** — schema/type, grounding/faithfulness, toxicity/PII, policy
- **Action** — authz, allow-lists, confirmation/human-in-loop, spend caps
- **Fallbacks** — retry / degrade / refuse / escalate (no fallback = outage)

```svg
<svg viewBox="0 0 600 170" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <g font-size="12">
    <rect x="20"  y="60" width="70" height="46" rx="6" fill="#eef4ff" stroke="#b9c4da"/><text x="55" y="88" text-anchor="middle">user input</text>
    <rect x="120" y="55" width="70" height="56" rx="6" fill="#f0a500"/><text x="155" y="79" text-anchor="middle" fill="#fff" font-weight="bold">INPUT</text><text x="155" y="96" text-anchor="middle" fill="#fff" font-size="10">guardrail</text>
    <rect x="220" y="60" width="70" height="46" rx="6" fill="#1f2a44"/><text x="255" y="88" text-anchor="middle" fill="#fff">LLM</text>
    <rect x="320" y="55" width="70" height="56" rx="6" fill="#f0a500"/><text x="355" y="79" text-anchor="middle" fill="#fff" font-weight="bold">OUTPUT</text><text x="355" y="96" text-anchor="middle" fill="#fff" font-size="10">guardrail</text>
    <rect x="420" y="55" width="70" height="56" rx="6" fill="#c0392b"/><text x="455" y="79" text-anchor="middle" fill="#fff" font-weight="bold">ACTION</text><text x="455" y="96" text-anchor="middle" fill="#fff" font-size="10">guardrail</text>
    <rect x="520" y="60" width="66" height="46" rx="6" fill="#2a7d5f"/><text x="553" y="82" text-anchor="middle" fill="#fff" font-size="11">DB/email</text><text x="553" y="97" text-anchor="middle" fill="#fff" font-size="11">/pay</text>
  </g>
  <g stroke="#333" stroke-width="2" fill="none" marker-end="url(#c1)">
    <path d="M90 83 H120"/><path d="M190 83 H220"/><path d="M290 83 H320"/><path d="M390 83 H420"/><path d="M490 83 H520"/>
  </g>
  <text x="300" y="30" text-anchor="middle" font-size="13" font-weight="bold" fill="#1f2a44">Defense in depth: a checkpoint at every stage</text>
  <text x="300" y="140" text-anchor="middle" font-size="12" fill="#c0392b">validation proportional to the cost of being wrong ↑</text>
  <defs><marker id="c1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#333"/></marker></defs>
</svg>
```
<p class="diagram-caption">Guardrails are layered: screen the input, the output, and the action before any real-world sink.</p>

> Never route raw output into a consequential sink (DB/shell/email/pay) without
> validation proportional to the cost of being wrong.

---

## Cost & latency engineering

- **Model routing / cascade** — cheap model for easy, frontier for hard (biggest lever)

```svg
<svg viewBox="0 0 560 180" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <rect x="30" y="70" width="90" height="44" rx="8" fill="#eef4ff" stroke="#b9c4da"/><text x="75" y="97" text-anchor="middle" font-size="13">request</text>
  <path d="M120 92 H180" stroke="#333" stroke-width="2" marker-end="url(#cc)"/>
  <polygon points="180,70 240,92 180,114 120,92" fill="#f0a500"/><text x="188" y="96" text-anchor="middle" font-size="11" fill="#fff">easy?</text>
  <!-- yes -> cheap model -->
  <path d="M240 92 H320" stroke="#2a7d5f" stroke-width="2.5" marker-end="url(#cg)"/><text x="280" y="84" text-anchor="middle" font-size="11" fill="#2a7d5f">yes</text>
  <rect x="320" y="60" width="130" height="30" rx="6" fill="#2a7d5f"/><text x="385" y="80" text-anchor="middle" font-size="12" fill="#fff">cheap model ($)</text>
  <!-- no -> frontier -->
  <path d="M210 110 V150 H320" stroke="#c0392b" stroke-width="2.5" marker-end="url(#cr)"/><text x="250" y="145" text-anchor="middle" font-size="11" fill="#c0392b">hard</text>
  <rect x="320" y="135" width="130" height="30" rx="6" fill="#c0392b"/><text x="385" y="155" text-anchor="middle" font-size="12" fill="#fff">frontier model ($$$)</text>
  <text x="280" y="28" text-anchor="middle" font-size="13" font-weight="bold" fill="#1f2a44">Cascade: route by difficulty — the biggest cost lever</text>
  <defs>
    <marker id="cc" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#333"/></marker>
    <marker id="cg" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#2a7d5f"/></marker>
    <marker id="cr" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#c0392b"/></marker>
  </defs>
</svg>
```
<p class="diagram-caption">Send easy requests to a cheap model, escalate only the hard ones — most traffic never needs the frontier.</p>
- **Context economy** — trim chunks, summarize history, compress prompts
- **Caching** — response (exact+semantic), embeddings, prompt/KV
- **Streaming** — collapse *perceived* latency
- **`max_tokens`**, batching, async

Instrument **cost + latency per request from day one.**

---

## LLM security surface (OWASP LLM Top 10)

- **Prompt injection (direct & indirect)** — untrusted input *and* ingested
  content (RAG/tools/pages); no prompt fully prevents it
- **Insecure output handling** — output → SQL/shell/HTML/code = injection
- **Sensitive-info disclosure** — secrets in prompts, PII in logs
- **Excessive agency** — over-scoped tools
- **Supply chain** — model/data/plugin provenance
- **Unbounded consumption** — denial-of-wallet → rate-limit & cap

---

## Bias · privacy · governance

- **Bias** — test disparate outcomes for consequential decisions; human-in-loop; document intended use
- **Privacy** — data residency/egress, minimization, consent, GDPR/HIPAA; prompts & outputs can be regulated data
- **Transparency/accountability** — disclose AI + fallibility; keep audit trails that explain a decision

Often legal requirements, not nice-to-haves.

---

## Production readiness checklist

- [ ] Eval suite that **gates** every change + online sampling
- [ ] Layered guardrails (input/output/action) + fallbacks
- [ ] Output validation before any consequential sink
- [ ] Cost/latency instrumented; routing, caching, `max_tokens`
- [ ] Injection defenses; ingested content = untrusted
- [ ] Secrets/PII out of prompts & logs
- [ ] Least-privilege tools; approval for irreversible actions
- [ ] Full traces; pinned model/prompt/index versions
- [ ] Bias/privacy/governance per domain

---

## Course wrap

A foundation model is a **powerful, probabilistic, untrusted component**.
The engineering is the **system around it** — context, retrieval, control,
evaluation, safety.

> That system is where you add value — and what senior AI roles hire for.

**Lab:** build the guardrail suite + golden-set eval → "works" & "safe" as numbers.
