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

```svg
<svg viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <text x="150" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#b9770a">OFFLINE (index your docs)</text>
  <g font-size="12">
    <rect x="20" y="30" width="80" height="34" rx="5" fill="#fdf3e6" stroke="#f0a500"/><text x="60" y="51" text-anchor="middle">docs</text>
    <rect x="120" y="30" width="80" height="34" rx="5" fill="#fdf3e6" stroke="#f0a500"/><text x="160" y="51" text-anchor="middle">chunk</text>
    <rect x="220" y="30" width="80" height="34" rx="5" fill="#fdf3e6" stroke="#f0a500"/><text x="260" y="51" text-anchor="middle">embed</text>
    <rect x="320" y="30" width="110" height="34" rx="5" fill="#f0a500"/><text x="375" y="51" text-anchor="middle" fill="#fff" font-weight="bold">vector index</text>
  </g>
  <path d="M100 47 H120" stroke="#b9770a" stroke-width="2" marker-end="url(#r1)"/>
  <path d="M200 47 H220" stroke="#b9770a" stroke-width="2" marker-end="url(#r1)"/>
  <path d="M300 47 H320" stroke="#b9770a" stroke-width="2" marker-end="url(#r1)"/>
  <text x="150" y="104" text-anchor="middle" font-size="13" font-weight="bold" fill="#1d6a4f">ONLINE (answer a question)</text>
  <g font-size="12">
    <rect x="20" y="116" width="80" height="34" rx="5" fill="#eafaf3" stroke="#2a7d5f"/><text x="60" y="137" text-anchor="middle">query</text>
    <rect x="120" y="116" width="80" height="34" rx="5" fill="#eafaf3" stroke="#2a7d5f"/><text x="160" y="137" text-anchor="middle">embed</text>
    <rect x="220" y="116" width="90" height="34" rx="5" fill="#eafaf3" stroke="#2a7d5f"/><text x="265" y="137" text-anchor="middle">top-k search</text>
    <rect x="330" y="116" width="80" height="34" rx="5" fill="#eafaf3" stroke="#2a7d5f"/><text x="370" y="137" text-anchor="middle">context</text>
    <rect x="430" y="116" width="90" height="34" rx="5" fill="#2a7d5f"/><text x="475" y="137" text-anchor="middle" fill="#fff" font-weight="bold">generate</text>
  </g>
  <path d="M100 133 H120" stroke="#1d6a4f" stroke-width="2" marker-end="url(#r2)"/>
  <path d="M200 133 H220" stroke="#1d6a4f" stroke-width="2" marker-end="url(#r2)"/>
  <path d="M310 133 H330" stroke="#1d6a4f" stroke-width="2" marker-end="url(#r2)"/>
  <path d="M410 133 H430" stroke="#1d6a4f" stroke-width="2" marker-end="url(#r2)"/>
  <!-- index feeds the search -->
  <path d="M375 64 V88 H265 V116" stroke="#888" stroke-width="2" stroke-dasharray="5 4" fill="none" marker-end="url(#r3)"/>
  <text x="300" y="82" font-size="11" fill="#888">same index</text>
  <text x="475" y="175" text-anchor="middle" font-size="11" fill="#c0392b" font-weight="bold">answer from context only</text>
  <defs>
    <marker id="r1" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#b9770a"/></marker>
    <marker id="r2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#1d6a4f"/></marker>
    <marker id="r3" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#888"/></marker>
  </defs>
</svg>
```
<p class="diagram-caption">RAG is a search problem: index docs offline, retrieve the relevant ones at query time, then generate grounded in them.</p>

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
