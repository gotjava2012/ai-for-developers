# Module 8 — Reinforcement Learning: AI That Learns to Beat a Game

The entire process, from zero knowledge to superhuman.

---

## The whole idea in one breath

- The AI is **never told the rules or the goal**
- It **observes** a state → **acts** → gets a **reward** + next state
- Repeats thousands of times, learning which actions lead to **winning**
- Early: act randomly to *discover* (explore). Later: do what works (exploit)
- The learned state→action strategy is its **policy**

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

---

## Step 6 — Scaling: tabular → deep RL

- Grid: 64 table entries. Chess: ~10⁴⁰ states. Atari: millions of pixels
- **Only change: replace the Q-table with a neural net** that approximates Q
- Everything else stays the same → that's **DQN** (Atari from pixels, 2015)
- From here: **PPO** (policy gradients), **AlphaZero** (self-play + tree search),
  **MuZero** (learns the rules, then plans)

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
