# Module 8 — Reinforcement Learning: AI That Learns to Beat a Game

> **Goal:** Understand *the entire process* by which an AI learns to play and
> win a game — starting from zero knowledge and ending superhuman. We'll trace
> every step: how the game is framed, how the agent perceives and acts, how a
> reward signal drives learning, the exact update rule that makes it improve,
> how it balances exploring vs. exploiting, and how this scales from a 16-cell
> grid to Atari, Go, and StarCraft. Then you'll watch a from-scratch agent go
> from random stumbling to a perfect winning path.
>
> This is the *predictive-to-prescriptive* bridge from Module 7 §7.7: there we
> named Markov Decision Processes; here we solve one.

---

## 8.1 The whole process in one paragraph

An AI learns to beat a game by **trial and error guided by a reward signal.** It
is never told the rules or the goal. It observes the game's current **state**,
takes an **action**, and receives a **reward** plus the next state. Over many
thousands of playthroughs it builds an estimate of how *valuable* each action is
in each state — where "valuable" means "leads to the most total future reward,
i.e. winning." Early on it acts almost randomly to *discover* what works
(exploration); later it increasingly does what it has learned is best
(exploitation). The learned mapping from state to best action is its **policy**.
That's the entire idea. Everything below is the mechanism that makes it work.

---

## 8.2 Step 1 — Frame the game as a Markov Decision Process (MDP)

Before any learning, you cast the game into five pieces. This framing is what
makes a game *learnable*.

- **States (S)** — everything the agent can observe about the current situation.
  For our grid: which cell it's in. For Atari: the last few frames of pixels.
  For chess: the board position.
- **Actions (A)** — the moves available. Grid: up/down/left/right. Atari: the
  joystick/button combos. Chess: the legal moves.
- **Transition (how the world responds)** — take action `a` in state `s`, land in
  a new state `s'`. The agent usually does *not* know this in advance; it finds
  out by trying.
- **Reward (R)** — a number the game hands back after each action. **This is the
  only teaching signal.** Design it to mean "winning": +1 for reaching the goal,
  −1 for dying, and a tiny −0.01 per step so the agent prefers *short* wins.
- **Discount factor (γ, gamma)** — how much the agent values future reward vs.
  immediate reward (typically 0.9–0.99). γ is what lets a move get credit for a
  win that happens 500 steps later.

> **Markov property:** the current state captures everything needed to decide
> the next action — history doesn't matter beyond what's encoded in the state.
> This assumption is what makes the math tractable.

---

## 8.3 Step 2 — What the agent is trying to compute: value

The agent's goal is to maximize **return** — the total discounted future reward
from now until the game ends:

```
return = r₁ + γ·r₂ + γ²·r₃ + γ³·r₄ + ...
```

To act well it needs to know the **value** of its choices. We track the
**action-value function Q(s, a)**: *"if I'm in state s and take action a (then
play well afterward), how much total future reward should I expect?"*

If you had the true Q, beating the game is trivial: in any state, pick the action
with the highest Q. **So the entire learning problem reduces to: estimate Q.**

For a small game, Q is literally a lookup table — one number per
(state, action) pair. Our grid has 16 states × 4 actions = 64 numbers. The agent
starts with all of them at 0 (knows nothing) and refines them.

---

## 8.4 Step 3 — The learning loop (what runs millions of times)

Every playthrough ("episode") runs this loop until the game ends:

```
1. Observe current state  s
2. Choose an action       a   (explore or exploit — see 8.5)
3. Take it; the game returns   next state s', reward r, done?
4. UPDATE the estimate Q(s, a) using r and s'   (see 8.6)
5. s ← s';  repeat until done
```

Run that loop over thousands of episodes and Q converges toward the truth. That's
it — that's the engine. The two pieces that make it *learn* rather than just
wander are the action choice (step 2) and the update (step 4).

---

## 8.5 Step 4 — Exploration vs. exploitation (the explore/exploit dilemma)

A chicken-and-egg problem: to learn which actions are good, the agent must try
them — but to win, it must use the good ones. Lean too hard on what you already
know and you get stuck in a mediocre strategy you happened to find first; explore
forever and you never cash in.

The standard fix is **ε-greedy with decay**:
- With probability **ε**, act **randomly** (explore).
- Otherwise, take the **best known** action, `argmax Q(s, a)` (exploit).
- **Decay ε over time:** start near 1.0 (almost all exploration — the agent knows
  nothing, so random is as good as anything) and shrink toward ~0.05 (mostly
  exploit the now-trustworthy policy).

This is exactly why, in the lab, the win rate is near-zero early (it's flailing
on purpose) and climbs steeply once ε drops and it starts committing to what it
learned.

---

## 8.6 Step 5 — The update rule that makes it improve (Q-learning)

This single line is where learning actually happens:

```
Q(s, a)  ←  Q(s, a)  +  α · [ r + γ · maxₐ' Q(s', a')  −  Q(s, a) ]
                             └─────────── target ───────────┘   └ old ┘
```

Read it as "nudge my old estimate toward a better one":
- `r + γ · maxₐ' Q(s', a')` is the **target**: the reward I just got, plus my
  best estimate of the value of where I landed (the *best* action available
  next). This is a **bootstrap** — the estimate improves itself using its own
  later estimates.
- The bracket is the **TD error** (temporal-difference error): how wrong my old
  estimate was. If it's positive, that action was better than I thought — raise
  its value.
- **α (alpha, learning rate)** controls how big a step to take (e.g. 0.1).

