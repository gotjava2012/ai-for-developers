# Module 9 — Beat the Chrome Dino Game · Script

*Runtime: ~9–11 min. [brackets] map to slides.md.*

---

[Slide: title]

You know the little dinosaur game that shows up in Chrome when your internet
drops — the T-Rex that jumps over cacti? In this module we're going to build an
AI that beats it. And I picked this game very deliberately, because of the three
games people always ask about — Mario, Tetris, and the dino — this is the only one
that trains end to end on a normal laptop with zero dependencies. It's also the
cleanest possible demonstration that the reinforcement learning from Module 8
isn't just a toy: point the exact same algorithm at a real game and it wins.

---

[Slide: why the dino game]

Here's why the other two don't work locally. Mario needs a NES emulator plus a
deep convolutional network reading pixels — that's PyTorch and a GPU, so it's
Colab territory. Tetris is a board-evaluation problem where strong play uses
heuristic search, and it's provably unwinnable in the long run anyway. The dino
game is different: its entire decision reduces to three things — is an obstacle
coming, what kind is it, and am I already in the air. That's a handful of numbers,
not a screen of pixels. And small state is exactly what lets the Module 8 Q-table
work. No neural network required. One quick honesty note, same as Tetris: the dino
game speeds up forever, so it's eventually unwinnable. "Beating it" means going
from a score of zero to surviving far longer than any human can.

---

[Slide: MDP framing]

Let's frame it as a Markov decision process, like we did in Module 8. The state is
a discretized snapshot: how soon the next obstacle arrives, whether it's a cactus
or a bird, and whether the dino is currently airborne. The actions are run, jump,
and duck. The reward is plus one for every frame survived and minus a hundred for
a collision — and that penalty is the only thing that ever tells the agent an
obstacle is bad. It is never told that jumping clears a cactus. The transition is
the physics: gravity pulls the dino back down, obstacles scroll left at the
current speed, and the speed ramps up every single frame. The agent's job is the
same as always — estimate Q of state and action, then act greedily.

---

[Slide: the state decision]

Now the single most important design decision in this whole module, and it's a
lesson that applies far beyond this game. Your instinct would be to bucket the raw
distance to the next obstacle. That fails — and understanding why is the point.
The dino's jump has a fixed air time, about twenty frames. To clear a cactus you
have to launch when the cactus is the right *time* away. But how far away is it in
*distance* at that moment? That depends on the speed — which keeps rising. So a
single "distance equals 110" bucket means "jump now, perfect" when you're slow,
and "you jumped way too late, you're dead" when you're fast. The table would need
a separate entry for every speed, and the agent would have to relearn jumping over
and over.

---

[Slide: time-to-impact]

The fix is beautiful in its simplicity: don't bucket distance, bucket distance
*divided by speed* — time to impact, measured in frames. Now "jump when the cactus
is five to eight frames away" is a single rule that's true at every speed, slow or
fast. The state space collapses from hundreds of speed-dependent cells down to
about twenty total, and the agent learns one clean policy that generalizes across
the entire speed ramp. This is feature engineering for reinforcement learning:
choosing a representation in which the right action is a *simple, stable function*
of the state. Get this right and a tiny lookup table wins. Get it wrong and even a
deep network struggles. The whole art is often in the state, not the algorithm.

---

[Slide: the learner]

And the learner itself? Completely unchanged from Module 8. Same Q-learning update
— nudge Q toward reward plus discounted best-next-value. Same epsilon-greedy with
decay: explore wildly early, so the agent stumbles onto the fact that jumping
clears cacti and ducking clears birds, then exploit the learned policy late. The
minus-one-hundred crash penalty propagates backward to the states just *before* a
crash, teaching the agent to act before the obstacle arrives — credit assignment,
exactly like the grid world. I want to be clear about this: nothing about the
algorithm changed. Only the environment and the state changed. That is the entire
lesson — the RL core transfers straight from a toy grid to a real game the moment
you hand it a workable state.

---

[Slide: what it learned]

Here's the payoff from the lab. Compare policies. Always run? Score about sixty —
it dies at the first cactus. Always jump? About a hundred and twenty-five — it
clears cacti but smashes into birds, and it can't jump again while already in the
air. Always duck? Around eighty — ducks the birds, hits the cacti. Random? Around
ninety. And the learned greedy policy? It hits the five-thousand-frame cap every
single game. It's the *only* policy that jumps cacti *and* ducks birds, choosing
the right one based on the state. That conditional behavior — discovered purely
from the reward signal — is the whole demonstration. It didn't learn one trick; it
learned *when* to use each trick.

---

[Slide: when you'd need deep RL]

So when would you actually need the heavy deep-RL approach from those famous
videos? When you don't get a clean state. The videos learn from the raw screen
pixels, and that's where deep RL earns its keep. The recipe, which you'd run on
Colab because it needs PyTorch and a GPU: wrap the game in a Gym-style interface,
stack the last three or four grayscale frames so the network can infer velocity,
feed those into a small convolutional network that outputs Q-values — that's a
DQN — and stabilize it with experience replay and a target network, the two tricks
from Module 8. Train for a million-plus frames. We didn't do that here for a good
reason: PyTorch has no build for this Mac, a CNN needs a GPU anyway, and the
tabular version teaches the same ideas, runs in seconds, and actually beats the
game. Which is the rule of thumb for Modules 7 through 9: use the simplest
representation that makes the decision easy. Hand-crafted features plus a table
beat a neural net whenever you can get away with it. Reach for deep learning only
when the state is genuinely high-dimensional and you can't engineer good features.

---

[Slide: lab]

To the lab — pure standard library, no PyTorch, no emulator, no install. You'll
train the agent from zero and watch its average score climb as epsilon decays.
Then you'll run the learned policy head-to-head against run-only, jump-only,
duck-only, and random baselines, and watch it be the only one that survives
indefinitely — five thousand frames, every game. An AI that taught itself to beat
the game Google gives you when the network is down. That's the course.
