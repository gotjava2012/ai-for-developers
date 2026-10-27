# Module 4 — Giving an LLM Your Own Data

> **Goal:** Learn the two ways to make a general LLM work with *your* specific
> data — **RAG** (retrieval) and **fine-tuning** — when to use each, and build a
> working RAG system.

A base LLM knows nothing about your company's docs, your codebase, or anything
after its training cutoff. Two techniques fix that. Choosing the right one is a
key architectural decision.

---

## 4.1 The problem

You ask an LLM about your internal product and it either says it doesn't know,
or worse, hallucinates a confident wrong answer (Module 3). The model simply
never saw your data. Two solutions:

- **RAG** — *retrieve* relevant data at query time and put it in the prompt.
- **Fine-tuning** — *further-train* the model so the behavior/knowledge is baked
  into its weights.

They solve different problems and are often used together.

---

## 4.2 RAG — Retrieval-Augmented Generation

**Idea:** don't change the model — change its *input*. At query time, find the
most relevant chunks of your data and hand them to the model as context, with an
instruction to answer only from them.

### The pipeline (two phases)
**Indexing (once, ahead of time):**
1. **Chunk** your documents into passages.
2. **Embed** each chunk — turn it into a vector that captures meaning.
3. **Store** the vectors in a vector index/database.

**Query (every question):**
4. **Embed the question** the same way.
5. **Retrieve** the chunks whose vectors are most similar (cosine similarity).
6. **Augment** the prompt with those chunks.
7. **Generate** an answer grounded in them.

```
docs → chunk → embed → store        (indexing, once)
question → embed → retrieve top-k → stuff into prompt → LLM → answer   (per query)
```

### Why RAG is usually your first choice
- **Facts stay current** — update the documents, no retraining.
- **Cites sources** — you can show *where* the answer came from.
- **Cheaper & faster** to build than fine-tuning.
- **Reduces hallucination** — the model answers from supplied facts.

You build exactly this in the lab (`rag-from-scratch`).

---

## 4.3 Fine-tuning

**Idea:** actually train the model further on your examples so new behavior or
style is baked into its parameters.

- Best for teaching **style, tone, format, or a specialized task** — not for
  injecting changing facts.
- Needs a dataset of examples (often hundreds to thousands).
- Costs compute (a GPU) and must be redone when your data changes.

### LoRA — fine-tuning without a data center
Full fine-tuning updates *all* of a model's (billions of) weights — too much for
most people. **LoRA** (Low-Rank Adaptation) **freezes** the base model and trains
tiny "adapter" matrices — often <1% of the parameters. Results are close to full
fine-tuning, but it fits on a single free GPU and the saved adapter is a few MB.
You run a LoRA fine-tune in the (optional) lab (`llm-lora-finetune`).

---

## 4.4 RAG vs. fine-tuning — how to choose

| Use **RAG** when… | Use **fine-tuning** when… |
|---|---|
| You need **facts/knowledge** (docs, policies, data) | You need a **style, tone, or format** |
| The data **changes often** | The behavior is **stable** |
| You must **cite sources** | Sources don't matter |
| You want to ship **fast and cheap** | You've already maxed out prompting + RAG |
| (most apps start here) | (a later optimization) |

**Rule of thumb:** *RAG for what the model should* ***know***, *fine-tuning for
how it should* ***behave***. They combine well — fine-tune the style, RAG the
facts.

> Start with good prompting. If it needs your data, add RAG. Only reach for
> fine-tuning when prompting + RAG aren't enough. Most teams never need to
> fine-tune.

---

## 4.5 Embeddings & vector search (the engine under RAG)

An **embedding** turns text into a vector of numbers positioned so that similar
meanings are close together. Retrieval = "find the stored vectors nearest to the
question's vector," measured by **cosine similarity** (the angle between vectors).

- Small datasets: a simple in-memory index with exact cosine similarity (what
  the lab does — so you see the mechanics).
- Production: a **vector database** (Chroma, FAISS, Qdrant, pgvector, Pinecone)
  using Approximate Nearest Neighbor search for speed at scale.

---

## Key terms
- **RAG** — retrieve relevant data at query time, put it in the prompt.
- **Chunk / embed / retrieve** — the RAG pipeline steps.
- **Embedding** — a vector capturing text meaning.
- **Cosine similarity** — closeness measure for vectors.
- **Fine-tuning** — further-training to bake in behavior.
- **LoRA** — parameter-efficient fine-tuning (train tiny adapters).

## Check yourself
1. Which technique would you use to answer questions over your company's
   constantly-updated internal wiki? Why?
2. Which would you use to make a model always respond in your brand's voice?
3. What are the two phases of a RAG pipeline?
4. What does LoRA freeze, and what does it train?

➡️ **Do the `lab/`** — build a working RAG Q&A system over your own documents,
and optionally run a LoRA fine-tune.
