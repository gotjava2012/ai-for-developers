"""
Module 9 Lab — an AI that learns to beat the Chrome "dino" game.

A self-contained simulator of Chrome's offline T-Rex Runner (chrome://dino) plus
a tabular Q-learning agent that learns, from a reward signal alone, WHEN to jump
and when to duck. It starts dying at the first cactus and ends surviving
essentially forever (the game speeds up, so like real Tetris it's eventually
unwinnable — but the agent goes from a score of ~0 to thousands).

Why tabular Q-learning works here (unlike Mario/Atari): the decision is
low-dimensional — distance to the next obstacle, its type, and the current speed.
We bucket those into a small discrete state, so a lookup table suffices. This is
exactly Module 8's algorithm applied to a real game.

Pure Python standard library. No PyTorch, no emulator, no pip install.
    python3 dino_q_learning.py
"""

import random

random.seed(7)

# --- The game (a faithful-but-minimal T-Rex Runner) -------------------------
GROUND = 0.0
GRAVITY = 0.9
JUMP_V = 9.0          # initial jump velocity (air time ~20 frames)
START_SPEED = 3.0     # world scroll speed (obstacles move left this fast)
SPEED_RAMP = 0.0008   # speed increases every frame -> game gets harder
MAX_STEPS = 5000      # cap an episode (a "win" if it survives this long)

# actions
RUN, JUMP, DUCK = 0, 1, 2
ACTIONS = [RUN, JUMP, DUCK]


class DinoGame:
    """Minimal T-Rex Runner. Obstacles are cacti (jump) or birds (duck)."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.y = GROUND          # dino vertical position
        self.vy = 0.0            # vertical velocity
        self.ducking = False
        self.speed = START_SPEED
        self.steps = 0
        self.score = 0
        self.obstacles = []      # list of dicts: x, kind ('cactus'|'bird'), h
        self._spawn(initial=True)
        return self._state()

    def _spawn(self, initial=False):
        # place the next obstacle ahead, with enough gap to be clearable
        # (air time is ~20 frames; at higher speed that's a longer world-gap)
        min_gap = int(self.speed * 26) + 10
        gap = random.randint(min_gap, min_gap + 45)
        x = (100 if initial else max(o["x"] for o in self.obstacles)) + gap
        kind = "cactus" if random.random() < 0.75 else "bird"
        self.obstacles.append({"x": float(x), "kind": kind})

    def _next_obstacle(self):
        ahead = [o for o in self.obstacles if o["x"] >= 0]
        return min(ahead, key=lambda o: o["x"]) if ahead else None

    def _state(self):
        """Discretized state the agent sees (keeps the Q-table small).

        Distance is expressed in FRAMES-TO-IMPACT (= distance / speed) so the
        'launch now' window is consistent regardless of game speed — this is the
        key to a small, speed-robust table.
        """
        o = self._next_obstacle()
        airborne = int(self.y > GROUND)
        if o is None:
            return (9, 0, airborne)
        ttc = o["x"] / self.speed  # frames until the obstacle reaches the dino
        if ttc < 5:     tbin = 0
        elif ttc < 8:   tbin = 1   # <-- the launch window for a jump
        elif ttc < 12:  tbin = 2
        elif ttc < 18:  tbin = 3
        else:           tbin = 4
        kind = 0 if o["kind"] == "cactus" else 1
        return (tbin, kind, airborne)

    def step(self, action):
        """Advance one frame. Returns (state, reward, done)."""
        self.steps += 1
        self.speed += SPEED_RAMP

        # apply action (can only jump from the ground)
        self.ducking = (action == DUCK and self.y == GROUND)
        if action == JUMP and self.y == GROUND:
            self.vy = JUMP_V

        # physics
        if self.y > GROUND or self.vy > 0:
            self.y += self.vy
            self.vy -= GRAVITY
            if self.y <= GROUND:
                self.y, self.vy = GROUND, 0.0

        # move obstacles left; recycle + spawn
        for o in self.obstacles:
            o["x"] -= self.speed
        self.obstacles = [o for o in self.obstacles if o["x"] > -10]
        if len(self.obstacles) < 2:
            self._spawn()

        # collision check at the dino's x position (~0)
        done = False
        for o in self.obstacles:
            if -6 < o["x"] < 6:  # obstacle is at the dino
                if o["kind"] == "cactus":
                    # must be in the air to clear a cactus
                    if self.y <= GROUND + 2:
                        done = True
                else:  # bird: must be ducking (or not jumping into it)
                    if not self.ducking:
                        done = True
        reward = -100.0 if done else 1.0  # survive = +1/frame; crash = big penalty
        self.score += 0 if done else 1
        if self.steps >= MAX_STEPS:
            done = True  # treated as a "win" (survived the cap)
        return self._state(), reward, done


# --- The learner (Q-learning, identical machinery to Module 8) --------------
def train(episodes=4000, alpha=0.1, gamma=0.95, eps_start=1.0, eps_end=0.02):
    Q = {}

    def q(s):
        if s not in Q:
            Q[s] = [0.0, 0.0, 0.0]
        return Q[s]

    history = []
    scores = []
    for ep in range(episodes):
        eps = eps_end + (eps_start - eps_end) * (1 - ep / episodes)
        game = DinoGame()
        s = game.reset()
        done = False
        while not done:
            if random.random() < eps:
                a = random.choice(ACTIONS)
            else:
                qs = q(s)
                a = max(range(3), key=lambda i: qs[i])
            ns, r, done = game.step(a)
            best_next = max(q(ns))
            q(s)[a] += alpha * (r + gamma * best_next - q(s)[a])
            s = ns
        scores.append(game.score)
        if (ep + 1) % 500 == 0:
            avg = sum(scores[-500:]) / 500
            history.append((ep + 1, avg))
    return Q, history


def play_greedy(Q, episodes=5):
    """Run the learned policy with no exploration; report scores."""
    results = []
    for _ in range(episodes):
        game = DinoGame()
        s = game.reset()
        done = False
        while not done:
            qs = Q.get(s, [0.0, 0.0, 0.0])
            a = max(range(3), key=lambda i: qs[i])
            s, _, done = game.step(a)
        results.append(game.score)
    return results


def main():
    print("Training a dino agent from zero knowledge "
          "(it doesn't know jumping clears cacti)...\n")
    Q, history = train()

    print("Average score over training (watch it learn to survive):")
    for ep, avg in history:
        bar = "#" * int(avg / 100)
        print(f"  after {ep:5d} games:  avg score {avg:7.1f}  {bar}")
    print()

    print(f"Learned a Q-table with {len(Q)} distinct states.\n")

    print("Playing 5 games with the LEARNED policy (no exploration):")
    scores = play_greedy(Q)
    for i, sc in enumerate(scores, 1):
        tag = "  (hit the 5000-frame cap — effectively unbeatable now)" \
            if sc >= MAX_STEPS - 1 else ""
        print(f"  game {i}: survived {sc} frames{tag}")
    print(f"\n  best: {max(scores)}   worst: {min(scores)}   "
          f"avg: {sum(scores)/len(scores):.0f}")
    print()

    print("TAKEAWAYS")
    print("  - started dying at the first cactus (~score 0)")
    print("  - learned to jump cacti / duck birds from reward alone (+1/frame, -100 crash)")
    print("  - same Q-learning as Module 8 — works because the state is small")
    print("  - the game speeds up forever, so like Tetris it's eventually")
    print("    unwinnable; 'beating it' = surviving far longer than a human can")


if __name__ == "__main__":
    main()
