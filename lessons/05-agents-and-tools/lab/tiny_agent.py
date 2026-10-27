"""
Module 5 Lab — A tiny agent: LLM + tools + a loop.

This is a minimal, readable agent so you can SEE the think -> act -> observe
loop and, crucially, the exact line where YOUR code decides whether to run a
tool the model requested.

It runs in two modes:
  - MOCK mode (default, no model needed): a scripted "LLM" so you can watch the
    loop mechanics with zero setup.
  - OLLAMA mode: set USE_OLLAMA=1 to drive it with a real local model.

Run:
    python3 tiny_agent.py "What is 23 * 19, and what time is it?"
    USE_OLLAMA=1 python3 tiny_agent.py "What is 23 * 19?"
"""

import datetime
import json
import os
import re
import sys
import urllib.request

# ---------------------------------------------------------------------------
# 1) THE TOOLS — ordinary Python functions the agent may call.
#    Each has a name, a description, and runs real code.
# ---------------------------------------------------------------------------
def tool_calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression, e.g. '23 * 19'."""
    # SAFETY: only allow digits/operators — never eval arbitrary input from a model.
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        return "error: expression contains disallowed characters"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"error: {e}"


def tool_current_time(_: str = "") -> str:
    """Return the current local time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


TOOLS = {
    "calculator": {"fn": tool_calculator, "desc": "evaluate arithmetic, arg=expression"},
    "current_time": {"fn": tool_current_time, "desc": "get the current time, no arg"},
}

# The gate: the model may only ever REQUEST these. Your code enforces the allow-list.
ALLOWED_TOOLS = set(TOOLS.keys())


# ---------------------------------------------------------------------------
# 2) THE "LLM" — decides the next step. In MOCK mode it's scripted; in OLLAMA
#    mode it's a real model prompted to emit a tool call or a final answer.
#    Protocol: the LLM outputs either
#        TOOL: <name> | <arg>
#    or
#        ANSWER: <final answer>
# ---------------------------------------------------------------------------
def llm_decide(goal, history):
    if os.environ.get("USE_OLLAMA") == "1":
        return _ollama_decide(goal, history)
    return _mock_decide(goal, history)


def _mock_decide(goal, history):
    """A scripted stand-in so the loop runs with zero setup.
    Strategy: if the goal mentions math and we haven't done it, call calculator;
    if it mentions time and we haven't, call current_time; else answer."""
    done_tools = {h["tool"] for h in history if "tool" in h}
    m = re.search(r"(\d+\s*[*+\-/]\s*\d+)", goal)
    if m and "calculator" not in done_tools:
        return f"TOOL: calculator | {m.group(1)}"
    if "time" in goal.lower() and "current_time" not in done_tools:
        return "TOOL: current_time | "
    # compose a final answer from what we observed
    facts = "; ".join(f"{h['tool']}({h['arg']})={h['result']}" for h in history if "tool" in h)
    return f"ANSWER: Based on the tools I used -> {facts or 'no tools needed'}"


def _ollama_decide(goal, history):
    sys_prompt = (
        "You are an agent that can use tools. Available tools:\n"
        + "\n".join(f"- {n}: {t['desc']}" for n, t in TOOLS.items())
        + "\nRespond with EXACTLY one line, either:\n"
          "TOOL: <tool_name> | <argument>\n"
          "or\nANSWER: <final answer>\n"
          "Use tools to get facts before answering."
    )
    convo = f"GOAL: {goal}\n" + "\n".join(
        f"observed {h['tool']}({h['arg']}) = {h['result']}" for h in history if "tool" in h
    )
    body = {"model": os.environ.get("CHAT_MODEL", "llama3.2:1b"),
            "system": sys_prompt, "prompt": convo, "stream": False,
            "options": {"temperature": 0}}
    req = urllib.request.Request("http://127.0.0.1:11434/api/generate",
                                 data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read().decode()).get("response", "").strip().splitlines()[0]


# ---------------------------------------------------------------------------
# 3) THE LOOP — think -> act -> observe -> repeat, BOUNDED.
# ---------------------------------------------------------------------------
def run_agent(goal, max_steps=5):
    print(f"GOAL: {goal}\n")
    history = []
    for step in range(1, max_steps + 1):
        decision = llm_decide(goal, history)
        print(f"[step {step}] LLM decides: {decision}")

        if decision.startswith("ANSWER:"):
            print(f"\nFINAL ANSWER: {decision[len('ANSWER:'):].strip()}")
            return

        if decision.startswith("TOOL:"):
            body = decision[len("TOOL:"):].strip()
            name, _, arg = body.partition("|")
            name, arg = name.strip(), arg.strip()

            # ===== THE SAFETY GATE: your code decides whether to run it =====
            if name not in ALLOWED_TOOLS:
                print(f"         ⛔ blocked: '{name}' is not an allowed tool")
                history.append({"tool": name, "arg": arg, "result": "blocked"})
                continue
            # (here is where you'd also require human approval for risky tools)
            result = TOOLS[name]["fn"](arg)
            print(f"         ✅ ran {name}({arg!r}) -> {result}")
            history.append({"tool": name, "arg": arg, "result": result})
        else:
            print("         (unparseable; stopping)")
            return
    print("\n[loop cap reached — stopping so the agent can't run forever]")


if __name__ == "__main__":
    goal = " ".join(sys.argv[1:]) or "What is 23 * 19, and what time is it?"
    run_agent(goal)
