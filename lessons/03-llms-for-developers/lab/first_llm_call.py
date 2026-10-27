"""
Module 3 Lab — Your first LLM call, from code.

Runs against a LOCAL model via Ollama (free, offline). The same pattern works
for a hosted API — see the note at the bottom.

Prereqs:
    1. Install Ollama: https://ollama.com
    2. Pull a small model:  ollama pull llama3.2:1b   (or any model you have)
    3. python3 first_llm_call.py

Try:
    python3 first_llm_call.py "Explain what a token is in one sentence."
    python3 first_llm_call.py --temp 1.3 "Give me a creative product name for a coffee app"
"""

import json
import os
import sys
import urllib.request

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
MODEL = os.environ.get("CHAT_MODEL", "llama3.2:1b")


def ask_llm(prompt, system="You are a helpful, concise assistant.", temperature=0.2):
    """A minimal LLM call. This is INFERENCE (Module 1) in ~10 lines."""
    body = {
        "model": MODEL,
        "prompt": prompt,
        "system": system,
        "stream": False,
        "options": {"temperature": temperature},
    }
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.loads(resp.read().decode()).get("response", "").strip()


def main():
    args = sys.argv[1:]
    temperature = 0.2
    if "--temp" in args:
        i = args.index("--temp")
        temperature = float(args[i + 1])
        del args[i:i + 2]
    prompt = " ".join(args) if args else "Explain what an LLM is in two sentences."

    print(f"Model: {MODEL}  |  temperature: {temperature}\n")
    print(f"PROMPT: {prompt}\n")
    print("RESPONSE:")
    try:
        print(ask_llm(prompt, temperature=temperature))
    except Exception as e:
        print(f"[could not reach Ollama at {OLLAMA_URL}: {e}]")
        print("Make sure Ollama is running (`ollama serve`) and the model is pulled.")


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# SAME PATTERN WITH A HOSTED API (e.g. OpenAI) — for when you're ready:
#
#   from openai import OpenAI
#   client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
#   resp = client.chat.completions.create(
#       model="gpt-4o-mini",
#       messages=[{"role": "system", "content": system},
#                 {"role": "user", "content": prompt}],
#       temperature=temperature,
#   )
#   print(resp.choices[0].message.content)
#
# Notice: identical shape (system + prompt + temperature). Only the transport
# and auth change. Learn the pattern once, use it everywhere.
# ---------------------------------------------------------------------------
