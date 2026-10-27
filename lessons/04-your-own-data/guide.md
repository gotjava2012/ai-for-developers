# Module 4 — Grounding & Customization (RAG, Fine-Tuning, Long-Context)

> **Goal:** Make the central architectural decision of applied LLM work — how to
> adapt a general model to your domain — with real understanding of the
> mechanisms, failure modes, and evaluation. RAG, fine-tuning, and long-context
> are not interchangeable; knowing *when* and *why* is the senior skill here.

---

## 4.1 The problem, framed as distribution vs. facts

A foundation model encodes a general distribution; it has no access to your
private, proprietary, or post-cutoff facts, and it fabricates at a nonzero rate
(Module 3). Three levers to adapt it:

- **RAG** — inject relevant facts into the context at inference time. Changes the
  *input*, not the weights.
- **Fine-tuning** — shift the weights toward a behavior/format/domain via
  additional training. Changes the *model*.
- **Long-context** — just put more raw material in the window. Changes *how much
  input*, bounded by cost and the limits from Module 3.

They address different axes: RAG and long-context inject **knowledge**;
fine-tuning instills **behavior/skill/format**. They compose.

---

## 4.2 RAG as a retrieval system (because that's what it is)

The generation half is easy; **RAG is a search problem**, and its quality is
dominated by retrieval quality. Pipeline:

**Indexing (offline):** chunk → embed → store in a vector index.
**Query (online):** embed query → retrieve top-k → (re-rank) → assemble context
→ generate with answer-only-from-context instruction.

### Embeddings and similarity
An embedding maps text to a vector such that semantic similarity ≈ geometric
proximity (cosine similarity = angle between vectors, magnitude-invariant).
Retrieval = approximate nearest-neighbor (ANN) search (HNSW, IVF) over those
vectors — exact search is O(N), ANN trades a little recall for sublinear latency
at scale.

### The decisions that actually determine quality
- **Chunking** — size and boundaries are consequential. Too large → diluted
  embeddings, wasted context, lost-in-the-middle; too small → fragments lacking
  the context to be meaningful. Prefer semantic/structural boundaries
  (headings, sections) over fixed character counts; use overlap to preserve
  straddling content.
- **Embedding model choice** — domain match matters; a model that embeds your
  jargon well beats a bigger generic one. Dimensionality trades recall vs.
  storage/latency.
- **Retrieval depth k** — more candidates ↑ recall but ↑ context cost and noise;
  there's a quality peak, not "more is better."
- **Metadata filtering** — pre-filter by source/date/permissions before vector
  search; often the difference between usable and not.

---

## 4.3 Retrieval failure modes (where RAG actually breaks)

RAG systems rarely fail at generation; they fail at retrieval, silently:
- **Semantic mismatch** — the query and the answer-bearing chunk don't embed
  close (question vs. statement phrasing). Mitigate with query rewriting /
  HyDE (embed a hypothetical answer), or hybrid search.
- **Lexical gaps** — pure vector search misses exact keywords/IDs/codes.
  **Hybrid search** (vector + BM25/keyword, fused) fixes most of this.
- **Weak ranking** — the right chunk is retrieved but ranked low and truncated
  away. Add a **cross-encoder re-ranker**: retrieve 50, re-rank, keep 5.
- **Chunk boundary loss** — the answer spans two chunks. Overlap, larger chunks,
  or parent-document retrieval.
- **Stale index** — freshness bugs when sources change; index updates are an
  ops concern.

### Evaluate retrieval, not just the answer
Measure the retriever independently with IR metrics on a labeled query set:
**recall@k** (is the right chunk in the top-k at all — the ceiling on answer
quality), **precision@k**, **MRR / nDCG** (is it ranked high). You cannot fix an
answer the retriever never surfaced; diagnosing RAG means separating retrieval
failures from generation failures.

---

## 4.4 Fine-tuning and PEFT

Fine-tuning continues training on your examples to move the weights. Use it for
**form, not facts**: consistent style/tone, strict output formats, a narrow
specialized task, latency (a small fine-tuned model can replace a large prompted
one). It is the *wrong* tool for changing facts — baked-in knowledge goes stale
and isn't attributable.

- **Full fine-tuning** updates all weights — memory- and data-hungry, and risks
  **catastrophic forgetting** of general ability.
- **PEFT / LoRA** — freeze the base model; inject low-rank adapter matrices
  (`ΔW = BA`, rank r ≪ dim) into attention projections and train only those —
  typically <1% of parameters. Near-full-FT quality, fits a single GPU, adapters
  are a few MB and swappable at serve time. **QLoRA** adds 4-bit quantization of
  the frozen base to fine-tune large models on commodity GPUs.
- **Data is the hard part**, not the training command: fine-tuning amplifies the
  quality and consistency of your example set. Hundreds of clean, on-distribution
  examples beat thousands of noisy ones.

---

## 4.5 The decision, as an engineer makes it

| Need | Reach for |
|---|---|
| Current/changing facts, attribution, auditability | **RAG** |
| Consistent style, format, tone, or a narrow skill | **Fine-tuning (LoRA)** |
| Small, self-contained source that fits the window | **Long-context** (simplest; watch cost/lost-in-middle) |
| Latency/cost reduction vs. a big prompted model | **Fine-tune a small model** |
| Facts *and* behavior | **Both** — fine-tune the form, RAG the facts |

**Default path:** strong prompting → add RAG when you need your data → consider
fine-tuning only after prompting + retrieval are exhausted. Most production
systems are RAG + prompt engineering; fine-tuning is a deliberate optimization,
not a starting point. Reasons: RAG keeps facts fresh and attributable, is
cheaper to iterate, and doesn't require a training pipeline or labeled data.

---

## Terms, at working precision
- **ANN / HNSW / IVF** — approximate nearest-neighbor indexes for sublinear retrieval.
- **Hybrid search** — fuse dense (vector) + sparse (BM25) retrieval.
- **Re-ranker (cross-encoder)** — scores query–chunk pairs jointly for precise ordering.
- **recall@k / MRR / nDCG** — retrieval quality metrics; recall@k caps answer quality.
- **HyDE / query rewriting** — bridge query–document phrasing mismatch.
- **LoRA / QLoRA** — low-rank (and quantized) parameter-efficient fine-tuning.
- **Catastrophic forgetting** — loss of general ability from naive full fine-tuning.

## Check yourself
1. Why is RAG primarily a search problem, and what's the single most important
   retrieval metric — why?
2. Give a concrete failure that pure vector search causes and the technique that fixes it.
3. When is fine-tuning the wrong tool, and why specifically?
4. What does LoRA freeze and what does it train, and why does that make
   single-GPU fine-tuning feasible?
5. You need answers over a weekly-updated policy wiki *with citations*, in the
   company's formal voice. What's the architecture, component by component?

➡️ **Lab:** build a RAG pipeline, deliberately induce a retrieval failure and
fix it (hybrid/re-rank/chunking), measure recall@k, and — optionally on Colab —
run a LoRA fine-tune and inspect the trainable-parameter fraction.
