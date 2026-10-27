# Module 6 — Production & Responsible AI Engineering

> **Goal:** The discipline that separates a demo from a system real users and
> auditors can trust: rigorous evaluation, layered guardrails, cost/latency
> engineering, the LLM-specific security surface, and governance. This is where
> most of the actual engineering lives.

---

## 6.1 Evaluation — the hardest and most-skipped discipline

LLM outputs are non-deterministic and open-ended, so exact-match assertions
don't apply. You need an **evaluation system**: a repeatable, quantitative
measure of quality that gates changes.

### Build it in layers
- **Golden/reference sets** — curated inputs with known-good outputs or checkable
  properties. Your regression suite. Start small (dozens), grow from production
  failures.
- **Programmatic checks** — deterministic assertions: schema/format validity,
  required fields, must-cite-source, forbidden content, numeric tolerances. Cheap,
  fast, run on every change.
- **Reference-based metrics** — for tasks with ground truth: exact match, F1,
  or embedding similarity for semantic closeness.
- **LLM-as-judge** — a model scores outputs against a rubric. Scales to
  open-ended quality but has real pitfalls: position/verbosity/self-preference
  bias, and it's itself nondeterministic. **Validate the judge against human
  labels** before trusting it; pin and version the judge prompt.
- **Human evaluation** — the ground truth for high-stakes; sample and grade,
  feed disagreements back into the golden set.

### Offline vs. online
Offline evals gate deploys (CI for quality). **Online** evaluation — A/B tests,
user signals, production trace sampling — catches what offline sets miss, because
real input distribution always drifts from your fixtures.

> The operative question for any reported number: *which dataset, which metric,
> and does it gate releases?* If quality isn't measured and gated, every prompt
> or model change is an unmonitored production change.

---

## 6.2 Guardrails — a layered control architecture

Guardrails are deterministic (and sometimes model-based) controls around the
nondeterministic core. Layer them:

- **Input guardrails** — before the model: injection detection, PII
  detection/redaction, topic/abuse filtering, input-size limits.
- **Output guardrails** — before *use*: schema/type validation, grounding/
  faithfulness checks (does the answer trace to the retrieved context?),
  toxicity/PII filters, policy checks.
- **Action guardrails** — before side effects: authorization, allow-lists,
  confirmation/human-in-the-loop for irreversible or costly actions, spend caps.
- **Fallbacks** — defined safe behavior when a guardrail trips: retry, degrade,
  refuse, or escalate. A tripped guardrail with no fallback is an outage.

Principle: **never route raw model output into a consequential sink** (DB, shell,
email, code exec, payment) without validation proportional to the cost of being
wrong. Guardrails are defense-in-depth, not a single check.

---

## 6.3 Cost & latency engineering

Token-metered, latency-sensitive systems need deliberate engineering, not just
"call the biggest model."

- **Model routing / cascades** — classify difficulty; serve easy traffic with a
  small/cheap model, escalate only hard cases to a frontier model. Often the
  largest single cost lever.
- **Context economy** — retrieved-chunk trimming, history summarization, prompt
  compression. Input tokens are usually the bulk of cost in RAG. (A gateway-level
  response compressor/token router is this idea operationalized.)
- **Caching** — exact and semantic caching of responses; cache embeddings;
  prompt/KV caching where the provider supports it.
- **Streaming** — stream tokens to collapse *perceived* latency even when total
  latency is unchanged.
- **Output bounds** — `max_tokens`; output tokens are generated serially and often
  priced higher.
- **Batching & async** — amortize and parallelize independent calls.

Instrument **cost and latency per request from day one**; a demo-stage prompt can
be economically nonviable at scale, and you want that visible before launch.

---

## 6.4 The LLM security surface (OWASP LLM Top 10, in practice)

Beyond conventional app security, treat these as first-class:

