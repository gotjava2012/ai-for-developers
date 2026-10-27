# Module 8 — Reinforcement Learning: AI That Learns to Beat a Game

The entire process, from zero knowledge to superhuman.

---

## The whole idea in one breath

- The AI is **never told the rules or the goal**
- It **observes** a state → **acts** → gets a **reward** + next state
- Repeats thousands of times, learning which actions lead to **winning**
- Early: act randomly to *discover* (explore). Later: do what works (exploit)
- The learned state→action strategy is its **policy**

```svg
<svg viewBox="0 0 640 200" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <rect x="40" y="70" width="180" height="60" rx="10" fill="#1f2a44"/>
  <text x="130" y="105" fill="#fff" font-size="20" text-anchor="middle" font-weight="bold">AGENT</text>
  <rect x="420" y="70" width="180" height="60" rx="10" fill="#2a7d5f"/>
  <text x="510" y="98" fill="#fff" font-size="18" text-anchor="middle" font-weight="bold">ENVIRONMENT</text>
  <text x="510" y="118" fill="#cfe9df" font-size="13" text-anchor="middle">(the game)</text>
  <!-- top arrow: action -->
  <path d="M220 85 H420" stroke="#1f2a44" stroke-width="3" fill="none" marker-end="url(#ar)"/>
  <text x="320" y="76" fill="#1f2a44" font-size="16" text-anchor="middle" font-weight="bold">action a</text>
  <!-- bottom arrow: reward + next state -->
  <path d="M420 118 H220" stroke="#2a7d5f" stroke-width="3" fill="none" marker-end="url(#ag)"/>
  <text x="320" y="140" fill="#2a7d5f" font-size="16" text-anchor="middle" font-weight="bold">reward r + next state s&#8242;</text>
  <defs>
    <marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#1f2a44"/></marker>
    <marker id="ag" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#2a7d5f"/></marker>
  </defs>
</svg>
```
<p class="diagram-caption">The core loop: act, observe reward + new state, repeat.</p>

> Trial and error, guided by a reward signal. Everything else is mechanism.

---

## Step 1 — Frame the game as an MDP

Five pieces that make a game *learnable*:

- **State** — what the agent observes (grid cell / Atari pixels / board)
- **Action** — the moves available
- **Transition** — how the world responds (agent learns this by trying)
- **Reward** — the *only* teaching signal: +1 win, −1 die, −0.01 per step
- **γ (discount)** — value future reward; lets a move get credit for a later win

---

## Step 2 — What it computes: value

**Q(s, a)** = "expected total future reward if I take action *a* in state *s*,
then keep playing well."

- Know the true Q → beating the game is trivial: pick `argmax Q(s, a)`
- So the whole problem reduces to: **estimate Q**
- Small game → Q is a lookup table (our grid: 16 × 4 = 64 numbers), starts at 0