**How this solves credit assignment** (the hard part of beating a game): the +1
win reward lands only on the final move. But next episode, the move *before* the
win sees a high `maxₐ' Q(s', a')` and its own Q rises. The episode after, the move
before *that* rises. Value **propagates backward** along the winning path, one
step per visit, until early moves correctly "know" they lead to a win hundreds of
steps later. Watching the grid policy's arrows line up into a path is this
propagation made visible.

Key property: Q-learning is **off-policy** — it can explore randomly yet still
learn the *optimal* policy, because the update always bootstraps from the *best*
next action (`max`), not the one it happened to take.

---

## 8.7 Step 6 — Convergence: random → optimal

Repeat the loop enough and, under mild conditions (every state-action tried often
enough, α decayed appropriately), Q provably converges to the optimal values. The
**policy** is then just: in each state, take `argmax Q(s, a)`. The agent now beats
the game every time, by the shortest path the rewards incentivized. In the lab you
see the full arc: 2% → 88%+ win rate, ending with a clean pit-dodging route.

---

## 8.8 Step 7 — Scaling up: from a table to deep reinforcement learning

Our Q-table has 64 entries. A chess board has ~10⁴⁰ states; an Atari screen is
~10⁷ pixels per frame. You cannot tabulate that. The **only** thing that changes
for real games:

> **Replace the Q-table with a neural network** that *approximates* Q(s, a) from
> the raw state. Everything else — states, actions, rewards, the loop, explore/
> exploit, the TD-error update — stays conceptually the same.

This is **Deep Q-Networks (DQN)**, how DeepMind beat Atari from pixels in 2015.
Two engineering tricks make the neural version stable:
- **Experience replay** — store past (s, a, r, s') transitions and train on random
  batches, breaking correlation between consecutive frames.
- **Target network** — a periodically-frozen copy of the network provides the
  bootstrap target, so you're not chasing a moving goalpost.

The modern family tree from here:
- **Policy-gradient / actor-critic** methods (**PPO**, A3C, SAC) — learn the policy
  directly instead of via Q; **PPO is the workhorse** behind OpenAI Five (Dota 2)
  and much of RLHF for LLMs.
- **Planning + learning** — **AlphaGo/AlphaZero** combine a learned value/policy
  net with **Monte Carlo Tree Search** (simulate many futures, pick the best),
  trained by **self-play** so the opponent always matches the agent's skill. This
  is how it went from random to superhuman with *zero human games*.
- **Model-based** — **MuZero** additionally *learns the game's rules* (a model of
  transitions), then plans inside its own learned model — beating games without
  being told how they work.

---

## 8.9 Why beating a game is genuinely hard (and the gotchas)

- **Credit assignment** — connecting a reward to the action that earned it, moves
  earlier. Solved by value bootstrapping (8.6), but long-horizon games strain it.
- **Sparse reward** — if you only score on a win, the agent may *never* stumble
  onto one to learn from. Fixes: reward shaping (our −0.01 step cost), curiosity/
  exploration bonuses, curriculum learning, or demonstrations.
- **Reward hacking** — the agent maximizes the literal reward, not what you
  *meant*. Infamous case: a boat-racing agent that spun in circles hitting score
  pickups instead of finishing the race. **Your reward design *is* the goal
  definition** — get it wrong and the agent will exploit it.
- **Sample inefficiency** — RL can need millions to billions of frames; OpenAI
  Five played the equivalent of ~900 years of Dota per day across a huge cluster.
- **Instability / non-stationarity** — in self-play and multi-agent settings the
  target keeps moving; training can oscillate or collapse.
- **Sim-to-real gap** — a policy trained in simulation often breaks in the real
  world (relevant when RL moves from games to robotics).

---

## 8.10 Where this goes beyond games

Games are the testbed; the same machinery drives sequential decision-making
everywhere: robotics control, datacenter cooling, chip layout, recommendation,
trading, and — directly — **RLHF**, where reinforcement learning aligns LLMs to
human preferences (the "RL" in the model you're talking to). Learning to beat a
game and learning to be a helpful assistant are, mechanically, the same idea:
maximize a reward signal over a sequence of decisions.

---

## Terms, at working precision
- **MDP** — states, actions, rewards, transitions, discount; the formal frame.
- **Policy (π)** — the agent's state→action strategy; the thing you're learning.
- **Return** — total discounted future reward; what the agent maximizes.
- **Q(s, a)** — expected return from taking action a in state s, then acting well.
- **TD error** — gap between old estimate and bootstrapped target; drives updates.
- **ε-greedy** — explore randomly with prob. ε, else exploit the best known action.
- **Off-policy** — learns the optimal policy even while exploring (Q-learning).
- **DQN / PPO / AlphaZero / MuZero** — tabular Q scaled up with nets, policy
  gradients, self-play + search, and learned models, respectively.
- **Reward hacking** — maximizing the literal reward in unintended ways.

## Check yourself
1. Name the five pieces of the MDP framing and what the reward signal is *for*.
2. What does Q(s, a) represent, and why does estimating it solve the whole game?
3. Walk through the Q-learning update and explain how it assigns credit to a move
   made long before the win.
4. Why must ε start high and decay? What breaks if it's always 0? Always 1?
5. What single thing changes to go from our grid to Atari-from-pixels, and what
   stays the same?

➡️ **Lab:** run a from-scratch Q-learning agent (stdlib only — no PyTorch) and
watch it climb from a ~2% to ~90% win rate, then print the learned policy and the
exact winning path it discovered.
