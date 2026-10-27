---
marp: true
theme: default
paginate: true
header: "AI for Developers · Module 5 — Agents & Tool-Calling"
---

# Module 5
## Agents & Tool-Calling

Where LLMs stop talking and start doing.

---

## What an agent really is

> **an LLM + tools + a loop**

- **LLM** decides what to do next
- **Tools** = functions it can call (search, query, run code, send email)
- **Loop** = think → act → observe → repeat, until done

"Agentic" = the model can **take actions** and react to results.

---

## Tool-calling (the core mechanism)

An LLM only produces text — it can't run code itself. So:

```
1. You describe tools to the model (name, purpose, params)
2. Model replies: "call get_weather({city:'Denver'})"
3. YOUR code runs the function
4. You feed the result back
5. Model answers (or calls another tool)
```

🔒 The model only *requests*. **Your code decides whether to run it.**

---

## The agent loop

```
1. give LLM the goal + available tools
2. LLM → final answer OR a tool call
3. tool call? your code runs it, captures result
4. feed result back
5. repeat until final answer (or a limit)
```

⚠️ **Always cap the loop** — unbounded agents loop, cost, and thrash.

---

## Where MCP fits

Many tools across many systems → integration chaos.

**MCP (Model Context Protocol)** = open standard for exposing/calling tools.

- **MCP server** — exposes tools (Jira, GitHub, …)
- **MCP client** — your AI app uses them
- **MCP gateway** — routes many servers; adds auth, rate limits, logging

> The "USB-C of AI tools." Build a tool once; any MCP client can use it.

---

## What can go wrong (design for it)

- **Runaway loops** → cap iterations & cost
- **Irreversible actions** → confirm spend/delete/send; human in the loop
- **Prompt injection via tool results** → treat tool output as untrusted
- **Over-broad permissions** → least access per tool

Good agent engineering = good **boundary** engineering.

---

## Lab

1. Build a tiny **agent**: LLM + 2 tools + a loop
2. Watch it **think → call a tool → observe → answer**
3. See where **your code** gates the tool call

**Next:** Module 6 — Building Real, Responsible AI Apps