```svg
<svg viewBox="0 0 520 235" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <!-- 4x4 grid, cell = 50px, origin 60,20 -->
  <g stroke="#cbd2e0" stroke-width="2">
    <!-- draw cells -->
    <!-- row backgrounds filled per special cell below; base cells white -->
  </g>
  <!-- base cells -->
  <g>
    <!-- generate 16 cells -->
    <rect x="60"  y="20"  width="50" height="50" fill="#eef4ff" stroke="#b9c4da"/>
    <rect x="110" y="20"  width="50" height="50" fill="#fff" stroke="#b9c4da"/>
    <rect x="160" y="20"  width="50" height="50" fill="#fff" stroke="#b9c4da"/>
    <rect x="210" y="20"  width="50" height="50" fill="#fff" stroke="#b9c4da"/>
    <rect x="60"  y="70"  width="50" height="50" fill="#fff" stroke="#b9c4da"/>
    <rect x="110" y="70"  width="50" height="50" fill="#c0392b" stroke="#b9c4da"/>
    <rect x="160" y="70"  width="50" height="50" fill="#fff" stroke="#b9c4da"/>
    <rect x="210" y="70"  width="50" height="50" fill="#fff" stroke="#b9c4da"/>
    <rect x="60"  y="120" width="50" height="50" fill="#fff" stroke="#b9c4da"/>
    <rect x="110" y="120" width="50" height="50" fill="#fff" stroke="#b9c4da"/>
    <rect x="160" y="120" width="50" height="50" fill="#fff" stroke="#b9c4da"/>
    <rect x="210" y="120" width="50" height="50" fill="#c0392b" stroke="#b9c4da"/>
    <rect x="60"  y="170" width="50" height="50" fill="#fff" stroke="#b9c4da"/>
    <rect x="110" y="170" width="50" height="50" fill="#c0392b" stroke="#b9c4da"/>
    <rect x="160" y="170" width="50" height="50" fill="#fff" stroke="#b9c4da"/>
    <rect x="210" y="170" width="50" height="50" fill="#2a7d5f" stroke="#b9c4da"/>
  </g>
  <text x="85"  y="52"  text-anchor="middle" font-size="18" font-weight="bold" fill="#1f2a44">S</text>
  <text x="235" y="202" text-anchor="middle" font-size="18" font-weight="bold" fill="#fff">G</text>
  <text x="135" y="102" text-anchor="middle" font-size="18" fill="#fff">#</text>
  <text x="235" y="152" text-anchor="middle" font-size="18" fill="#fff">#</text>
  <text x="135" y="202" text-anchor="middle" font-size="18" fill="#fff">#</text>
  <!-- learned winning path: (0,0)->(1,0)->(2,0)->(2,1)->(2,2)->(3,2)->(3,3) ; cell centers -->
  <polyline points="85,45 85,95 85,145 135,145 185,145 185,195 235,195"
            fill="none" stroke="#f0a500" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- legend -->
  <g font-size="14" fill="#333">
    <rect x="300" y="24" width="18" height="18" fill="#eef4ff" stroke="#b9c4da"/><text x="326" y="38">start</text>
    <rect x="300" y="52" width="18" height="18" fill="#2a7d5f"/><text x="326" y="66">goal (+1)</text>
    <rect x="300" y="80" width="18" height="18" fill="#c0392b"/><text x="326" y="94">pit (−1)</text>
    <line x1="300" y1="117" x2="318" y2="117" stroke="#f0a500" stroke-width="5"/><text x="326" y="122">learned path</text>
  </g>
</svg>
```
<p class="diagram-caption">The game, and the pit-dodging winning path the agent learned.</p>

---

## Step 3 — The learning loop (runs millions of times)

```
observe state s
choose action a      (explore or exploit)
take it → next state s', reward r, done?
UPDATE Q(s, a) from r and s'
s ← s'  ;  repeat until done
```

Two pieces make it *learn* rather than wander: the **action choice** and the
**update**.

---

## Step 4 — Explore vs. exploit

- To learn good actions you must **try** them; to win you must **use** them
- **ε-greedy:** with prob. ε act randomly, else take best known action
- **Decay ε:** ~1.0 early (knows nothing) → ~0.05 late (trust the policy)
- This is why win rate is near-zero early (flailing on purpose), then climbs

```svg
<svg viewBox="0 0 560 240" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <!-- axes -->
  <line x1="60" y1="200" x2="520" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="60" y1="200" x2="60"  y2="30"  stroke="#333" stroke-width="2"/>
  <text x="290" y="230" text-anchor="middle" font-size="14" fill="#333">training games →</text>
  <text x="24" y="120" text-anchor="middle" font-size="14" fill="#333" transform="rotate(-90 24 120)">win rate %</text>
  <!-- win-rate curve: (500,2.4) .. (5000,88.2) mapped to the plot box x:60..520 y:200..40 -->
  <polyline points="100,196 146,189 192,182 238,156 284,141 330,114 376,86 422,57 468,55 514,45"
            fill="none" stroke="#2a7d5f" stroke-width="4"/>
  <text x="500" y="40" text-anchor="end" font-size="13" fill="#2a7d5f" font-weight="bold">~90%</text>
  <text x="110" y="190" font-size="13" fill="#2a7d5f" font-weight="bold">~2%</text>
  <!-- epsilon decay line (dashed, high->low) across same box -->
  <polyline points="100,55 514,185" fill="none" stroke="#c0392b" stroke-width="3" stroke-dasharray="7 5"/>
  <text x="150" y="48" font-size="13" fill="#c0392b" font-weight="bold">ε high (explore)</text>
  <text x="440" y="178" font-size="13" fill="#c0392b" font-weight="bold" text-anchor="end">ε low (exploit)</text>
</svg>
```
<p class="diagram-caption">As ε decays (red), the agent stops flailing and the win rate (green) climbs.</p>

