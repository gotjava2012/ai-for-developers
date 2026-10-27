# Module 6 — Building Real, Responsible AI Apps

> **Goal:** Turn a demo into something you can actually ship: know if it works
> (evals), keep it safe (guardrails), control cost and latency, handle security,
> and address bias and privacy.

A cool prototype is easy. A *trustworthy* AI feature is the real engineering —
and it's mostly the stuff this module covers.

---

## 6.1 Evals — how do you know it even works?

With normal code, you write tests: input X → assert output Y. LLMs are
non-deterministic, so "assert exact output" usually doesn't apply. You need
**evals**: a repeatable way to measure output *quality*.

Approaches, simplest first:
- **Golden set** — a fixed set of inputs with known-good expected outputs/
  properties; run your system against them and score.
- **Rule/assertion checks** — does the output contain the required fields? Valid
  JSON? Mention a source? Avoid forbidden content?
- **Similarity / keyword checks** — does the answer contain the key facts?
- **LLM-as-judge** — use another model to score answers against criteria (useful,
  but validate the judge).
- **Human review** — the gold standard for high-stakes; sample and grade.

> If you can't measure quality, you can't improve it or safely change the
> prompt/model. Build a small eval set *early* — even 20 examples beats vibes.

---

## 6.2 Guardrails — constraining inputs and outputs

Guardrails are checks around the model that keep it inside safe, valid bounds:

- **Input guardrails** — block/clean prompts before they hit the model:
  prompt-injection attempts, PII you don't want sent, off-topic/abuse.
- **Output guardrails** — validate before you use/show the response: schema
  validation (is it valid JSON?), forbidden-content filters, "must cite a
  source," max length, groundedness checks.
- **Fallbacks** — when a guardrail trips, have a safe default (ask again, return
  "I can't help with that," escalate to a human).

Rule of thumb: **never pipe raw LLM output directly into something consequential**
(a database write, an email, a shell command) without validating it first.

---

## 6.3 Cost & latency — the part that surprises people

You pay per token (input + output) and users feel every second of latency.
Levers:

- **Smaller/cheaper models** for easy tasks; reserve the big expensive model for
  hard ones (route by difficulty).
- **Shorter prompts & context** — trim retrieved chunks, summarize history.
  (That MCP gateway's "token router" that compresses responses is this idea.)
- **Caching** — cache repeated queries/embeddings.
- **Streaming** — stream tokens so the user sees output immediately (better
  perceived latency).
- **Set `max_tokens`** — cap runaway (and costly) outputs.
- **Batch** where possible.

> Track cost per request from day one. A feature that's great in a demo can be
> unaffordable at scale.

---

## 6.4 Security — the AI-specific risks

On top of normal app security, LLM apps add new attack surface:

- **Prompt injection** — untrusted content (user input, a fetched web page, a
  retrieved doc) contains instructions that hijack the model. *Mitigation:* treat
  all external content as untrusted data, separate instructions from data,
  constrain what tools/actions are possible, don't give the model more authority
  than needed.
- **Sensitive data leakage** — don't put secrets in prompts; redact PII; be
  careful what you log (prompts/outputs can contain sensitive data).
- **Insecure output handling** — model output used in SQL, shell, HTML, or code
  can carry injection. Validate/escape it like any untrusted input.
- **Excessive agency** — an agent with broad permissions is a big blast radius;
  least privilege + human approval for risky actions (Module 5).

(These map to the OWASP Top 10 for LLM Applications — worth a read.)

---

## 6.5 Bias, fairness & privacy

- **Bias** — models reflect biases in their training data. If your app affects
  people (hiring, lending, moderation), test for disparate outcomes and keep a
  human in the loop for consequential decisions.
- **Privacy** — know where data goes (hosted API = data leaves your
  environment), honor consent, minimize what you collect/send, comply with
  regulations (GDPR, etc.).
- **Transparency** — tell users when they're interacting with AI and when output
  may be wrong.

These aren't "nice to have" — for many domains they're legal requirements and
reputational necessities.

---

## 6.6 A shipping checklist

Before an AI feature goes to real users:
- [ ] A **golden eval set** you run on every prompt/model change
- [ ] **Output validation** (schema/format) before use
- [ ] **Input/output guardrails** for safety and injection
- [ ] **Cost tracked** per request; `max_tokens` set; cheap-model routing where possible
- [ ] **No secrets in prompts/logs**; PII handled
- [ ] **Least-privilege** tools; human approval for irreversible actions
- [ ] **Fallbacks** for failures/timeouts/guardrail trips
- [ ] **Transparency** to users about AI involvement and limits

---

## Key terms
- **Eval** — repeatable measurement of output quality.
- **Golden set** — fixed inputs with known-good expected results.
- **Guardrail** — input/output check keeping the model in safe bounds.
- **Prompt injection** — hostile instructions hidden in untrusted content.
- **Least privilege / excessive agency** — limit what tools/actions are possible.

## Check yourself
1. Why can't you test an LLM feature with normal exact-match assertions? What do
   you use instead?
2. Give one input guardrail and one output guardrail.
3. Name three levers to cut LLM cost.
4. What is prompt injection, and what's the core mitigation?
5. List three items you'd require before shipping an AI feature.

➡️ **Do the `lab/`** — add a guardrail and a tiny eval harness to an LLM output,
and see "does it work / is it safe" become measurable.
