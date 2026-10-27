# Module 5 — Agents, Tool-Calling & Orchestration

> **Goal:** Understand agentic systems as what they are — control loops around a
> stochastic decision-maker — including the common architectures, the
> tool-calling mechanism, the reliability and context problems that dominate in
> practice, and where MCP fits as a standardization layer. Then build one and
> see the control boundaries.

---

## 5.1 Definition that survives contact with production

An agent is a **control loop in which an LLM chooses actions, those actions
execute, and results feed back into the model's context until a termination
condition**. Formally it's a policy over {emit a tool call, emit a final answer}
conditioned on accumulating context.

The thing to internalize: you are building a **control system whose controller
is non-deterministic and occasionally wrong**. Everything hard about agents —
reliability, cost, loops, safety — comes from that. The LLM is the planner; your
code is the runtime, the sandbox, and the safety envelope.

---

## 5.2 Tool-calling, mechanically

The model cannot execute anything; it emits structured *intent*. The loop:

1. You advertise tools as schemas (name, description, typed parameters —
   JSON-Schema). These descriptions are **prompt**: the model selects tools based
   on them, so they're part of your engineering surface.
2. The model returns a structured **tool call** (name + arguments) instead of
   prose. Modern APIs expose this as first-class "function/tool calling" with
   constrained decoding to valid JSON.
3. **Your runtime** validates the arguments, enforces authorization, executes
   the function, and captures the result.
4. You append the result to context; the model continues — another call, or a
   final answer.

The control boundary is step 3: **the model proposes, your code disposes.**
Authorization, validation, rate limiting, and side-effect policy live there, not
in the prompt — a prompt instruction is not a security control.

---

## 5.3 Agent architectures (choose deliberately)

- **ReAct (reason + act)** — interleave a thought, an action, an observation,
  repeat. Simple, general, the default; prone to meandering on hard tasks.
- **Plan-then-execute** — generate a full plan up front, then execute steps.
  More controllable and auditable, cheaper to parallelize; weaker at adapting
  when a step surprises it.
- **Reflection / critique loops** — a second pass (same or separate model)
  evaluates and revises the output. Improves quality at the cost of more calls;
  your `agent-orchestrator` Builder→Validator loop is this pattern.
- **Multi-agent / role decomposition** — specialized agents with scoped tools and
  a coordinator. Powerful for separable work; adds orchestration complexity and
  cost, and compounding error across hops.

Bias toward the **least agentic design that solves the problem**. A fixed
pipeline with one well-placed LLM call is more reliable and cheaper than an
autonomous loop — reach for autonomy only when the task genuinely requires
dynamic, data-dependent control flow.

---

## 5.4 The problems that actually dominate

- **Reliability compounds.** If each step succeeds 90% of the time, a 5-step
  chain is ~59%. Agent reliability is the *product* of step reliabilities —
  which is why bounding steps and validating each one matters more than cleverness.
- **Context growth.** Every step appends to the window → rising cost, latency,
  and lost-in-the-middle degradation over long runs. Manage it: summarize prior
  steps, prune stale observations, scope what each step sees.
- **Loops and non-termination.** Stochastic controllers get stuck repeating
  actions. **Always** bound max iterations and cost; detect repeated
  states/no-progress and break.
- **Error recovery.** Tools fail, return junk, time out. Feed errors back as
  observations the model can react to, with retry/backoff and a give-up path to
  human escalation.
- **Observability.** You can't debug what you can't see: log every thought, tool
  call, argument, result, and token/cost per step. Traces are non-optional.

---

## 5.5 MCP — standardizing the integration layer

Hand-wiring tools per app doesn't scale: N apps × M tools × bespoke glue. **MCP
(Model Context Protocol)** is an open protocol that standardizes how clients
discover and invoke tools exposed by servers.

- **Server** — exposes a capability set (e.g. Jira, GitHub, a database) behind a
  uniform interface.
- **Client** — an AI app/IDE that connects and consumes any compliant server.
- **Gateway/orchestrator** — fronts many servers to centralize routing,
  authn/authz, rate limiting, circuit breaking, and audit logging — so one
  governed entry point manages dozens of tool servers. (The companion
  `ai-mcp-servers` project is exactly this: 200+ tools across many servers with
  per-server circuit breakers, per-tool rate limits, secret redaction, and audit
  logging — i.e. the "your code disposes" boundary from §5.2, operationalized at
  fleet scale.)

MCP matters because it turns tool integration from per-app glue into a reusable,
governable layer — and because the gateway is the natural place to enforce the
safety envelope uniformly.

---

## 5.6 Security & safety surface (expanded in Module 6)

Agents convert model mistakes into **actions with side effects**, so the stakes
rise:
- **Prompt injection → tool abuse.** Untrusted content an agent reads (a page, a
  file, a ticket) can carry instructions that trigger tool calls. Treat all tool
  output as untrusted; constrain which tools are reachable in which contexts.
- **Excessive agency.** Scope tools to least privilege; gate irreversible/
  spending/destructive actions behind explicit confirmation or human approval.
- **Blast radius.** Assume the controller will eventually do the wrong thing;
  design so the worst case is bounded (read-only by default, dry-run, spend caps,
  reversibility).

---

## Terms, at working precision
- **Agent** — control loop: LLM chooses actions, runtime executes, results feed back, bounded.
- **Tool/function calling** — model emits structured intent; runtime validates and executes.
- **ReAct / plan-execute / reflection / multi-agent** — the common control architectures.
- **Reliability compounding** — chain success ≈ product of step successes.
- **MCP** — open protocol for discovering/invoking tools across servers; gateway governs the fleet.
- **Excessive agency** — more authority/tools than the task needs; a blast-radius risk.

## Check yourself
1. Express agent reliability in terms of per-step reliability. What does that imply for design?
2. Why is a tool's *description* part of your engineering surface?
3. Where exactly does authorization belong, and why not in the system prompt?
4. Contrast ReAct and plan-then-execute; when is each the better fit?
5. What problem does MCP solve that per-app tool wiring doesn't, and why is the gateway the right place for the safety envelope?

➡️ **Lab:** build a bounded tool-calling agent, locate the propose/dispose
control boundary in code, break reliability by raising step count, and add an
approval gate for a destructive tool.
