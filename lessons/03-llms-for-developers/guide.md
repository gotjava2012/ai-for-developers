# Module 3 — LLMs for Developers

> **Goal:** Understand what an LLM actually does, the knobs you'll touch
> (tokens, context, temperature), how to prompt well, and why LLMs hallucinate —
> then make your first LLM call from code.

---

## 3.1 What an LLM actually does

A Large Language Model does exactly one thing at its core:

> **Given some text, predict the next token.**

A **token** is a chunk of text — roughly ¾ of a word on average (e.g. "developer"
might be one token; "tokenization" might be two or three). The model outputs a
probability for every possible next token, picks one, appends it, and repeats.
That's how it writes whole paragraphs: next-token prediction, over and over.

Everything impressive an LLM does — answering, coding, summarizing — emerges from
that one mechanism at massive scale. It is **not** looking things up in a
database. It is generating statistically likely continuations.

That single fact explains most LLM behavior, including the weird parts.

---

## 3.2 The knobs you'll actually touch

| Knob | What it does | Practical advice |
|------|--------------|------------------|
| **Context window** | Max tokens the model can "see" at once (prompt + output) | Everything — your instructions, the user input, retrieved docs, the reply — must fit. Larger = more room, more cost. |
| **Temperature** | Randomness of the output (0 = deterministic-ish, higher = more varied/creative) | Low (0–0.3) for factual/structured tasks; higher (0.7–1.0) for brainstorming/creative. |
| **Max tokens** | Cap on output length | Controls cost and prevents runaway responses. |
| **System prompt** | A top-level instruction that sets role/behavior | Your main lever for steering the model. |
| **Stop sequences** | Strings that halt generation | Useful for structured output. |

**Cost note:** you pay per token — *both* input and output. A long prompt with
big retrieved documents costs real money on every call. Token-awareness is a
core engineering skill (Module 6).

---

## 3.3 Prompting is engineering, not magic

A prompt is your API to the model. Treat it with the same rigor as any input.
Patterns that reliably work:

1. **Use a system prompt to set role and rules.**
   *"You are a precise assistant. Answer only from the provided context. If
   unknown, say 'I don't know.'"*
2. **Be specific about format.** Ask for JSON, a list, a table — and show an
   example of the shape you want.
3. **Give examples (few-shot).** Showing 2–3 input→output examples often beats
   a paragraph of instructions.
4. **Put the instruction first and the data clearly delimited.** e.g. wrap user
   content in triple backticks or XML-ish tags so the model doesn't confuse
   instructions with data.
5. **Ask it to think step by step** for reasoning tasks (it improves multi-step
   answers).

**Anti-pattern:** vague prompts ("make this better") → vague, inconsistent
output. Specificity is the whole game.

---

## 3.4 Hallucination — the thing you must design around

Because an LLM generates *plausible* text rather than *retrieving true* text, it
will sometimes produce confident, fluent, completely false statements. Fake
citations, invented APIs, wrong dates — stated with total confidence.

This is not a bug you can fully "fix" — it's inherent to how LLMs work. You
**manage** it:

- **Ground it with real data** (RAG — Module 4): give the model the facts and
  tell it to answer only from them.
- **Ask for sources** and verify them.
- **Lower temperature** for factual tasks.
- **Never auto-trust** output for anything consequential without a check.
- **Add evals and guardrails** (Module 6).

> The #1 beginner mistake: shipping an LLM feature that assumes the output is
> true. Design as if it sometimes lies — because it does.

---

## 3.5 Open vs. hosted, local vs. API

- **Hosted APIs** (OpenAI, Anthropic, Google) — easiest, most capable, pay per
  token, data leaves your machine. Best for most apps.
- **Local models** (via **Ollama**, etc.) — free, private, offline, run on your
  hardware; smaller/less capable but great for learning, prototyping, and
  privacy-sensitive work.
- **Open-weight models** (Llama, Qwen, Mistral) — you can download and run or
  fine-tune them (Module 4).

For this course's labs we default to **Ollama** so everything is free and
offline, but the code pattern is identical for a hosted API.

---

## Key terms
- **Token** — a chunk of text (~¾ word); models read/write in tokens.
- **Context window** — max tokens the model can consider at once.
- **Temperature** — output randomness knob.
- **System prompt** — top-level instruction setting behavior.
- **Few-shot** — giving examples in the prompt.
- **Hallucination** — confident, fluent, false output.

## Check yourself
1. In one sentence, what does an LLM fundamentally do?
2. You need consistent, structured JSON output. What temperature range, and
   what prompting technique?
3. Why do LLMs hallucinate, and what's the main way to reduce it?
4. When would you choose a local model over a hosted API?

➡️ **Do the `lab/`** — make your first LLM call, experiment with temperature and
prompts, and trigger a hallucination on purpose so you never forget it's possible.