---

## Step 5 — The update that makes it improve

```
Q(s,a) ← Q(s,a) + α · [ r + γ·maxₐ' Q(s',a') − Q(s,a) ]
                        └──── target ────┘   └ old ┘
                        └──────── TD error ────────┘
```

- **Nudge** the old estimate toward reward + value of where you landed
- **Credit assignment:** value propagates *backward* along the winning path,
  one step per visit — early moves learn they lead to a far-off win
- **Off-policy:** explores randomly yet still learns the *optimal* policy

```svg
<svg viewBox="0 0 600 150" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <!-- 5 states along the winning path, reward at the end -->
  <g>
    <circle cx="70"  cy="70" r="26" fill="#eef4ff" stroke="#1f2a44" stroke-width="2"/>
    <circle cx="190" cy="70" r="26" fill="#eef4ff" stroke="#1f2a44" stroke-width="2"/>
    <circle cx="310" cy="70" r="26" fill="#eef4ff" stroke="#1f2a44" stroke-width="2"/>
    <circle cx="430" cy="70" r="26" fill="#eef4ff" stroke="#1f2a44" stroke-width="2"/>
    <circle cx="540" cy="70" r="30" fill="#2a7d5f" stroke="#1f2a44" stroke-width="2"/>
  </g>
  <text x="70"  y="76" text-anchor="middle" font-size="15" fill="#1f2a44">s₀</text>
  <text x="190" y="76" text-anchor="middle" font-size="15" fill="#1f2a44">s₁</text>
  <text x="310" y="76" text-anchor="middle" font-size="15" fill="#1f2a44">s₂</text>
  <text x="430" y="76" text-anchor="middle" font-size="15" fill="#1f2a44">s₃</text>
  <text x="540" y="68" text-anchor="middle" font-size="15" fill="#fff" font-weight="bold">WIN</text>
  <text x="540" y="84" text-anchor="middle" font-size="12" fill="#cfe9df">+1</text>
  <!-- forward moves (grey) -->
  <g stroke="#b9c4da" stroke-width="2" fill="none">
    <line x1="96" y1="70" x2="164" y2="70"/><line x1="216" y1="70" x2="284" y2="70"/>
    <line x1="336" y1="70" x2="404" y2="70"/><line x1="456" y1="70" x2="510" y2="70"/>
  </g>
  <!-- backward value propagation (orange, curved, above) -->
  <g stroke="#f0a500" stroke-width="3" fill="none" marker-end="url(#bk)">
    <path d="M512 48 Q470 18 434 44"/>
    <path d="M404 48 Q350 18 314 44"/>
    <path d="M284 48 Q230 18 194 44"/>
    <path d="M164 48 Q110 18 74 44"/>
  </g>
  <text x="300" y="120" text-anchor="middle" font-size="14" fill="#f0a500" font-weight="bold">value flows backward, one step per visit — early moves learn they lead to the win</text>
  <defs><marker id="bk" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#f0a500"/></marker></defs>
</svg>
```
<p class="diagram-caption">Credit assignment: the +1 at the goal propagates back along the path.</p>

---

## Step 6 — Scaling: tabular → deep RL

- Grid: 64 table entries. Chess: ~10⁴⁰ states. Atari: millions of pixels
- **Only change: replace the Q-table with a neural net** that approximates Q
- Everything else stays the same → that's **DQN** (Atari from pixels, 2015)
- From here: **PPO** (policy gradients), **AlphaZero** (self-play + tree search),
  **MuZero** (learns the rules, then plans)

