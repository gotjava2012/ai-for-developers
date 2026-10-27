# AI for Developers — A Hands-On Course

A practical, no-fluff course for **developers who are new to AI**. If you can
write code, use a terminal, and call an API, you're ready. We skip the
"what is a variable" material and go straight to how AI actually works and how
to build with it.

By the end you will be able to:
- Explain how ML and LLMs work well enough to make good engineering decisions
- Call an LLM from code and prompt it effectively
- Give an LLM your own data with **RAG** and **fine-tuning**
- Build a simple **agent** that uses tools
- Ship AI features responsibly (evals, guardrails, cost, security)

## Format

Every module ships **four ways to learn the same material**, so you can read,
present, watch, or build:

| File | What it is |
|------|-----------|
| `guide.md` | The written guide — read this to learn |
| `slides.md` | A slide deck (Marp-compatible Markdown) to present/teach |
| `script.md` | A video/presentation narration script |
| `lab/` | Hands-on code and exercises |

## Modules

1. **Foundations** — AI vs ML vs deep learning vs generative AI; training vs inference
2. **How ML Actually Works** — data, models, loss, gradient descent (with runnable labs)
3. **LLMs for Developers** — tokens, context, prompting, hallucination; your first LLM call
4. **Giving an LLM Your Own Data** — RAG vs fine-tuning, and when to use each
5. **Agents & Tool-Calling** — LLM + tools + a loop; function calling and MCP
6. **Building Real, Responsible AI Apps** — evals, guardrails, cost, security, bias
7. **Decision Models: Trees & Ensembles** — decision trees, random forests, gradient boosting; the models that win on tabular data
8. **Reinforcement Learning: AI That Learns to Beat a Game** — MDPs, Q-learning, explore/exploit, deep RL (DQN→AlphaZero); the full process end to end

## Labs use real projects

The hands-on labs build on companion open-source projects (also in this
portfolio), so you learn by running real code, not toy snippets:
- `neural-net-from-scratch` · `ml-training-pipeline` · `rag-from-scratch`
- `pytorch-image-classifier` · `llm-lora-finetune`

## Prerequisites
- Comfortable writing code (examples are in Python, but the ideas are language-agnostic)
- Python 3, a terminal, and git
- Optional for some labs: an LLM API key, or [Ollama](https://ollama.com) for local/free models
- Optional for GPU labs: a free Google Colab account

## How to use this course
Work through the modules in order. In each, start with `guide.md`, do the
`lab/`, and use `slides.md` / `script.md` if you want to teach it to others.
