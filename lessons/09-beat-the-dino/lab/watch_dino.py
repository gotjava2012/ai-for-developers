"""
Module 9 — WATCH the dino agent play (animated ASCII in your terminal).

Renders the game live so you can actually see the dino jump cacti and duck birds.
To show learning without an hours-long render, it trains in fast (headless) bursts
and then animates the agent at three stages:

    Stage 1  untrained        -> crashes almost immediately
    Stage 2  lightly trained  -> clears some, still dies
    Stage 3  fully trained    -> clears everything

Pure Python standard library. Reuses the verified game + learner from the lab.
    python3 watch_dino.py
"""

import sys
import time

from dino_q_learning import (
    DinoGame, ACTIONS, RUN, JUMP, DUCK, GROUND, MAX_STEPS,
)

# --- incremental training (same Q-learning, just resumable) -----------------
import random


def train_steps(Q, episodes, alpha=0.1, gamma=0.95, eps=0.1):
    """Run `episodes` of Q-learning into an existing table Q (in place)."""
    def q(s):
        if s not in Q:
            Q[s] = [0.0, 0.0, 0.0]
        return Q[s]
    for _ in range(episodes):
        g = DinoGame()
        s = g.reset()
        done = False
        while not done:
            a = random.choice(ACTIONS) if random.random() < eps \
                else max(range(3), key=lambda i: q(s)[i])
            ns, r, done = g.step(a)
            q(s)[a] += alpha * (r + gamma * max(q(ns)) - q(s)[a])
            s = ns
    return Q


# --- ASCII renderer ---------------------------------------------------------
WIDTH = 60          # columns of visible track
HEIGHT = 10         # rows (vertical air space)
GROUND_ROW = HEIGHT - 1
SCALE = 7.0         # world y-units per screen row (jump peak ~49 -> ~7 rows up)


def render(game, action, label, frame):
    """Draw one frame of the game as text."""
    grid = [[" "] * WIDTH for _ in range(HEIGHT)]

    # ground line
    for x in range(WIDTH):
        grid[GROUND_ROW][x] = "_"

    # obstacles (dino sits at screen column 4; obstacles scroll toward it)
    dino_col = 4
    for o in game.obstacles:
        col = dino_col + int(o["x"] / 4.0)   # world x -> screen col
        if 0 <= col < WIDTH:
            if o["kind"] == "cactus":
                grid[GROUND_ROW][col] = "Y"            # cactus on the ground
                if GROUND_ROW - 1 >= 0:
                    grid[GROUND_ROW - 1][col] = "|"
            else:  # bird flies at head height
                grid[GROUND_ROW - 3][col] = ">"

    # dino: row depends on jump height; ducking shown as a crouch glyph
    dino_row = GROUND_ROW - min(GROUND_ROW, int(game.y / SCALE))
    glyph = "D"
    if action == DUCK and game.y <= GROUND:
        glyph = "d"                      # ducking (crouched)
    if 0 <= dino_row < HEIGHT:
        grid[dino_row][dino_col] = glyph

    act_name = {RUN: "run ", JUMP: "JUMP", DUCK: "DUCK"}[action]
    lines = ["".join(row) for row in grid]
    out = []
    out.append(f"  {label}")
    out.append("  +" + "-" * WIDTH + "+")
    for ln in lines:
        out.append("  |" + ln + "|")
    out.append("  +" + "-" * WIDTH + "+")
    out.append(f"  score={game.score:<5d} speed={game.speed:4.1f} "
               f"action={act_name}   (frame {frame})")
    return "\n".join(out)


def play_animated(Q, label, max_frames=400, fps=30, epsilon=0.0):
    """Play one game with policy Q, drawing each frame in place."""
    g = DinoGame()
    s = g.reset()
    done = False
    frame = 0
    # hide cursor
    sys.stdout.write("\x1b[?25l")
    try:
        while not done and frame < max_frames:
            if epsilon and random.random() < epsilon:
                a = random.choice(ACTIONS)
            else:
                a = max(range(3), key=lambda i: Q.get(s, [0, 0, 0])[i])
            screen = render(g, a, label, frame)
            # move cursor to top-left of our block and redraw
            sys.stdout.write("\x1b[H\x1b[2J")   # clear screen
            sys.stdout.write(screen + "\n")
            sys.stdout.flush()
            s, _, done = g.step(a)
            frame += 1
            time.sleep(1.0 / fps)
        # final frame + outcome
        outcome = ("SURVIVED the render window!" if frame >= max_frames
                   else f"crashed after {g.score} frames")
        sys.stdout.write(f"\n  >> {outcome}\n")
        sys.stdout.flush()
    finally:
        sys.stdout.write("\x1b[?25h")  # show cursor again
    return g.score


def main():
    fps = 30
    print("Legend:  D = dino   d = ducking   Y|= cactus   > = bird   _ = ground")
    print("Training in fast headless bursts, then animating each stage...\n")
    time.sleep(1.5)

    Q = {}

    # Stage 1: untrained (0 episodes)
    play_animated(Q, "STAGE 1 — UNTRAINED (knows nothing)", max_frames=200, fps=fps)
    time.sleep(1.2)

    # Stage 2: lightly trained
    train_steps(Q, episodes=150)
    play_animated(Q, "STAGE 2 — LIGHTLY TRAINED (~150 games)", max_frames=300, fps=fps)
    time.sleep(1.2)

    # Stage 3: fully trained
    train_steps(Q, episodes=4000)
    play_animated(Q, "STAGE 3 — FULLY TRAINED (~4000 games)", max_frames=400, fps=fps)

    print("\n  That's the agent going from crashing to clearing — learned from")
    print("  reward alone, rendered live. (Stage 3 would run forever; the render")
    print("  window is capped so the demo ends.)")


if __name__ == "__main__":
    main()
