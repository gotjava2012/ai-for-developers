---
marp: true
theme: default
paginate: true
header: "AI for Developers · Module 5 — Agents & Orchestration"
---

# Module 5 — Agents, Tool-Calling & Orchestration
### Control loops around a stochastic, occasionally-wrong controller

---

## Definition that survives production

> An agent is a **control loop**: the LLM chooses actions → runtime executes →
> results feed back into context → until a termination condition.

You're building a control system whose **controller is non-deterministic and
sometimes wrong.** The LLM plans; **your code is the runtime, sandbox, and
safety envelope.**

---

## Tool-calling, mechanically

1. Advertise tools as **schemas** (name/desc/typed params) — *descriptions are prompt*
2. Model returns a structured **tool call** (not prose)
3. **Your runtime** validates args, enforces authz, executes, captures result
4. Append result → model continues (another call or final answer)

> The boundary is step 3: **model proposes, your code disposes.**
> A prompt instruction is **not** a security control.

---

## Architectures — choose deliberately

- **ReAct** — thought→action→observation, repeat. Default; can meander
- **Plan-then-execute** — plan up front, then run. Controllable/auditable; less adaptive
- **Reflection/critique** — second pass revises (your Builder→Validator loop)
- **Multi-agent** — scoped roles + coordinator. Powerful; costly, compounding error

> Bias to the **least agentic design** that works. Fixed pipeline + one LLM call
> beats an autonomous loop when the task allows.

---

## The problems that dominate

- **Reliability compounds:** 90%/step × 5 steps ≈ **59%**
- **Context growth:** each step appends → cost, latency, lost-in-middle → prune/summarize
- **Loops/non-termination:** bound iterations & cost; detect no-progress
- **Error recovery:** feed failures back as observations; retry/backoff; escalate
- **Observability:** log every thought/call/arg/result/cost — traces non-optional

---

## MCP — standardizing integration

N apps × M tools × bespoke glue → doesn't scale.

- **Server** — exposes a capability set (Jira, GitHub, DB) uniformly
- **Client** — any compliant AI app consumes it
- **Gateway** — fronts many servers: routing, authz, rate limits, circuit
  breaking, audit — one governed entry point

> The gateway is the natural place to enforce the safety envelope fleet-wide.
> (`ai-mcp-servers`: 200+ tools, circuit breakers, rate limits, audit.)

---

## Security & safety surface

Agents turn model mistakes into **actions with side effects**:

- **Prompt injection → tool abuse** — tool output is untrusted; constrain reachable tools
- **Excessive agency** — least privilege; gate destructive/spending actions
- **Blast radius** — assume it *will* err: read-only default, dry-run, spend caps, reversibility

---

## Next

**Lab:** build a bounded agent; find the propose/dispose boundary in code; break
reliability by raising step count; add a human-approval gate for a destructive tool.

**Module 6:** evals, guardrails, cost, security, bias — shipping responsibly.
