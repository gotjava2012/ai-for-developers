# Module 9 — Beat the Chrome Dino Game

RL from Module 8, pointed at a real game — and it actually wins.

---

## Why the dino game (of all games)

- **Mario** → NES emulator + deep CNN → PyTorch/GPU (Colab territory)
- **Tetris** → board-evaluation + search; provably unwinnable long-term
- **Dino** → **low-dimensional state** → a Q-table is enough → pure Python, trains in seconds

> The whole decision is: *obstacle coming? what kind? am I airborne?* —
> a few numbers, not a screen of pixels. That's why tabular RL works here.

---

## The game as an MDP (recall §8.2)

```svg
<svg viewBox="0 0 620 200" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <!-- ground -->
  <line x1="20" y1="150" x2="600" y2="150" stroke="#555" stroke-width="2"/>
  <!-- dino -->
  <rect x="60" y="118" width="30" height="32" rx="4" fill="#2a7d5f"/>
  <text x="75" y="168" text-anchor="middle" font-size="12" fill="#2a7d5f" font-weight="bold">dino</text>
  <!-- cactus -->
  <rect x="330" y="120" width="16" height="30" fill="#c0392b"/>
  <text x="338" y="168" text-anchor="middle" font-size="11" fill="#c0392b">cactus</text>
  <!-- bird -->
  <polygon points="500,96 516,104 500,112" fill="#1f2a44"/>
  <text x="508" y="90" text-anchor="middle" font-size="11" fill="#1f2a44">bird</text>
  <!-- distance arrow (above ground, clear of boxes) -->
  <path d="M95 104 H326" stroke="#f0a500" stroke-width="2" fill="none" marker-end="url(#d1)"/>
  <text x="210" y="98" text-anchor="middle" font-size="12" fill="#b9770a" font-weight="bold">time-to-impact</text>
  <!-- scroll arrow -->
  <path d="M560 135 H470" stroke="#555" stroke-width="2" fill="none" marker-end="url(#d2)"/>
  <text x="520" y="130" text-anchor="middle" font-size="11" fill="#555">scroll (speed ↑)</text>
  <!-- actions -->
  <text x="75" y="192" text-anchor="middle" font-size="11" fill="#333">RUN · JUMP · DUCK</text>
  <text x="430" y="192" text-anchor="middle" font-size="11" fill="#333">reward = +1 / frame,  −100 on crash</text>
  <defs>
    <marker id="d1" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#f0a500"/></marker>
    <marker id="d2" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#555"/></marker>
  </defs>
</svg>
```
<p class="diagram-caption">State = (time-to-impact, obstacle kind, airborne). Actions = run/jump/duck. Reward = survive.</p>

---

## The one decision that makes or breaks it: the state

- Naive: bucket the **raw distance** to the next obstacle → **fails**
- The jump has fixed **air time**; the distance to launch at depends on **speed**,
  which keeps rising → one table cell means "jump now" at slow speed, "too late" at fast
- **Fix:** bucket **time-to-impact = distance ÷ speed** → one rule works at every speed
- State collapses to **~20 cells**; the agent learns **one** policy that generalizes

---

## Raw distance fails; time-to-impact works

