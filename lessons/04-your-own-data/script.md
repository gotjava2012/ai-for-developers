# Module 4 — Giving an LLM Your Own Data · Script

*Runtime: ~9–11 min. [brackets] map to slides.md.*

---

[Slide: title]

In Module 3 we watched an LLM confidently make something up. This module is how
you stop that — by giving the model *your* data. There are two techniques: RAG
and fine-tuning. Knowing which to reach for is one of the most important
architectural calls you'll make in an AI project, so let's get it right.

---

[Slide: the problem]

Here's the situation. A base model like GPT or Llama knows nothing about your
company's internal docs, your codebase, or anything that happened after its
training cutoff. Ask it about your product and you get either "I don't know" or,
worse, a fluent hallucination. The model never saw your data. Two ways to fix
that: RAG, and fine-tuning.

---

[Slide: RAG]

RAG — Retrieval-Augmented Generation. The key insight is beautiful in its
simplicity: you don't change the model at all. You change its input.

It works in two phases. The indexing phase runs once, ahead of time: you take
your documents, chunk them into passages, turn each chunk into an embedding
vector, and store those in a vector index. Then the query phase runs for every
question: you embed the question the same way, retrieve the chunks whose vectors
are most similar, stuff those chunks into the prompt as context, and ask the LLM
to answer using only them. Retrieve, augment, generate.

---

[Slide: why RAG first]

Why is RAG almost always the right first move? Your facts stay current — when
the docs change, you just re-index, no retraining. You can cite sources, showing
exactly where an answer came from, which is huge for trust. It's cheaper and
faster to build than fine-tuning. And it directly attacks hallucination, because
the model is answering from facts you handed it rather than from memory. You'll
build a complete RAG system in the lab.

---

[Slide: fine-tuning]

Fine-tuning is the other tool. Here you actually train the model further on your
own examples, so the new behavior gets baked into its weights. Fine-tuning
shines for teaching a style, a tone, a format, or a specialized task — it is
*not* the right tool for injecting facts that change, because the facts get
frozen into the weights. It needs a dataset of examples, usually hundreds to
thousands, plus a GPU, and you have to redo it when things change.

The practical version is LoRA — Low-Rank Adaptation. Full fine-tuning would
update all of a model's billions of weights, which most of us can't afford. LoRA
freezes the base model and trains tiny adapter matrices, often less than one
percent of the parameters. You get most of the benefit, it runs on a single free
GPU, and the saved adapter is just a few megabytes. There's an optional lab where
you run one on Colab.

---

[Slide: RAG vs fine-tuning]

So how do you choose? Use RAG when you need facts and knowledge, when the data
changes often, when you must cite sources, and when you want to ship fast and
cheap — which is most applications. Use fine-tuning when you need a particular
style, tone, or format, when the behavior is stable, and typically only after
you've already pushed prompting and RAG as far as they go.

The rule of thumb to remember: RAG for what the model should *know*; fine-tuning
for how it should *behave*. And they combine beautifully — fine-tune the voice,
RAG the facts. But honestly? Start with good prompting, add RAG if you need your
data, and most teams never actually need to fine-tune at all.

---

[Slide: embeddings + vector search]

Quick look under the hood at what powers retrieval. An embedding turns a piece
of text into a vector of numbers, positioned so that texts with similar meaning
land close together. Retrieval is just finding the stored vectors nearest to
your question's vector, and "nearest" is usually measured with cosine
similarity — the angle between the vectors. For small datasets you can compare
against every vector exactly, which is what the lab does so you can see the
mechanics. In production you'd use a vector database — Chroma, FAISS, Qdrant,
pgvector — which uses approximate nearest-neighbor search to stay fast at scale.

---

[Slide: lab]

Now build it. In the lab you'll stand up a working RAG system over your own
documents, ask it questions, and watch it retrieve the relevant chunks and
answer *with citations*. Then you'll ask it something that isn't in the
documents, and watch it correctly say it doesn't know — the hallucination from
Module 3, fixed. And if you want to go further, there's an optional Colab lab
where you run a real LoRA fine-tune. After that, Module 5: we let the model take
actions, with agents and tools.