```svg
<svg viewBox="0 0 620 210" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <!-- left: Q-table -->
  <text x="130" y="24" text-anchor="middle" font-size="16" font-weight="bold" fill="#1f2a44">Small game: Q-table</text>
  <g font-size="13">
    <rect x="40" y="36" width="180" height="140" fill="#fff" stroke="#b9c4da"/>
    <line x1="40" y1="64" x2="220" y2="64" stroke="#b9c4da"/>
    <line x1="100" y1="36" x2="100" y2="176" stroke="#b9c4da"/>
    <text x="70" y="56" text-anchor="middle" fill="#555">state</text>
    <text x="160" y="56" text-anchor="middle" fill="#555">Q(U/D/L/R)</text>
    <text x="70" y="86" text-anchor="middle">s₀</text><text x="160" y="86" text-anchor="middle">.3 .9 .1 .5</text>
    <text x="70" y="112" text-anchor="middle">s₁</text><text x="160" y="112" text-anchor="middle">.7 .2 .4 .8</text>
    <text x="70" y="138" text-anchor="middle">s₂</text><text x="160" y="138" text-anchor="middle">.1 .6 .9 .3</text>
    <text x="70" y="164" text-anchor="middle">…</text><text x="160" y="164" text-anchor="middle">… 64 numbers</text>
  </g>
  <!-- arrow -->
  <path d="M240 106 H330" stroke="#1f2a44" stroke-width="3" fill="none" marker-end="url(#a2)"/>
  <text x="285" y="96" text-anchor="middle" font-size="13" fill="#1f2a44">too many states?</text>
  <text x="285" y="128" text-anchor="middle" font-size="12" fill="#555">10⁴⁰ / pixels</text>
  <!-- right: neural net approximating Q -->
  <text x="490" y="24" text-anchor="middle" font-size="16" font-weight="bold" fill="#2a7d5f">Real game: neural net ≈ Q</text>
  <g fill="#2a7d5f">
    <circle cx="360" cy="70" r="9"/><circle cx="360" cy="106" r="9"/><circle cx="360" cy="142" r="9"/>
    <circle cx="440" cy="60" r="9"/><circle cx="440" cy="94" r="9"/><circle cx="440" cy="128" r="9"/><circle cx="440" cy="162" r="9"/>
    <circle cx="520" cy="88" r="9"/><circle cx="520" cy="124" r="9"/>
    <circle cx="600" cy="106" r="9"/>
  </g>
  <g stroke="#b9c4da" stroke-width="1">
    <line x1="360" y1="70" x2="440" y2="60"/><line x1="360" y1="70" x2="440" y2="128"/>
    <line x1="360" y1="106" x2="440" y2="94"/><line x1="360" y1="142" x2="440" y2="162"/>
    <line x1="440" y1="60" x2="520" y2="88"/><line x1="440" y1="128" x2="520" y2="124"/>
    <line x1="440" y1="94" x2="520" y2="88"/><line x1="440" y1="162" x2="520" y2="124"/>
    <line x1="520" y1="88" x2="600" y2="106"/><line x1="520" y1="124" x2="600" y2="106"/>
  </g>
  <text x="352" y="186" font-size="12" fill="#555">state in</text>
  <text x="600" y="134" text-anchor="middle" font-size="12" fill="#555">Q out</text>
  <defs><marker id="a2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#1f2a44"/></marker></defs>
</svg>
```
<p class="diagram-caption">The one change for deep RL: swap the table for a network. Everything else stays.</p>

---

## The milestones

| AI | Game | Result |
|---|---|---|
| DQN | 49 Atari games | human-level from raw pixels |
| AlphaGo → AlphaZero | Go/chess/shogi | superhuman from **self-play only** |
| OpenAI Five | Dota 2 | beat world champions |
| MuZero | Atari + board | won **without being told the rules** |

---

## Gotchas (why it's genuinely hard)

- **Sparse reward** — never stumbles on a win to learn from → shape rewards
- **Reward hacking** — maximizes the *literal* reward, not what you meant
- **Sample inefficiency** — millions–billions of frames (OpenAI Five: ~900 yrs/day)
- **Your reward design *is* the goal definition** — get it wrong, it exploits it

---

## Beyond games

- Same machinery: robotics, chip layout, datacenter cooling, trading
- **RLHF** — the "RL" that aligns LLMs to human preferences
- Beating a game and being a helpful assistant are mechanically the same:
  maximize a reward over a sequence of decisions

---

## Lab

Run a from-scratch Q-learning agent — **stdlib only, no PyTorch**:

- watch win rate climb **~2% → ~90%**
- print the **learned policy** (arrows) and the exact **winning path**
- it was never told the rules — only +1 / −1
