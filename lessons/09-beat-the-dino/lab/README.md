# Module 9 Lab — beat the Chrome dino game

A self-contained simulator of Chrome's offline T-Rex Runner plus a Q-learning
agent that teaches itself **when to jump and when to duck** — from a reward signal
alone. It starts dying at the first cactus and ends surviving indefinitely.
**Pure Python standard library — no PyTorch, no emulator, no pip install.**

## Run it
```bash
python3 dino_q_learning.py
```

---

## What you'll see

### 1. It learns — average score climbs during training
```
after   500 games:  avg score   106.8
after  4000 games:  avg score   250.1  ##
```
The training average stays modest **because training still includes random
exploration moves** (ε). The real result shows up when exploration is turned off.

### 2. The learned policy beats the game
```
Playing 5 games with the LEARNED policy (no exploration):
  game 1: survived 5000 frames  (hit the 5000-frame cap — effectively unbeatable now)
  ... all 5 games: 5000 ...
```
With ε=0, the greedy policy clears the full 5000-frame cap every game. The game
speeds up forever, so like Tetris it's eventually unwinnable — but surviving the
cap every time is "beating it."

### 3. It beat every simple baseline (run this to confirm)
```
always RUN    avg≈64    dies at the first cactus
always JUMP   avg≈125   clears cacti, crashes into birds
always DUCK   avg≈81    ducks birds, hits cacti
random        avg≈97
learned       5000      jumps cacti AND ducks birds — conditionally
```
The learned agent is the **only** policy that picks the right action per state.
That conditional behavior, learned from +1/−100 alone, is the whole point.

---

## Map the code to the guide
- **MDP framing (§9.2)** — `DinoGame.step()` returns `(state, reward, done)`
- **The state decision (§9.3)** — `_state()` buckets **time-to-impact = x / speed**,
  *not* raw distance. This is the lesson of the module.
- **The learner (§9.4)** — the Q-learning update in `train()`:
  ```python
  q(s)[a] += alpha * (r + gamma * max(q(ns)) - q(s)[a])
  ```
- **Reward (§9.2)** — `+1.0` per surviving frame, `-100.0` on collision

---

## Exercises
1. **Break the state (see §9.3 fail live).** In `_state()`, replace time-to-impact
   with raw `dist = o["x"]` bucketed by fixed thresholds. Retrain and watch the
   greedy score collapse as speed rises — the table can't represent one rule.
2. **Weaken the penalty.** Change the crash reward from `-100` to `-1`. The agent
   stops reliably avoiding obstacles — the +1 survival reward no longer dominates.
3. **Make it harder.** Raise `SPEED_RAMP` (e.g. `0.002`) or `START_SPEED`. Find the
   point where even the learned policy can't survive the cap — the "killscreen."
4. **More birds.** Lower the cactus probability in `_spawn` (currently `0.75`) so
   ducking matters more; confirm the agent still learns both actions.
5. **Add a feature (harder).** Add a second upcoming obstacle to the state so the
   agent can plan two obstacles ahead; measure whether top speed improves.

---

## Takeaways
- Same Q-learning as Module 8 — only the **environment** and **state** changed.
- The make-or-break choice is the **state representation**: time-to-impact makes
  one policy work at every speed; raw distance does not.
- Tabular RL **beats a real game** here precisely because the state is small —
  reach for deep RL (pixels, §9.6) only when you can't engineer features like this.

## Tie it together
- This is **Module 8**'s algorithm on a real game.
- §9.6 sketches the **DQN-from-pixels** version (Colab) — the same idea scaled up
  with a neural net when the state is the raw screen.