- **Prompt injection (direct & indirect)** — the signature LLM vuln. Untrusted
  content — user input *or* anything the model ingests (retrieved docs, web
  pages, tool output, file contents) — can carry instructions that hijack
  behavior. No prompt fully prevents it. Defenses: separate instructions from
  data, least-privilege tool access, output validation, and never let model
  output alone authorize a consequential action. (Indirect injection via
  RAG/agent-fetched content is the underrated case.)
- **Insecure output handling** — model output flowing unescaped into SQL, shell,
  HTML, or code is an injection vector. Treat it as untrusted input to the sink.
- **Sensitive-information disclosure** — secrets in prompts, PII in logs/traces,
  training/context data leakage. Redact at the boundary; be deliberate about what
  you log.
- **Excessive agency** — over-scoped tools/permissions (Module 5). Constrain and
  gate.
- **Supply chain & model risks** — provenance of models/weights/datasets;
  poisoned data; dependency and plugin trust.
- **Unbounded consumption** — token/cost exhaustion as a denial-of-wallet attack;
  rate-limit and cap.

---

## 6.5 Bias, fairness, privacy, governance

- **Bias** — models inherit training-data bias. For consequential decisions
  (hiring, lending, moderation, health), test for disparate outcomes across
  groups, keep humans in the loop, and document the model's intended use and
  limits.
- **Privacy & compliance** — know data residency and egress (hosted API =
  data leaves your boundary), minimize collection, honor consent and retention,
  meet applicable regimes (GDPR, HIPAA, etc.). Prompts and outputs can both be
  regulated data.
- **Transparency & accountability** — disclose AI involvement and fallibility;
  maintain audit trails of inputs, outputs, and actions sufficient to explain a
  decision after the fact. In regulated contexts this is a requirement, not a
  nicety.

---

## 6.6 Production readiness checklist

- [ ] **Eval suite** (golden set + programmatic checks) that **gates** every
      prompt/model/retrieval change; online eval + trace sampling in prod
- [ ] **Layered guardrails** (input / output / action) with defined **fallbacks**
- [ ] **Output validation** before any consequential sink
- [ ] **Cost & latency** instrumented per request; routing, caching, `max_tokens`
- [ ] **Injection defenses**; all ingested content treated as untrusted
- [ ] **Secrets/PII** kept out of prompts and logs; redaction at boundaries
- [ ] **Least-privilege tools**; human approval for irreversible/high-cost actions
- [ ] **Observability**: full traces (prompt, retrieval, tool calls, output, cost)
- [ ] **Versioning**: pin model + prompt + index versions; changes are releases
- [ ] **Bias/privacy/governance** controls appropriate to the domain

---

## Terms, at working precision
- **Golden set / regression gate** — fixtures that block quality regressions in CI.
- **LLM-as-judge** — model-scored eval; must be validated against humans; biased.
- **Online vs offline eval** — production signals vs pre-deploy fixtures.
- **Model routing / cascade** — difficulty-based cheap→frontier escalation.
- **Indirect prompt injection** — hostile instructions in content the model ingests (RAG/tools).
- **Denial-of-wallet** — cost-exhaustion attack via unbounded consumption.

## Check yourself
1. Why are exact-match tests insufficient, and what does an eval system use instead?
2. Name a concrete pitfall of LLM-as-judge and how you'd mitigate it.
3. Why is *indirect* prompt injection often more dangerous than direct?
4. Give the largest single cost lever for a high-volume LLM feature and why.
5. Walk the path of a model output to a consequential sink and place the guardrails.

➡️ **Lab:** implement a programmatic guardrail suite and a golden-set eval
harness; produce a gating score and watch injection/secret/format violations get
blocked — "works" and "safe" as numbers, not vibes.

---

## Course wrap

You've gone from *AI as a learned function* through optimization, LLM mechanics,
grounding and customization, agentic orchestration, and production discipline.
The through-line: a foundation model is a powerful, probabilistic, untrusted
component, and the engineering is the **system you build around it** — context,
retrieval, control, evaluation, and safety. That system is where you add value,
and it's exactly what senior AI roles are hiring for. Next steps are in the
course `README.md`.
