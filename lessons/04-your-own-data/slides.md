---
marp: true
theme: default
paginate: true
header: "AI for Developers · Module 4 — Grounding & Customization"
---

# Module 4 — Grounding & Customization
### RAG vs. Fine-Tuning vs. Long-Context

The central architectural decision of applied LLM work.

---

## Three levers, different axes

- **RAG** — inject facts into context at inference. Changes the **input**.
- **Fine-tuning** — shift weights toward behavior/format. Changes the **model**.
- **Long-context** — more raw material in the window. Changes **how much input**.

> RAG & long-context inject **knowledge**. Fine-tuning instills
> **behavior/skill/format**. They compose.

---

## RAG *is* a search problem

```
offline:  chunk → embed → vector index
online:   embed query → top-k → (re-rank) → context → generate (answer-only-from-context)
```

Quality is dominated by **retrieval**, not generation.
Embeddings: semantic similarity ≈ geometric proximity (cosine).
Retrieval = **ANN** (HNSW/IVF): trade a little recall for sublinear latency.

---

## What actually determines RAG quality

- **Chunking** — semantic/structural boundaries > fixed sizes; overlap for straddling content
- **Embedding model** — domain match > raw size
- **Retrieval depth k** — ↑recall but ↑noise/cost; there's a peak
- **Metadata filtering** — pre-filter by source/date/permissions

Big vague chunks → diluted vectors, lost-in-middle. Tiny chunks → no context.

---

## Retrieval failure modes (where RAG breaks, silently)

- **Semantic mismatch** (question vs statement) → query rewrite / **HyDE**
- **Lexical gaps** (exact IDs/keywords) → **hybrid search** (vector + BM25)
- **Weak ranking** (right chunk, ranked low) → **cross-encoder re-ranker** (retrieve 50 → keep 5)
- **Boundary loss** (answer spans chunks) → overlap / parent-doc retrieval
- **Stale index** → an ops concern

---

## Evaluate the retriever, not just the answer

IR metrics on a labeled query set:

- **recall@k** — is the right chunk even in the top-k? (**caps** answer quality)
- **precision@k**, **MRR / nDCG** — is it ranked high?

> You can't fix an answer the retriever never surfaced.
> Diagnose RAG = separate retrieval failures from generation failures.

---

## Fine-tuning & PEFT — form, not facts

Use for style/format/narrow-skill/latency. **Wrong** for changing facts
(stale, not attributable).

- **Full FT** — all weights; costly; risks **catastrophic forgetting**
- **LoRA** — freeze base, train low-rank adapters `ΔW=BA` (r≪dim), <1% params;
  single-GPU, few-MB swappable adapters
- **QLoRA** — 4-bit frozen base → large models on commodity GPUs
- **Data quality is the hard part** — clean, on-distribution examples dominate

---

## The decision

| Need | Reach for |
|---|---|
| current/changing facts + citations | **RAG** |
| style / format / narrow skill | **Fine-tune (LoRA)** |
| small self-contained source | **Long-context** |
| cut latency/cost vs big prompt | **Fine-tune a small model** |
| facts **and** behavior | **Both** |

> Default: prompting → RAG → (only then) fine-tuning.

---

## Next

**Lab:** build RAG, induce a retrieval failure and fix it (hybrid / re-rank /
chunking), measure **recall@k**; optional Colab LoRA run.

**Module 5:** orchestration — tools, agents, control flow, MCP.
