# Module 9 — Beat the Chrome Dino Game (RL on a real game)

> **Goal:** Take the reinforcement-learning machinery from Module 8 and point it
> at a *real, recognizable game* — Chrome's offline T-Rex Runner (`chrome://dino`).
> You'll see why this game is the sweet spot for tabular RL, build the state
> representation that makes a lookup table enough, train an agent that goes from
> dying at the first cactus to surviving indefinitely, and understand exactly
> when you'd need to step up to deep RL from pixels (and how).
>
> This is the applied capstone to Module 8: same algorithm, real game, runs on a
> CPU with no dependencies.

---

## 9.1 Why the dino game, specifically

Three games get asked about constantly — Tetris, Mario, and the dino game. Only
one of them trains end-to-end on a normal laptop with zero dependencies, and it's
the dino:

| Game | Why it's hard to train locally |
|---|---|
| **Mario** | needs a NES emulator (`gym-super-mario-bros` + `nes-py`) **and** a deep CNN → PyTorch/GPU; Colab territory |
| **Tetris** | board-evaluation problem; strong play uses heuristic search, and it's provably unwinnable long-term |
| **Dino** | **low-dimensional state** → tabular Q-learning works → pure Python, trains in seconds |

The dino game's entire decision reduces to: *"is an obstacle coming, what kind,
and am I already in the air?"* That's a handful of numbers — not a screen of
pixels. Small state is the whole reason the Module 8 Q-table is enough here, and
why this is the right first "beat a real game" project.

> "Beat" here means what it means for Tetris too: the game **speeds up forever**,
> so it's eventually unwinnable. A trained agent going from score ~0 to surviving
> far longer than any human *is* beating it.

---

## 9.2 Framing the dino game as an MDP (recall §8.2)

- **State** — a *discretized* snapshot: time-to-impact of the next obstacle, its
  type (cactus vs. bird), and whether the dino is airborne.
- **Actions** — `RUN` (do nothing), `JUMP`, `DUCK`.
- **Reward** — **+1 per frame survived**, **−100 on collision**. That's the only
  teaching signal; the agent is never told that jumping clears a cactus.
- **Transition** — the physics: gravity pulls the dino down, obstacles scroll
  left at the current speed, speed ramps up every frame.
- **γ** — discounts future reward so "don't crash soon" is valued.

The agent's job, as always: estimate **Q(state, action)** and then act greedily.

---

## 9.3 The one design decision that makes or breaks it: the state

Naively you'd bucket the *raw distance* to the next obstacle. **That fails**,
and understanding why is the lesson of this module.

The dino's jump has a fixed **air time** (~20 frames in our sim). To clear a
cactus the agent must launch when the cactus is the right *time* away — but the
obstacle's *distance* at that moment depends on the current **speed**, which
keeps rising. So a fixed distance bucket means "jump now" at speed 3 and "jump
far too late" at speed 7. The table would need a separate entry for every speed,
and the agent would relearn jumping at each speed from scratch.

**The fix: measure distance in _frames-to-impact_ (distance ÷ speed), not raw
distance.** Now "jump when the cactus is 5–8 frames away" is a single rule that
holds at every speed. The state collapses from hundreds of speed-dependent cells
to about **20 total**, and the agent learns one clean policy that generalizes
across the whole speed ramp.

> This is feature engineering for RL: choosing a state representation in which
> the right action is a *simple, stable function of the state*. Get this right
> and a tiny table wins; get it wrong and even deep RL struggles.

The resulting state is `(time_bucket, obstacle_kind, airborne)` — small,
speed-invariant, and exactly enough to decide.

---

## 9.4 The learner (unchanged from Module 8)

Same tabular Q-learning, same update, same ε-greedy decay:

```
Q[s][a] ← Q[s][a] + α · ( r + γ·max Q[s'][a']  −  Q[s][a] )
```

- explore early (ε≈1.0): flail, discover that jumping clears cacti and ducking
  clears birds
- exploit late (ε≈0.02): run the learned policy
- the −100 crash penalty propagates **backward** to the states just before a
  crash, teaching the agent to act *before* the obstacle arrives — credit
  assignment again (§8.6)

