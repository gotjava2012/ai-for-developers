---
marp: true
theme: default
paginate: true
header: "AI for Developers · Module 4 — Giving an LLM Your Own Data"
---

# Module 4
## Giving an LLM Your Own Data

RAG vs. fine-tuning — and build a working RAG system.

---

## The problem

A base LLM knows nothing about:
- your company's docs
- your codebase
- anything after its training cutoff

Ask it anyway → "I don't know" or a **hallucination**.

Two fixes: **RAG** and **fine-tuning**.

---

## RAG — Retrieval-Augmented Generation

Don't change the model — change its **input**.

**Indexing (once):**
```
docs → chunk → embed → store in a vector index
```
**Query (every question):**
```
question → embed → retrieve top-k similar chunks
         → stuff into prompt → LLM → grounded answer
```

---

## Why RAG is usually first choice

- **Facts stay current** — just update the docs, no retraining
- **Cites sources** — show where the answer came from
- **Cheap & fast** to build
- **Reduces hallucination** — answers from supplied facts

You'll build this in the lab.

---

## Fine-tuning

Actually train the model further → behavior baked into weights.

- Best for **style, tone, format, specialized task**
- Needs a dataset (hundreds–thousands of examples) + a GPU
- Redo it when data changes

**LoRA:** freeze the base model, train tiny adapters (<1% of params).
Fits on a free GPU; adapter is a few MB.

---

## RAG vs. fine-tuning

| RAG when… | Fine-tune when… |
|---|---|
| need **facts/knowledge** | need **style/tone/format** |
| data **changes often** | behavior is **stable** |
| must **cite sources** | sources don't matter |
| ship fast & cheap | prompting + RAG maxed out |

> RAG for what it should **know**. Fine-tune for how it should **behave**.

---

## The engine: embeddings + vector search

- **Embedding** = text → vector; similar meaning → close vectors
- **Retrieval** = find nearest vectors (**cosine similarity**)
- Small data: in-memory exact search (the lab)
- Production: a **vector DB** (Chroma, FAISS, Qdrant, pgvector)

---

## Lab

1. Build a **RAG Q&A** over your own docs (`rag-from-scratch`)
2. Watch it retrieve, then answer with **citations**
3. Ask something not in the docs → it declines (no hallucination)
4. *Optional (Colab):* run a **LoRA fine-tune** (`llm-lora-finetune`)

**Next:** Module 5 — Agents & Tool-Calling
