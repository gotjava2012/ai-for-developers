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

> Never route raw output into a consequential sink (DB/shell/email/pay) without
> validation proportional to the cost of being wrong.

---

## Cost & latency engineering

- **Model routing / cascade** — cheap model for easy, frontier for hard (biggest lever)
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
