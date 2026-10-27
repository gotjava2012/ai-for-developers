# Module 8 Lab — an AI that learns to beat a game

Watch a Q-learning agent go from knowing **nothing** to winning a grid-world game
every time. It's never told the rules, the goal, or that the pits are bad — it
learns entirely from a +1 / −1 reward signal. **Pure Python standard library, no
PyTorch, no pip install.**

## Run it
```bash
python3 q_learning_game.py
```

## The game (4×4 grid)
```
S . . .     S = start (top-left)
. # . .     G = goal  (+1, WIN)
. . . #     # = pit   (−1, LOSE)
. # . G     each step costs −0.01, so it learns the SHORT path
```

---

## What you'll see (and what it means)

### 1. It learns — win rate climbs from ~2% to ~90%
```
after   500 games:    2.4%
after  2500 games:   30.2%  ############
after  5000 games:   88.2%  ###################################
```
Early on it's near-zero **on purpose** — ε (exploration) is high, so it's acting
mostly at random to *discover* the game. As ε decays it starts exploiting what it
learned, and the win rate climbs. That rising curve **is** learning.

### 2. The learned policy — an arrow in every cell
```
↓  →  ↓  ←
↓  #  ↓  ←
→  →  ↓  #
↑  #  →  G
```
This is the **policy**: from each cell, the action with the highest learned Q. Read
it and you'll see the arrows form a route to `G` that routes *around* the `#` pits.

### 3. The exact winning path it discovered
```
Playing with the learned policy: WON 🏆
path: (0,0) -> (1,0) -> (2,0) -> (2,1) -> (2,2) -> (3,2) -> (3,3)
```
Following its own policy greedily (no randomness), it reaches the goal by a short,
pit-free path — one it was never shown.

---

## Map the code to the guide
Open `q_learning_game.py` and find each piece of the process from the guide:

- **MDP framing (§8.2)** — `step()` is the environment: state → `(next_state, reward, done)`
- **Q-table / value (§8.3)** — `Q = {state: {action: 0.0}}`, all zeros at the start
- **The loop (§8.4)** — the `while not done` block inside `train()`
- **Explore vs. exploit (§8.5)** — `eps` decays each episode; `random.random() < eps`
- **The update (§8.6)** — the one line:
  ```python
  Q[state][action] += alpha * (reward + gamma * best_next - Q[state][action])
  ```
- **Policy (§8.7)** — `greedy_action()` = `argmax Q[state]`

---

## Exercises
1. **Kill exploration.** Set `eps_start=0.0`. Watch it get stuck — with no
   exploration it never discovers the winning path. This *is* the explore/exploit
   dilemma from §8.5.
2. **Kill the future.** Set `gamma=0.0` so it only values immediate reward. It can
   no longer credit a move for a win many steps later — credit assignment breaks.
3. **Move the goal or add a pit.** Change `GOAL` / `PITS` and confirm it relearns a
   new winning policy. Nothing was hard-coded — it's all learned.
4. **Watch value propagate.** Print `Q[START]` every 500 episodes and watch the
   value of the start cell rise as the win signal flows backward along the path.
5. **Scale the idea (harder).** Grow the grid to 8×8. The table still works but
   training takes longer — this is exactly why real games swap the table for a
   neural net (DQN, §8.8).

---

## Takeaways
- Started random (~2% wins), ended near 100% → it **learned**, no rules given.
- The **Q-table is the learned strategy**; deep RL just replaces it with a neural
  net to scale from 16 cells to millions of pixels.
- **ε decay** = explore early, exploit later. **γ** = value the future, which is
  what makes long-horizon winning possible.

## Tie it together
- This is the MDP from **Module 7 §7.7**, actually solved.
- The reward-maximization loop here is the same idea as **RLHF**, which aligns the
  LLMs from **Modules 3–6** to human preferences.
