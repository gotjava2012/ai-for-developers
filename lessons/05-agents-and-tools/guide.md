# Module 5 — Agents & Tool-Calling

> **Goal:** Understand what "agentic AI" actually means — an LLM plus tools plus
> a loop — how tool/function calling works, where MCP fits, and build a tiny
> agent that takes real actions.

This is where LLMs stop just *talking* and start *doing*.

---

## 5.1 What an "agent" really is (demystified)

Strip away the hype. An AI agent is:

> **an LLM + tools + a loop.**

- The **LLM** decides what to do next.
- **Tools** are functions it can call (search the web, query a database, run
  code, send an email, read a file).
- The **loop** keeps going — think, act, observe the result, think again — until
  the task is done.

That's it. "Agentic" just means the model can *take actions* and *react to the
results*, not just emit one block of text.

---

## 5.2 Tool-calling (a.k.a. function calling) — the core mechanism

An LLM can't actually run code or hit an API by itself — it only produces text.
Tool-calling is the protocol that bridges that gap:

1. You describe your tools to the model (name, what it does, parameters) — usually
   as a JSON schema.
2. The model, instead of answering, replies: *"call `get_weather` with
   `{city: 'Denver'}`."*
3. **Your code** actually runs that function and gets the result.
4. You feed the result back to the model.
5. The model uses it to answer (or calls another tool).

```
user → LLM ──(wants a tool)──▶ your code runs the tool ──▶ result
                 ▲                                            │
                 └──────────────── fed back ──────────────────┘
        (loop until the LLM has what it needs to answer)
```

**Key safety point:** the model only *requests* an action. **Your code decides
whether to actually run it.** That boundary is where you put permissions,
validation, and limits — critical once tools can spend money or change data.

---

## 5.3 The agent loop

```
1. Give the LLM the goal + the list of available tools
2. LLM responds: either a final answer OR a tool call
3. If tool call: your code runs it, captures the result
4. Feed the result back to the LLM
5. Repeat from 2 until the LLM gives a final answer (or you hit a limit)
```

**Always cap the loop** (max iterations) — an unsupervised agent can loop
forever, rack up cost, or thrash. Bounding it is non-negotiable.

---

## 5.4 Where MCP fits

As soon as you have many tools across many systems, a problem appears: every
agent/app wires up tools differently, and it doesn't scale.

**MCP (Model Context Protocol)** is an open standard that solves this. It defines
a common way for AI clients to discover and call tools exposed by "MCP servers."
Build a tool once as an MCP server, and *any* MCP-capable client can use it —
no bespoke integration per app.

- An **MCP server** exposes a set of tools (e.g. a Jira server, a GitHub server).
- An **MCP client** (your AI app/IDE) connects and can call those tools.
- An **MCP gateway/orchestrator** can sit in front of many servers, routing
  calls, adding auth, rate limits, and logging — so one entry point manages
  dozens of tool servers.

MCP is becoming the "USB-C of AI tools": a standard plug so tools and models
interoperate. (If you want a real-world reference, see the companion
`ai-mcp-servers` project — a gateway orchestrating 200+ tools across many MCP
servers with circuit breakers, rate limiting, and audit logging.)

---

## 5.5 What can go wrong (design for it)

Agents are powerful *because* they act — which is also the risk:

- **Runaway loops** → cap iterations and cost.
- **Harmful/irreversible actions** → require confirmation for anything that
  spends money, deletes, or sends; keep a human in the loop for high-stakes steps.
- **Prompt injection via tool results** → data an agent reads (a web page, a
  file) can contain malicious instructions; treat tool output as untrusted.
- **Over-broad permissions** → give each tool the *least* access it needs.

Good agent engineering is mostly good *boundary* engineering: what the agent may
do, how far it may go, and where a human must approve.

---

## Key terms
- **Agent** — LLM + tools + a loop; can take actions and react.
- **Tool / function calling** — the model requests a function; your code runs it.
- **Agent loop** — think → act → observe → repeat (bounded).
- **MCP (Model Context Protocol)** — open standard for exposing/consuming tools.
- **MCP server / client / gateway** — expose tools / use tools / route+govern many.

## Check yourself
1. Define an agent in five words.
2. When an LLM "calls a tool," what actually executes the function?
3. Why must you cap the agent loop?
4. What problem does MCP solve once you have many tools?
5. Name two safety boundaries you'd put around a tool that can send email.

➡️ **Do the `lab/`** — build a tiny agent that uses tools, and watch the
think → act → observe loop run.
