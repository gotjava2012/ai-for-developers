# Module 6 Lab — Guardrails + Evals (hands-on)

Make "does it work?" and "is it safe?" measurable instead of vibes. Pure Python,
no model needed — the script feeds in sample outputs so the mechanics are clear
and repeatable. In a real app these same functions wrap your actual LLM calls.

## Run it
```bash
python3 guardrails_and_evals.py
```

---

## Part A — Evals: score outputs against a golden set
The script scores three sample outputs against a **golden set** (inputs with
expected properties). You'll see something like:
```
[PASS] defines inference as JSON
[PASS] cites a source
[FAIL] BAD: not json
SCORE: 2/3 (67%)
```
**That score is the number you track every time you change a prompt or model.**
If a change drops it from 90% to 70%, you caught a regression — exactly like a
test suite, but for quality.

---

## Part B — Guardrails: allow the good, block the bad
The script runs four cases through input + output guardrails and shows
ALLOW/BLOCK with reasons:
- ✅ clean question + valid JSON → **ALLOW**
- 🚫 "ignore previous instructions…" → **BLOCK** (prompt injection caught)
- 🚫 output containing `sk-...` → **BLOCK** (secret leak caught)
- 🚫 plain text where JSON was required → **BLOCK** (schema check)

Open `guardrails_and_evals.py` and read the three guardrail functions. Notice
they're just ordinary validation — the "AI safety" here is mostly disciplined
input/output checking.

---

## Exercises
1. **Add an eval example** to `GOLDEN_SET` that your current checks would fail,
   then fix the output so it passes. Watch the score change.
2. **Add a guardrail**: reject output longer than 500 characters (a `max_length`
   guardrail). Wire it into `apply_guardrails`.
3. **Add an input guardrail** that blocks a basic PII pattern (e.g. a
   `\d{3}-\d{2}-\d{4}` SSN shape) so it never reaches the model.
4. **Groundedness check (harder):** given a RAG answer and its retrieved context,
   write a check that the answer's key terms appear in the context.

---

## Tie it together
Combine with earlier modules for a real mini-app:
- **RAG** (Module 4) grounds the answer in your data,
- **this lab's guardrails** validate the output before you use it,
- **this lab's eval set** tells you whether a change made things better or worse.

That trio — grounding, guardrails, evals — is the backbone of a trustworthy LLM
feature.

## Takeaway
Shipping AI responsibly isn't exotic — it's evals so you know it works, and
guardrails so it stays safe, both turned into repeatable, measurable checks.

🎓 **Course complete.** See the course `README.md` for next steps and further
learning.