```svg
<svg viewBox="0 0 620 210" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <!-- LEFT: raw distance -->
  <text x="155" y="20" text-anchor="middle" font-size="14" font-weight="bold" fill="#c0392b">Raw distance (fails)</text>
  <line x1="30" y1="70" x2="280" y2="70" stroke="#555" stroke-width="2"/>
  <rect x="40" y="52" width="20" height="18" rx="3" fill="#2a7d5f"/>
  <rect x="150" y="50" width="12" height="20" fill="#c0392b"/>
  <text x="105" y="44" text-anchor="middle" font-size="11" fill="#b9770a">dist = 110</text>
  <path d="M60 80 H150" stroke="#f0a500" stroke-width="2" fill="none"/>
  <text x="155" y="104" text-anchor="middle" font-size="11" fill="#2a7d5f">slow: jump now ✓</text>
  <line x1="30" y1="150" x2="280" y2="150" stroke="#555" stroke-width="2"/>
  <rect x="40" y="132" width="20" height="18" rx="3" fill="#2a7d5f"/>
  <rect x="150" y="130" width="12" height="20" fill="#c0392b"/>
  <text x="105" y="124" text-anchor="middle" font-size="11" fill="#b9770a">dist = 110</text>
  <path d="M60 160 H150" stroke="#f0a500" stroke-width="2" fill="none"/>
  <text x="165" y="184" text-anchor="middle" font-size="11" fill="#c0392b">fast: same cell, but too late ✗</text>
  <!-- divider -->
  <line x1="310" y1="20" x2="310" y2="195" stroke="#ccc"/>
  <!-- RIGHT: time to impact -->
  <text x="470" y="20" text-anchor="middle" font-size="14" font-weight="bold" fill="#2a7d5f">Time-to-impact (works)</text>
  <text x="470" y="52" text-anchor="middle" font-size="13" fill="#333">ttc = distance ÷ speed</text>
  <rect x="360" y="70" width="220" height="30" rx="5" fill="#eafaf3" stroke="#2a7d5f"/>
  <text x="470" y="90" text-anchor="middle" font-size="12" fill="#1d6a4f">"jump when ttc ≈ 5–8 frames"</text>
  <text x="470" y="128" text-anchor="middle" font-size="12" fill="#333">one rule — holds at every speed</text>
  <text x="470" y="162" text-anchor="middle" font-size="12" fill="#2a7d5f" font-weight="bold">~20 states total</text>
</svg>
```
<p class="diagram-caption">Feature engineering for RL: pick a state where the right action is a stable rule.</p>

---

## The learner — unchanged from Module 8

```
Q[s][a] ← Q[s][a] + α · ( r + γ·max Q[s'][a'] − Q[s][a] )
```

- explore early (ε≈1.0): discover jumping clears cacti, ducking clears birds
- exploit late (ε≈0.02): run the learned policy
- the **−100** crash penalty propagates **backward** → act *before* the obstacle

> Only the environment and the state changed. The RL core is identical —
> that's the point: it transfers from a toy grid to a real game.

---

## What it learned (lab result)

```svg
<svg viewBox="0 0 600 220" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <line x1="150" y1="190" x2="580" y2="190" stroke="#333" stroke-width="2"/>
  <!-- bars (scaled: 5000 -> 150px wide max) -->
  <g>
    <rect x="150" y="30"  width="64"  height="22" fill="#c0392b"/><text x="222" y="46" font-size="12">64</text>
    <rect x="150" y="62"  width="125" height="22" fill="#e67e22"/><text x="283" y="78" font-size="12">125</text>
    <rect x="150" y="94"  width="81"  height="22" fill="#e67e22"/><text x="239" y="110" font-size="12">81</text>
    <rect x="150" y="126" width="97"  height="22" fill="#f0a500"/><text x="255" y="142" font-size="12">97</text>
    <rect x="150" y="158" width="420" height="22" fill="#2a7d5f"/><text x="470" y="174" font-size="12" fill="#fff" font-weight="bold">5000 (the cap)</text>
  </g>
  <g font-size="12" fill="#333" text-anchor="end">
    <text x="144" y="46">always RUN</text>
    <text x="144" y="78">always JUMP</text>
    <text x="144" y="110">always DUCK</text>
    <text x="144" y="142">random</text>
    <text x="144" y="174" font-weight="bold" fill="#2a7d5f">learned</text>
  </g>
  <text x="365" y="212" text-anchor="middle" font-size="12" fill="#555">frames survived (greedy policy, 5 games)</text>
</svg>
```
<p class="diagram-caption">The learned policy is the only one that jumps cacti AND ducks birds conditionally.</p>

---

## When you'd need deep RL from pixels

- Our agent gets a **clean state**; the famous videos learn **from the screen**
- Deep-RL recipe (on **Colab**, needs PyTorch/GPU):
  - wrap the game in a Gym interface; stack 3–4 grayscale frames (for velocity)
  - small **CNN → Q-values** (a DQN); add **experience replay** + **target network**
  - +1/frame, −1 on death; ~1–2M frames
- Local tabular version teaches the same ideas, runs in seconds, **and wins**

> **Use the simplest representation that makes the decision easy.** Reach for deep
> RL only when the state is genuinely pixels/audio and features won't do.

---

## Lab

Pure stdlib — no PyTorch, no emulator, no install:

- train from zero → watch avg score climb
- run the learned policy vs RUN-only / JUMP-only / DUCK-only / random
- the learned agent survives the **5000-frame cap** every game — effectively unbeatable
