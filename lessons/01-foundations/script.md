# Module 1 — Foundations · Video/Presentation Script

*Estimated runtime: ~8–10 minutes. Cues in [brackets] map to slides.md.*

---

[Slide: title]

Welcome to AI for Developers. This course is for people who can already code —
you know your way around a terminal, you can call an API — but you haven't
really done AI yet. So we're going to skip the beginner programming stuff and
get straight to how AI actually works and how you build with it.

In this first module we're not writing much code. We're building the right
*mental model*, because if you get the model wrong, you'll waste weeks building
the wrong thing. Let's go.

---

[Slide: term soup]

First, let's clear up the words everyone mixes together.

AI is the big umbrella — making machines do things that normally need human
intelligence. Inside that is Machine Learning: instead of hand-coding rules,
you let a program learn patterns from data. Inside ML is Deep Learning, which
uses neural networks with lots of layers. And the newest, loudest corner is
Generative AI and Large Language Models — think GPT, Claude, Llama — which
generate new text and code.

So they're nested, not separate. Here's the one practical habit: when a
stakeholder says "let's add AI," ask them — do you mean a trained model, or an
LLM behind an API? Because the engineering for those is completely different.

---

[Slide: why now]

Quick history, because it kills the intimidation. These ideas are decades old.
Three things changed: we got enormous data from the internet, we got GPUs for
cheap compute, and in 2017 researchers invented the transformer — an
architecture that just keeps getting better as you throw more data and compute
at it. Every modern LLM is a transformer. That's the whole story. No magic.

---

[Slide: Training ≠ Inference]

Okay, the most important idea in this entire module. AI has two totally separate
phases, and confusing them is the number one beginner mistake. Training, and
inference.

---

[Slide: training / inference]

Training is building the model. You feed it tons of data, and it adjusts
millions or billions of internal numbers — parameters — until it stops making
mistakes. This is expensive and slow. Training a big language model costs
millions of dollars and weeks of GPU time. You do it rarely.

Inference is *using* the already-trained model. Input goes in, output comes out.
This is fast, cheap, and happens constantly — it's literally what happens every
time you call an LLM API.

And here's the liberating part: as a developer, you live in inference. You are
almost never training a model from scratch. You're using a model somebody else
spent millions to train. Your real job is prompting, retrieval, tools,
evaluation, and cost — not GPUs and PhD math. That myth stops people before they
start, so let it go now.

---

[Slide: the flow]

Here's the whole pipeline. Data goes through training — rare and expensive — and
produces a trained model. Then that model goes through inference — constant and
cheap, just an API call — and produces your app's output. You plug in at the
bottom.

---

[Slide: good at / can't do]

Let's set expectations honestly. AI is genuinely great at pattern recognition,
generating and transforming text and code, summarizing, and pulling structure
out of messy input.

But it cannot guarantee truth. An LLM predicts plausible text — it will tell you
something false with total confidence. That's called hallucination and we'll
dig into it in Module 3. It also doesn't know your private data or anything
after its training cutoff unless you give it that information. And it's not
deterministic — same prompt, different answers — so don't drop a raw LLM
anywhere you need exact, repeatable results without guardrails.

---

[Slide: mental model]

So here's the mental model to carry through the whole course. Treat an LLM like
a brilliant, fast, confident intern who sometimes just makes things up. Useful
everywhere. Trusted nowhere without verification. Burn that in.

---

[Slide: where you'll spend your time]

Here's the roadmap of where your actual time goes as an AI developer, and it
maps to the rest of this course: inference and prompting first, then grounding
models with your own data using RAG and fine-tuning, then agents and tools, then
making it production-ready with evals, guardrails, cost, and security. Training
is last and smallest — and when you do it, it's usually fine-tuning, not from
scratch.

---

[Slide: lab + next]

Before the next module, do the quick lab in the `lab` folder — it's a no-code
exercise to lock in these concepts, plus your first peek at what a "model" file
actually is. Then in Module 2, we stop talking and start doing: you'll run a
real neural network and literally watch it learn. See you there.
