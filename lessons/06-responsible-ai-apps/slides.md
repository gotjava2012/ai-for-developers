---
marp: true
theme: default
paginate: true
header: "AI for Developers · Module 6 — Responsible AI Apps"
---

# Module 6
## Building Real, Responsible AI Apps

From cool demo → trustworthy, shippable feature.

---

## Evals — does it even work?

LLMs are non-deterministic → exact-match tests don't fit.
Measure **quality** instead:

- **Golden set** — fixed inputs + known-good expectations
- **Rule/assertion checks** — valid JSON? required fields? cites a source?
- **Similarity / keyword** — are the key facts present?
- **LLM-as-judge** — another model scores (validate it)
- **Human review** — gold standard for high-stakes

> Even 20 examples beats vibes. Build evals early.

---

## Guardrails — constrain in & out

- **Input** — block prompt injection, PII, off-topic/abuse
- **Output** — schema/JSON validation, forbidden-content filter, "must cite,"
  length, groundedness
- **Fallbacks** — safe default when a guardrail trips

> Never pipe raw LLM output into something consequential
> (DB write, email, shell) without validating it.

---

## Cost & latency

- **Route by difficulty** — cheap model for easy, big model for hard
- **Trim prompts/context** — shorter = cheaper
- **Cache** repeated queries/embeddings
- **Stream** tokens → better perceived latency
- **Set `max_tokens`** — cap runaway cost

> Track cost per request from day one.

---

## Security — AI-specific risks

- **Prompt injection** — hostile instructions in untrusted content
  → treat all external content as untrusted; separate instructions from data
- **Data leakage** — no secrets in prompts; redact PII; careful logging
- **Insecure output handling** — output in SQL/shell/HTML → validate & escape
- **Excessive agency** — least privilege + human approval

(≈ OWASP Top 10 for LLM apps)

---

## Bias, fairness & privacy

- **Bias** — models mirror training data; test disparate outcomes; human in the
  loop for consequential decisions
- **Privacy** — know where data goes; minimize; comply (GDPR…)
- **Transparency** — tell users it's AI and that it can be wrong

Often legal requirements, not nice-to-haves.

---

## Shipping checklist

- [ ] Golden eval set (run on every change)
- [ ] Output validation before use
- [ ] Input/output guardrails
- [ ] Cost tracked; `max_tokens`; cheap-model routing
- [ ] No secrets in prompts/logs; PII handled
- [ ] Least-privilege tools; human approval for risky actions
- [ ] Fallbacks for failures
- [ ] Transparency to users

---

## Lab + course wrap

**Lab:** add a guardrail + a tiny eval harness → make "works / safe" measurable.

🎓 You've gone from *what is AI* → building RAG, agents, and shipping
responsibly. **Next steps** in the course README.
