"""
Module 8 Lab — an AI that LEARNS to beat a game, from scratch.

A tabular Q-learning agent learns to win a small grid-world game knowing
*nothing* up front: not the rules, not where the goal is, not even that falling
in the pit is bad. It discovers a winning policy purely from a reward signal
through trial and error — the core loop behind every game-playing AI from Atari
DQN to AlphaZero, just small enough to read and run on a CPU in seconds.

No PyTorch, no pip install — Python standard library only.
    python3 q_learning_game.py

THE GAME (4x4 grid):
    S . . .        S = start (top-left)
    . # . .        G = goal  (+1, you win)
    . . . #        # = pit   (-1, you lose)
    . # . G        move U/D/L/R; each step costs a tiny -0.01 (find the SHORT path)
"""

import random

random.seed(42)

# --- The game (environment) -------------------------------------------------
GRID = 4
START = (0, 0)
GOAL = (3, 3)
PITS = {(1, 1), (2, 3), (3, 1)}
ACTIONS = ["U", "D", "L", "R"]
MOVES = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


def step(state, action):
    """Apply an action. Returns (next_state, reward, done)."""
    dr, dc = MOVES[action]
    r = max(0, min(GRID - 1, state[0] + dr))
    c = max(0, min(GRID - 1, state[1] + dc))
    ns = (r, c)
    if ns == GOAL:
        return ns, 1.0, True        # WIN
    if ns in PITS:
        return ns, -1.0, True       # LOSE
    return ns, -0.01, False         # small step cost -> prefer short paths


# --- The learner (Q-learning agent) -----------------------------------------
def train(episodes=5000, alpha=0.1, gamma=0.95,
          eps_start=1.0, eps_end=0.05):
    """Learn Q[state][action] = expected total future reward."""
    Q = {(r, c): {a: 0.0 for a in ACTIONS}
         for r in range(GRID) for c in range(GRID)}
    wins = 0
    history = []  # (episode_block, win_rate) so we can watch it improve

    for ep in range(episodes):
        # epsilon decays: explore a lot early, exploit what we learned later
        eps = eps_end + (eps_start - eps_end) * (1 - ep / episodes)
        state, done, steps = START, False, 0

        while not done and steps < 100:
            # choose action: explore (random) or exploit (best known)
            if random.random() < eps:
                action = random.choice(ACTIONS)
            else:
                action = max(Q[state], key=Q[state].get)

            next_state, reward, done = step(state, action)

            # Q-learning update: nudge toward reward + discounted best future
            best_next = max(Q[next_state].values())
            Q[state][action] += alpha * (
                reward + gamma * best_next - Q[state][action])

            state = next_state
            steps += 1

        if done and state == GOAL:
            wins += 1
        if (ep + 1) % 500 == 0:
            history.append((ep + 1, wins / 500))
            wins = 0

    return Q, history


# --- Show what it learned ----------------------------------------------------
def greedy_action(Q, state):
    return max(Q[state], key=Q[state].get)


def render_policy(Q):
    arrows = {"U": "↑", "D": "↓", "L": "←", "R": "→"}
    print("Learned policy (the arrow it would follow from each cell):")
    for r in range(GRID):
        row = []
        for c in range(GRID):
            if (r, c) == GOAL:
                row.append("G")
            elif (r, c) in PITS:
                row.append("#")
            else:
                row.append(arrows[greedy_action(Q, (r, c))])
        print("   " + "  ".join(row))


def play_greedy(Q):
    """Follow the learned policy once and report the path + outcome."""
    state, done, path, steps = START, False, [START], 0
    while not done and steps < 50:
        state, _, done = step(state, greedy_action(Q, state))
        path.append(state)
        steps += 1
    outcome = "WON 🏆" if state == GOAL else ("fell in pit" if state in PITS
                                              else "gave up")
    return path, outcome


def main():
    print("Training an agent that starts with ZERO knowledge of the game...\n")
    Q, history = train()

    print("Win rate over training (watch it learn to beat the game):")
    for ep, rate in history:
        bar = "#" * int(rate * 40)
        print(f"  after {ep:5d} games:  {rate*100:5.1f}%  {bar}")
    print()

    render_policy(Q)
    print()

    path, outcome = play_greedy(Q)
    print(f"Playing with the learned policy: {outcome}")
    print("  path:", " -> ".join(str(p) for p in path))
    print()

    print("TAKEAWAYS")
    print("  - started random (~early win rate low), ended near 100% = it LEARNED")
    print("  - it was never told the rules — only a reward signal (+1 win / -1 pit)")
    print("  - epsilon decay = explore early, exploit the learned policy later")
    print("  - the Q-table IS the learned strategy; deep RL just replaces it")
    print("    with a neural net to scale from 16 cells to millions of pixels")


if __name__ == "__main__":
    main()