Nothing about the algorithm changed. Only the environment and the state did. That
is the point: **the same RL core transfers from a toy grid to a real game** the
moment you give it a workable state.

---

## 9.5 What "learning" looks like here

Watch the policies in the lab:

| Policy | Result | Why |
|---|---|---|
| always RUN | ~64 | dies at the first cactus |
| always JUMP | ~125 | clears cacti, but crashes into birds and can't jump mid-air |
| always DUCK | ~81 | ducks birds, hits cacti |
| random | ~97 | occasionally right |
| **learned (greedy)** | **5000 (the cap)** | the *only* policy that jumps cacti **and** ducks birds **conditionally** |

The learned agent isn't doing one trick — it's choosing the right action *per
state*. That conditional behavior, discovered from reward alone, is the whole
demonstration.

---

## 9.6 When you'd need deep RL from pixels (and how)

Our agent is handed a clean state. The *famous* "AI learns the dino game" videos
don't get that — they learn **from the screen pixels**, which is harder and is
where deep RL earns its keep.

The deep-RL recipe (reproducible on **Google Colab**, since it needs PyTorch/GPU):
- **Environment** — wrap the real game (e.g. the `chrome-trex-rush` Python clone,
  or screen-capture `chrome://dino` via Selenium) in a Gym-style interface.
- **State** — stack the last 3–4 grayscale, downscaled frames so the network can
  infer velocity.
- **Network** — a small CNN maps frames → Q-values per action (a **DQN**, §8.8).
- **Stabilizers** — experience replay + a target network (§8.8).
- **Reward** — +1 per frame, −1 on death; train for ~1–2M frames.

Why we didn't do that here: PyTorch has **no wheel for this Intel macOS / Python
build**, and a CNN needs a GPU to train in reasonable time. The tabular version
teaches the same ideas, runs locally in seconds, and *actually beats the game* —
so it's the better lab. The pixel version is the natural "next step on Colab."

> Rule of thumb from Modules 7–9: **use the simplest representation that makes the
> decision easy.** Hand-crafted features + a table beat a neural net whenever you
> can get away with it. Reach for deep RL only when the state is genuinely
> high-dimensional (raw pixels, audio) and you can't engineer good features.

---

## 9.7 Failure modes specific to this game
- **Bad state design** (raw distance) — the #1 failure; see §9.3.
- **Unclearable spawns** — if obstacles can spawn closer than the jump air-time
  allows, *no* policy can win; the sim enforces a speed-scaled minimum gap so the
  game is always theoretically survivable (until speed outruns reaction).
- **Sparse/implicit penalty** — if the crash penalty is too small relative to the
  +1 survival reward, the agent won't learn to avoid obstacles; −100 vs +1 makes
  "don't crash" dominate.
- **Over-discretization** — too few buckets and distinct situations collapse into
  one state with no single right action; too many and the table is slow to fill.

---

## Terms, at working precision
- **Time-to-impact state** — distance ÷ speed; the speed-invariant feature that
  makes one policy work across the whole speed ramp.
- **Tabular RL** — Q stored as a lookup table; viable only for small state spaces.
- **DQN** — Q approximated by a neural net; needed when the state is pixels (§8.8).
- **Feature engineering for RL** — picking a representation in which the optimal
  action is a simple function of the state.

## Check yourself
1. Why does the dino game suit tabular Q-learning when Mario and Atari don't?
2. Explain precisely why raw distance fails as a state feature and time-to-impact
   fixes it.
3. What does the −100 vs +1 reward ratio accomplish, and what breaks if it's +1
   vs −1?
4. The learned greedy policy scores far higher than "always jump." What does that
   tell you about what it actually learned?
5. When *would* you switch this to a pixel-based DQN, and what three things would
   you add to make DQN train stably?

➡️ **Lab:** train the agent from zero, watch its score climb, then run the learned
policy against RUN-only / JUMP-only / DUCK-only / random baselines and see it be
the only one that survives indefinitely.
