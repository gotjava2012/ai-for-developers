# Module 6 — Building Real, Responsible AI Apps · Script

*Runtime: ~9–11 min. [brackets] map to slides.md.*

---

[Slide: title]

Here's the truth that separates a weekend demo from a product: the cool part is
easy, and the responsible part is the real engineering. In this final module we
cover the five things that turn an LLM demo into something you can actually ship
to real users — knowing if it works, keeping it safe, controlling cost, handling
security, and dealing with bias and privacy.

---

[Slide: evals]

Start with the most overlooked one: evals. With normal code you write a test —
input X, assert output Y. But LLMs are non-deterministic; the same prompt can
give different wording every time, so exact-match assertions mostly don't work.
Instead you measure *quality*, repeatably.

The simplest and most valuable tool is a golden set — a fixed collection of
inputs with known-good expected outputs or properties that you score against.
Add rule-based assertion checks: is it valid JSON, does it have the required
fields, does it cite a source. You can do similarity or keyword checks for
whether the key facts are present. You can use another model as a judge, though
you have to validate the judge. And for high-stakes work, nothing beats human
review of a sample.

The mantra: if you can't measure quality, you can't improve it, and you can't
safely change your prompt or swap your model. Build a small eval set early —
even twenty examples beats going on vibes.

---

[Slide: guardrails]

Next, guardrails — the checks that keep the model inside safe, valid bounds.
Input guardrails run before the model: catch prompt-injection attempts, strip
PII you don't want sent, reject off-topic or abusive input. Output guardrails run
before you use the response: validate the schema — is it actually valid JSON —
filter forbidden content, enforce "must cite a source," cap the length, check
that it's grounded. And always have a fallback: when a guardrail trips, return a
safe default, ask again, or escalate to a human.

The rule to tattoo on your brain: never pipe raw LLM output directly into
something consequential — a database write, an email, a shell command — without
validating it first.

---

[Slide: cost & latency]

Now the part that surprises people in production: cost and latency. You pay per
token, input and output, and users feel every second of delay. Your levers:
route by difficulty — use a small cheap model for easy tasks and save the big
expensive one for the hard ones. Trim your prompts and context; shorter is
cheaper. Cache repeated queries and embeddings. Stream tokens so the user sees
output immediately, which hugely improves perceived speed. Always set a max
tokens cap so a runaway response can't blow up your bill. Track cost per request
from day one — a feature that's delightful in a demo can be financially
impossible at scale.

---

[Slide: security]

Security. On top of all your normal app security, LLMs add new attack surface.
The headline risk is prompt injection: untrusted content — user input, a web
page you fetched, a document you retrieved — contains hidden instructions that
hijack the model. The mitigation is to treat all external content as untrusted
data, keep instructions separate from data, and never give the model more
authority or tool access than it needs.

Then: sensitive data leakage — keep secrets out of prompts, redact PII, and be
careful what you log, because prompts and outputs can contain sensitive data.
Insecure output handling — if model output flows into SQL, a shell, HTML, or
code, it can carry injection, so validate and escape it like any untrusted
input. And excessive agency — an agent with broad permissions has a huge blast
radius, so least privilege and human approval for risky actions, straight from
Module 5. If you want a map of all this, look up the OWASP Top 10 for LLM
Applications.

---

[Slide: bias, fairness, privacy]

Bias, fairness, and privacy — not optional extras. Models reflect the biases in
their training data, so if your app touches people's lives — hiring, lending,
moderation — you must test for disparate outcomes and keep a human in the loop
for consequential decisions. Privacy: know where your data goes; a hosted API
means data leaves your environment, so minimize what you send, honor consent,
and comply with regulations like GDPR. And be transparent — tell users when
they're talking to AI and that its output can be wrong. In many domains these
are legal requirements, not courtesies.

---

[Slide: checklist]

So here's your shipping checklist, the thing to actually run down before an AI
feature meets real users: a golden eval set you run on every change; output
validation before use; input and output guardrails; cost tracked with max tokens
and cheap-model routing; no secrets in prompts or logs and PII handled;
least-privilege tools with human approval for irreversible actions; fallbacks for
failures; and transparency to users. Tape that to your monitor.

---

[Slide: lab + wrap]

In the final lab you'll add a guardrail and a tiny eval harness to some LLM
output, and watch "does it work" and "is it safe" turn from vibes into numbers
you can track.

And that's the course. You started not knowing what AI really was, and you've
walked all the way through how models learn, how LLMs work, grounding them with
RAG, fine-tuning, building agents with tools, and shipping responsibly. You're
no longer new to AI — you're a developer who can build with it. The course README
has your next steps. Go build something.
