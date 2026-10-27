# Module 5 — Agents & Tool-Calling · Script

*Runtime: ~8–10 min. [brackets] map to slides.md.*

---

[Slide: title]

"Agent" is the most hyped word in AI right now, so let's cut through it. By the
end of this module you'll know exactly what an agent is — it's simpler than the
marketing suggests — how tool-calling actually works, where MCP fits, and you'll
have built a tiny working agent yourself.

---

[Slide: what an agent is]

Here's the whole concept, demystified: an agent is an LLM, plus tools, plus a
loop. The LLM decides what to do next. The tools are functions it can call —
search the web, query a database, run code, send an email. And the loop keeps it
going: think, act, observe the result, think again, until the task is done.
That's it. "Agentic" just means the model can take actions and react to what
happens, instead of producing one block of text and stopping.

---

[Slide: tool-calling]

Now the mechanism that makes it work: tool-calling, also called function calling.
Here's the thing people miss — an LLM can't actually run code or hit an API. All
it can do is produce text. So tool-calling is the bridge.

You describe your tools to the model: name, what each does, what parameters it
takes, usually as a JSON schema. Then, instead of answering, the model can reply
"call get_weather with city Denver." Your code — not the model — actually runs
that function and gets the result. You feed the result back, and now the model
can answer, or call another tool.

And here's the critical safety point, say it with me: the model only *requests*
an action. Your code decides whether to actually run it. That boundary is where
you put permission checks, validation, and limits — and it matters enormously
once your tools can spend money or change data.

---

[Slide: agent loop]

Put it together and you get the agent loop. Give the LLM the goal and the list
of tools. It responds with either a final answer or a tool call. If it's a tool
call, your code runs it and captures the result. You feed that back. And you
repeat until the model gives a final answer — or until you hit a limit.

That limit is not optional. Always cap the loop with a maximum number of
iterations. An unsupervised agent can loop forever, burn through your API budget,
or thrash between the same two steps. Bounding it is non-negotiable engineering.

---

[Slide: MCP]

So you start adding tools, and quickly you have many tools across many systems —
and every app wires them up its own way. That doesn't scale. This is the problem
MCP solves. MCP — the Model Context Protocol — is an open standard for how AI
clients discover and call tools.

You build a tool once as an MCP server — say, a Jira server or a GitHub server.
Any MCP-capable client can then use it, no custom integration per app. And you
can put an MCP gateway in front of many servers to route calls and add auth,
rate limiting, and logging from one place. Think of MCP as the USB-C of AI
tools — a standard plug so models and tools just interoperate. If you want a
real-world example, the companion ai-mcp-servers project is exactly this: a
gateway orchestrating over 200 tools across many MCP servers, with circuit
breakers, rate limiting, and audit logging.

---

[Slide: what can go wrong]

Agents are powerful precisely because they act — and that's also the danger.
Design for it. Runaway loops: cap iterations and cost. Irreversible actions like
spending, deleting, or sending: require confirmation, and keep a human in the
loop for anything high-stakes. Prompt injection through tool results: remember
that a web page or file your agent reads can contain malicious instructions, so
treat all tool output as untrusted data. And over-broad permissions: give each
tool the least access it needs.

The theme: good agent engineering is mostly good *boundary* engineering. What
may the agent do, how far may it go, and where must a human approve.

---

[Slide: lab]

In the lab you'll build a tiny but real agent — an LLM, a couple of tools, and
the loop — and watch it think, decide to call a tool, observe the result, and
produce an answer. Pay attention to the exact spot in the code where *your*
program gates whether the tool actually runs. That's the boundary that keeps
agents safe. Then, our final module: making all of this production-ready and
responsible.
