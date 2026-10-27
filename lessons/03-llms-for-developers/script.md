# Module 3 — LLMs for Developers · Script

*Runtime: ~9–11 min. [brackets] map to slides.md.*

---

[Slide: title]

This is the module most of you came for: large language models. By the end
you'll understand what an LLM genuinely does under the hood, the settings you'll
actually tune, how to prompt like an engineer, and the one failure mode you must
design around. Then you'll make your first LLM call from code.

---

[Slide: what an LLM does]

Let's strip away the mystique. At its core, an LLM does exactly one thing: given
some text, it predicts the next token. A token is just a chunk of text, roughly
three-quarters of a word. The model looks at everything so far, assigns a
probability to every possible next token, picks one, adds it, and repeats. That
loop is how it produces whole paragraphs.

Here's the part to really internalize: it is *not* looking anything up in a
database. It's generating a statistically likely continuation of your text.
Every impressive thing it does emerges from next-token prediction at massive
scale. And this single fact — it predicts, it doesn't retrieve — explains almost
all of its behavior, including the weird and the wrong parts.

---

[Slide: knobs]

Now the knobs you'll actually touch as a developer. The context window is the
maximum number of tokens the model can see at once — and that budget has to hold
everything: your instructions, the user's input, any documents you give it, and
the response. Temperature controls randomness — near zero is focused and
near-deterministic, higher is more varied and creative. Max tokens caps the
output length. The system prompt is your top-level instruction that sets the
model's role and rules — it's your main steering lever. And stop sequences let
you halt generation at a marker.

One thing that surprises new AI developers: you pay per token, for both what you
send in and what comes out. A prompt stuffed with big documents costs real money
on every single call. Being token-aware is a genuine engineering skill, and
we'll come back to it in Module 6.

---

[Slide: prompting]

Prompting is engineering, not incantation. Your prompt is the model's input,
so treat it with the rigor you'd give any input. A few patterns that reliably
work. One: use a system prompt to set the role and the rules. Two: be specific
about the output format — if you want JSON, say so and show an example of the
shape. Three: give it a couple of input-output examples; this "few-shot"
technique often beats a wall of instructions. Four: put your instruction first
and clearly delimit the user's data, so the model doesn't confuse data with
commands. Five: for anything requiring reasoning, tell it to think step by step.

The anti-pattern is vagueness. "Make this better" gets you vague, inconsistent
results. Specificity is the entire game.

---

[Slide: hallucination]

Now the most important thing in this module. Because an LLM generates plausible
text instead of retrieving true text, it will sometimes hand you something
fluent, confident, and completely false. Fake citations. APIs that don't exist.
Wrong dates stated with total authority.

This is not a bug you can fully patch — it's inherent to how the technology
works. So you don't eliminate it, you manage it. You ground the model with real
data using RAG, which is the next module — you hand it the facts and tell it to
answer only from them. You ask for sources and you verify them. You lower the
temperature for factual work. And you never, ever auto-trust the output for
anything that matters without a check.

The single biggest mistake I see new AI developers make is shipping a feature
that quietly assumes the LLM's output is true. Build as if it sometimes lies,
because it does.

---

[Slide: local vs hosted]

Where do you get a model? Three options. Hosted APIs like OpenAI and Anthropic
are the easiest and most capable — you pay per token and your data leaves your
machine. Local models, run through a tool like Ollama, are free, private, and
work offline; they're smaller and less capable but fantastic for learning and
for privacy-sensitive work. And open-weight models like Llama and Qwen you can
download, run, or even fine-tune yourself — that's Module 4.

For this course's labs we default to Ollama so everything is free and runs
offline. But I want you to notice: the *code pattern* is identical whether
you're hitting a local model or a hosted API. Learn it once, apply it anywhere.

---

[Slide: lab]

Time to build. In the lab you'll make your first LLM call from code — just a few
lines. You'll change the temperature and watch the same prompt give different
answers. You'll take a weak prompt and improve it and compare the results. And
you'll deliberately trigger a hallucination, so you see with your own eyes that
confident and correct are not the same thing. Do that, and Module 4 is where it
gets powerful — we give the model *your* data.
