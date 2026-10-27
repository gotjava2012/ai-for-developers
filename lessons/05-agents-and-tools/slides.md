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

```svg
<svg viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <rect x="200" y="20" width="200" height="46" rx="10" fill="#1f2a44"/>
  <text x="300" y="40" text-anchor="middle" font-size="15" fill="#fff" font-weight="bold">LLM</text>
  <text x="300" y="58" text-anchor="middle" font-size="12" fill="#cfe9df">proposes a tool call</text>
  <rect x="200" y="140" width="200" height="46" rx="10" fill="#2a7d5f"/>
  <text x="300" y="160" text-anchor="middle" font-size="14" fill="#fff" font-weight="bold">YOUR RUNTIME</text>
  <text x="300" y="178" text-anchor="middle" font-size="11" fill="#cfe9df">validate · authz · execute</text>
  <rect x="470" y="83" width="110" height="40" rx="8" fill="#fdf3e6" stroke="#f0a500"/>
  <text x="525" y="107" text-anchor="middle" font-size="13" fill="#b9770a">tools / APIs</text>
  <!-- loop arrows -->
  <path d="M260 66 V140" stroke="#1f2a44" stroke-width="2.5" fill="none" marker-end="url(#m1)"/>
  <text x="150" y="108" font-size="12" fill="#1f2a44">tool call ↓</text>
  <path d="M340 140 V66" stroke="#2a7d5f" stroke-width="2.5" fill="none" marker-end="url(#m2)"/>
  <text x="352" y="108" font-size="12" fill="#2a7d5f">result ↑ (append, continue)</text>
  <path d="M400 158 H470 V123" stroke="#2a7d5f" stroke-width="2.5" fill="none" marker-end="url(#m2)"/>
  <path d="M470 103 H440 V123 Z" fill="none"/>
  <path d="M470 90 H410" stroke="#f0a500" stroke-width="2.5" fill="none" marker-end="url(#m3)"/>
  <text x="300" y="112" text-anchor="middle" font-size="12" fill="#c0392b" font-weight="bold">← the security boundary →</text>
  <defs>
    <marker id="m1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#1f2a44"/></marker>
    <marker id="m2" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#2a7d5f"/></marker>
    <marker id="m3" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#f0a500"/></marker>
  </defs>
</svg>
```
<p class="diagram-caption">Agent = LLM + tools + a loop. Your code — not the prompt — is the gate between them.</p>

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

```svg
<svg viewBox="0 0 560 150" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <line x1="50" y1="120" x2="520" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="50" y1="120" x2="50" y2="20" stroke="#333" stroke-width="2"/>
  <text x="285" y="144" text-anchor="middle" font-size="12" fill="#333">number of chained steps →</text>
  <!-- bars: 0.9^n -->
  <g fill="#c0392b">
    <rect x="80"  y="30"  width="40" height="90" opacity=".55"/>
    <rect x="160" y="39"  width="40" height="81" opacity=".62"/>
    <rect x="240" y="47"  width="40" height="73" opacity=".7"/>
    <rect x="320" y="54"  width="40" height="66" opacity=".8"/>
    <rect x="400" y="61"  width="40" height="59" opacity=".9"/>
  </g>
  <g font-size="12" fill="#1a1a1a" text-anchor="middle">
    <text x="100" y="24">90%</text><text x="180" y="33">81%</text><text x="260" y="41">73%</text>
    <text x="340" y="48">66%</text><text x="420" y="55">59%</text>
  </g>
  <g font-size="12" fill="#555" text-anchor="middle">
    <text x="100" y="135">1</text><text x="180" y="135">2</text><text x="260" y="135">3</text>
    <text x="340" y="135">4</text><text x="420" y="135">5</text>
  </g>
</svg>
```
<p class="diagram-caption">Each step is a coin-flip against you: 90% per step collapses to ~59% over five steps.</p>
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
