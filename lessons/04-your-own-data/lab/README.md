# Module 4 Lab — Build a RAG System (hands-on)

Give an LLM your own data and watch it answer from facts (with citations) — then
watch it refuse to hallucinate when the answer isn't there.

## Setup
```bash
git clone https://github.com/gotjava2012/rag-from-scratch.git
cd rag-from-scratch
# Prereqs: Python 3 + Ollama
ollama pull nomic-embed-text    # embedding model
ollama pull llama3.2:1b         # generation model
```

---

## Part A — Index your documents
```bash
python3 src/rag.py index
```
This runs the **indexing phase** from the guide: it chunks the docs in
`sample_docs/`, embeds each chunk, and saves the vectors. Watch the output —
it tells you how many chunks each file produced.

Map it to the guide: **chunk → embed → store.** Done once.

---

## Part B — Ask a grounded question
```bash
python3 src/rag.py ask "What is cosine similarity and why is it used in RAG?"
```
Look at the output in two parts:
1. **RETRIEVED CONTEXT** — the exact chunks the system pulled, with similarity
   scores. This is the retrieve step; you can *see* what the model was given.
2. **ANSWER** — grounded in those chunks, citing the source.

That transparency — showing the retrieved evidence — is a core advantage of RAG.

---

## Part C — Prove it won't hallucinate
Ask something that's NOT in the documents:
```bash
python3 src/rag.py ask "What is the capital of France?"
```
A good RAG system answers **"I don't know based on the provided documents."**
Compare that to Module 3, where the bare LLM happily made things up. *That's* the
whole point of grounding.

---

## Part D — Make it YOUR data
Drop your own `.txt` or `.md` files into `sample_docs/` (project notes, docs,
anything), then re-index and ask about them:
```bash
# add your files to sample_docs/
python3 src/rag.py index
python3 src/rag.py ask "a question about your own documents"
```
You now have a Q&A bot over your own knowledge base.

---

## Part E (optional, GPU/Colab) — Fine-tuning with LoRA
If you want to feel fine-tuning (vs. RAG):
```bash
git clone https://github.com/gotjava2012/llm-lora-finetune.git
```
Follow its `docs/TUTORIAL.md` — it includes a **Google Colab recipe** (free GPU),
since fine-tuning needs a GPU. You'll freeze a base model, train a tiny LoRA
adapter, and generate text in the fine-tuned style.

---

## Exercises
1. In Part B, open `src/rag.py` and change the chunk size, then re-index. How do
   the retrieved chunks change? Does the answer quality change?
2. Change `k` (number of retrieved chunks). Is more context always better?
3. Decide for each: **RAG or fine-tuning?**
   - "Answer support questions from our help center (updated weekly)"
   - "Always reply in our company's formal brand voice"
   - "Summarize today's internal standup notes"

## Takeaway
You built a retrieval system that grounds an LLM in your data, cites its
sources, and declines when it doesn't know. This is the backbone of most
real-world LLM applications.

➡️ **Next:** Module 5 — Agents & Tool-Calling (let the model *act*).
