# Module 3 Lab — Your First LLM (hands-on)

Make a real LLM call, feel the temperature knob, improve a prompt, and trigger a
hallucination on purpose.

## Setup (free, local, offline)
```bash
# 1. Install Ollama: https://ollama.com
# 2. Pull a small model:
ollama pull llama3.2:1b
# 3. Make sure Ollama is running (the app, or `ollama serve`)
```
No API key, no cost. (If you'd rather use a hosted API, see the note at the
bottom of `first_llm_call.py` — same code shape.)

---

## Part A — Your first call
```bash
python3 first_llm_call.py "Explain what a token is in one sentence."
```
You just did **inference** against a trained model in ~10 lines of code. Open
`first_llm_call.py` and notice the request is just: model + system prompt +
user prompt + temperature.

---

## Part B — Feel the temperature knob
Run the SAME creative prompt at low and high temperature:
```bash
python3 first_llm_call.py --temp 0.1 "Give me a product name for a coffee app"
python3 first_llm_call.py --temp 1.3 "Give me a product name for a coffee app"
```
Low temp → safe, repetitive. High temp → varied, surprising (sometimes
nonsense). **Lesson:** low for factual/structured, high for brainstorming.

---

## Part C — Prompting is engineering
Compare a vague prompt to a specific one:
```bash
python3 first_llm_call.py "summarize machine learning"
python3 first_llm_call.py "Summarize machine learning for a backend developer in exactly 3 bullet points, no jargon."
```
Notice how much better the second is. Specificity + format = control.

Now ask for structured output:
```bash
python3 first_llm_call.py "Return a JSON object with keys 'term' and 'definition' defining 'inference'. Output only JSON."
```

---

## Part D — Trigger a hallucination (on purpose)
Ask about something specific and obscure that the model likely doesn't know, and
watch it confidently make something up:
```bash
python3 first_llm_call.py --temp 0.9 "Summarize the key findings of the 2019 Zelinsky-Okafor paper on quantum tunneling in houseplants."
```
That paper doesn't exist — but a small model will often invent a fluent summary
anyway. **This is the single most important thing to witness in this course.**
It's why Module 4 (grounding with RAG) exists.

> If your model happens to refuse or say it doesn't know — good, that's the
> ideal behavior. Try a couple of obscure fake specifics; smaller models
> hallucinate readily.

---

## Exercises
1. Write a system prompt that forces the model to answer "I don't know" when
   unsure. Does it reduce the Part D hallucination?
2. Get the model to reliably output valid JSON 3 times in a row. What prompt
   wording made it consistent?
3. Find the temperature where the coffee-app names stop being usable.

## Takeaway
You can now call an LLM, steer it with system prompts and temperature, and you've
*seen* it hallucinate. Next: stop the hallucinations by giving it real data.

➡️ **Next:** Module 4 — Giving an LLM Your Own Data (RAG & fine-tuning).
