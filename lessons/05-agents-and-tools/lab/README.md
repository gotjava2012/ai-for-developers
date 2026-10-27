# Module 5 Lab — Build a Tiny Agent (hands-on)

Build and run a real (if small) agent: an LLM + tools + a loop. Watch the
think → act → observe cycle, and find the exact line where *your* code gates
whether a tool actually runs.

## Setup
Nothing required for mock mode (pure Python). Optional: Ollama for the real-LLM mode.
```bash
# the file is self-contained:
python3 tiny_agent.py "What is 23 * 19, and what time is it?"
```

---

## Part A — Watch the agent loop (mock mode, zero setup)
```bash
python3 tiny_agent.py "What is 23 * 19, and what time is it?"
```
Read the output step by step:
- **step 1** the "LLM" decides to call the `calculator` tool → your code runs it → `437`
- **step 2** it decides to call `current_time` → your code runs it
- **step 3** it has what it needs → emits a final ANSWER

That is the agent loop from the guide: **think → act → observe → repeat**, then
answer. (Mock mode uses a scripted stand-in for the LLM so you can see the
mechanics with no model.)

---

## Part B — Find the safety gate
Open `tiny_agent.py` and find the section marked:
```python
# ===== THE SAFETY GATE: your code decides whether to run it =====
```
This is the most important idea in the module. The "LLM" only *requested* a
tool; **your code** checks it against an allow-list before running it. Experiment:
- Add a fake tool name to the model's output path and watch it get **blocked**.
- Notice the comment where you'd add **human approval** for risky tools.

---

## Part C — Run it with a real LLM (optional)
```bash
ollama pull llama3.2:1b
USE_OLLAMA=1 python3 tiny_agent.py "What is 23 * 19?"
```
Now a real model decides the tool calls. Note it's less predictable than the
mock — small models sometimes format the tool call wrong. That unpredictability
is exactly why production agents need strict parsing, retries, and the loop cap.

---

## Part D — See the loop cap protect you
In `run_agent`, the loop is bounded by `max_steps=5`. This is what stops an agent
from looping forever and burning cost. Temporarily lower it to `max_steps=1` and
give it a 2-tool task — watch it hit the cap before finishing. Then restore it.

---

## Connect it to the real world: MCP
Your tiny agent wired up 2 tools by hand. Real systems have dozens across many
services — which is what **MCP** standardizes (guide §5.4). For a production-scale
reference, look at the companion **`ai-mcp-servers`** gateway: 200+ tools across
many MCP servers behind one entry point, with circuit breakers, rate limiting,
and audit logging — the same idea as your tiny agent's gate, at scale.

---

## Exercises
1. Add a third tool (e.g. `uppercase` that upper-cases its argument). Wire it
   into `TOOLS` and get the agent to use it.
2. Add a "risky" tool (e.g. `delete_file`) but make the gate **require typing
   'yes'** before it runs. This is human-in-the-loop approval.
3. In Ollama mode, make the system prompt stricter so the model formats tool
   calls more reliably.

## Takeaway
An agent is just an LLM choosing tools in a bounded loop — and the real
engineering is in the **boundaries**: the allow-list, the approval gate, and the
loop cap. Build those and agents are powerful *and* safe.

➡️ **Next:** Module 6 — Building Real, Responsible AI Apps.
