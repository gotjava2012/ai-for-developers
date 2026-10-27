---
marp: true
theme: default
paginate: true
header: "AI for Developers · Module 3 — LLMs for Developers"
---

# Module 3
## LLMs for Developers

What an LLM really does — and your first call from code.

---

## What an LLM actually does

> Given some text, **predict the next token.**

- A **token** ≈ ¾ of a word
- Output a probability for every possible next token → pick one → repeat
- Whole paragraphs = next-token prediction, over and over

It is **not** looking things up. It's generating likely continuations.

---

## The knobs you'll touch

- **Context window** — max tokens it can see (prompt + output)
- **Temperature** — randomness (0 = focused, high = creative)
- **Max tokens** — output length cap
- **System prompt** — sets role & rules (your main lever)
- **Stop sequences** — halt generation

💸 You pay per token — **input and output**. Token-awareness = a core skill.

---

## Prompting is engineering

1. **System prompt** sets role + rules
2. Be **specific about format** (JSON? list? show an example)
3. Give **examples** (few-shot) — often beats instructions
4. Put instruction first; **delimit** the data clearly
5. "Think step by step" for reasoning tasks

Vague prompt → vague output. Specificity is the game.

---

## Hallucination

LLMs generate *plausible* text, not *retrieved true* text.
→ They state false things **confidently**.

Not fully fixable — **manage** it:
- Ground with real data (**RAG**, Module 4)
- Ask for sources & verify
- Lower temperature for facts
- Never auto-trust output

> #1 beginner mistake: assuming the output is true.

---

## Local vs. hosted

- **Hosted API** (OpenAI/Anthropic) — easiest, most capable, pay-per-token
- **Local** (Ollama) — free, private, offline, smaller models
- **Open-weight** (Llama/Qwen) — download, run, or fine-tune

Labs default to **Ollama** (free/offline) — same code pattern as an API.

---

## Lab

1. Make your **first LLM call** from code (Ollama or an API)
2. Change **temperature** — watch output vary
3. Improve a **prompt** and compare results
4. **Trigger a hallucination** on purpose

**Next:** Module 4 — Giving an LLM Your Own Data (RAG & fine-tuning)
