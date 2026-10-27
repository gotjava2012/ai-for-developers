# Module 8 — Reinforcement Learning: AI That Learns to Beat a Game · Script

*Runtime: ~10–12 min. [brackets] map to slides.md.*

---

[Slide: title]

You've probably seen the headlines — AI beats the world champion at Go, AI
reaches Grandmaster at StarCraft, AI learns to play Atari from nothing but the
screen. In this module I'm going to explain the *entire process* behind those
headlines: how an AI that starts knowing absolutely nothing — not the rules, not
the controls, not even the goal — teaches itself to play and win. By the end
you'll understand every moving part, and you'll watch a from-scratch agent do it
live on your own machine. This is the predictive-to-prescriptive bridge from
Module 7: there we named Markov decision processes in passing; here we actually
solve one.

---

[Slide: the whole idea in one breath]

Here's the entire idea before we break it down. The AI is never told the rules.
It observes the game's current state, takes an action, and the game hands back a
reward plus the next state. It repeats that thousands of times, slowly learning
which actions lead to winning. Early on it acts almost randomly, just to discover
what happens — that's exploration. Later it increasingly does what it has learned
works — that's exploitation. The strategy it ends up with, the mapping from "what
I see" to "what I do," is called the policy. That's it. Trial and error, guided
by a reward signal. Everything else in this module is just the mechanism that
makes that work.

---

[Slide: step 1 — frame as MDP]

Step one, before any learning, is to frame the game as a Markov decision process
— five pieces. States: everything the agent can observe — for our grid it's which
cell it's in; for an Atari game it's the pixels on screen. Actions: the moves
available. The transition: how the world responds when you act — and crucially,
the agent usually doesn't know this in advance, it finds out by trying. The
reward: a single number the game returns after each action, and this is the *only*
teaching signal the agent ever gets. We design it to mean winning — plus one for
reaching the goal, minus one for dying, and a tiny minus a hundredth per step so
it prefers *short* paths. And gamma, the discount factor, which says how much to
value future reward versus immediate reward — that's the piece that lets a move
get credit for a win that happens hundreds of steps later.

---

[Slide: step 2 — value]

Step two: what is the agent actually computing? Value. We track a function called
Q of s comma a, which answers: if I'm in state s and I take action a, and then I
keep playing well, how much total future reward should I expect? Here's the key
insight — if you knew the true Q for every state and action, beating the game
would be trivial: in any situation, just pick the action with the highest Q. So
the entire learning problem collapses into one task: estimate Q. For a small game
Q is literally a lookup table — our grid has sixteen states times four actions,
sixty-four numbers. The agent starts with all of them at zero. It knows nothing.
Then it refines them.

---

[Slide: step 3 — the loop]

Step three is the loop that runs millions of times. Observe the current state.
Choose an action — and we'll come back to how. Take it; the game returns the next
state, a reward, and whether the game ended. Update your estimate of Q for the
action you just took. Move to the new state and repeat until the game's over. Run
that over thousands of playthroughs and Q converges toward the truth. That's the
whole engine. Two pieces inside it are what make it actually *learn* instead of
wander forever: how it chooses actions, and how it updates. Let's take those one
at a time.

---

[Slide: step 4 — explore vs exploit]

Step four, the choice. There's a chicken-and-egg problem here: to learn which
actions are good you have to try them, but to win you have to use the good ones.
Lean too hard on what you already know and you get locked into the first mediocre
strategy you happened to find. Explore forever and you never cash in. The standard
fix is called epsilon-greedy: with some probability epsilon you act completely
randomly, otherwise you take the best action you currently know. And you *decay*
epsilon over time — start near one, almost pure exploration, because at the start
the agent knows nothing so random is as good as anything, then shrink it toward
about five percent, mostly exploiting the policy it now trusts. This is exactly
why, in the lab, the win rate sits near zero early — it's flailing on purpose —
and then climbs steeply once epsilon drops.

---

[Slide: step 5 — the update]

Step five is where learning literally happens — one line. New Q equals old Q,
plus a small learning rate alpha, times a quantity in brackets: the reward you
just got, plus gamma times the best Q available in the state you landed in, minus
your old estimate. Read it as: nudge my old guess toward a better one. That better
one — reward plus the value of where I ended up — is called the target, and notice
it uses the agent's *own* later estimates to improve its earlier ones; that's
called bootstrapping. The bracket is the TD error, how wrong I was. Now here's how
this solves the hardest part of beating a game — credit assignment. The plus-one
reward only lands on the final winning move. But next time through, the move right
before the win sees that high value and its own Q goes up. The time after that,
the move before *that* goes up. Value propagates backward along the winning path,
one step per visit, until the very first move correctly knows it leads to a win
far in the future. When you watch the grid's arrows line up into a path, you are
literally watching that propagation. And one subtle but powerful property:
because the update always bootstraps from the *best* next action, the agent can
explore randomly and still converge on the *optimal* policy. That's called being
off-policy.

---

[Slide: step 6 — scaling to deep RL]

Step six: how does this become AlphaGo? Our table has sixty-four entries. A chess
board has about ten-to-the-forty states. An Atari frame is millions of pixels. You
can't put that in a table. So here's the one thing that changes — and it's the
only conceptual change — you replace the Q-table with a neural network that
*approximates* Q from the raw state. States, actions, rewards, the loop, explore
versus exploit, the TD-error update — all of it stays the same. That's a Deep
Q-Network, how DeepMind beat Atari from pixels in 2015. From there the family
grows: policy-gradient methods like PPO that learn the policy directly — that's
the workhorse behind OpenAI's Dota bot and, by the way, behind aligning LLMs.
AlphaZero, which pairs a learned network with tree search and trains purely by
playing *itself*, getting stronger with zero human games. And MuZero, which even
learns the rules of the game and then plans inside its own learned model.

---

[Slide: the milestones]

So the trajectory, quickly. DQN, 2015: human-level on dozens of Atari games, one
algorithm, raw pixels. AlphaGo beats the Go world champion in 2016 — then
AlphaZero throws away the human games a year later and gets *stronger* from
self-play alone. OpenAI Five beats the Dota 2 world champions. MuZero wins without
even being told the rules. Each step removes something the AI needed to be given.

---

[Slide: gotchas]

Now the honest part — why this is genuinely hard. Sparse reward: if you only score
on a win, the agent may never randomly stumble onto one to learn from, so you
shape intermediate rewards. Reward hacking: the agent maximizes the *literal*
reward, not what you meant — the famous case is a boat-racing agent that learned
to spin in circles collecting score pickups instead of finishing the race. Which
leads to the single most important lesson in this whole module: your reward design
*is* your definition of the goal. Get it wrong and the agent will ruthlessly
exploit the gap. Add to that sample inefficiency — these systems can need millions
to billions of frames; OpenAI Five played the equivalent of nine hundred years of
Dota per day — and training instability in self-play settings.

---

[Slide: beyond games]

Finally, why we care beyond games. Games are just the testbed — the same machinery
runs robotics control, datacenter cooling, chip layout, recommendation, and
trading. And most directly for this course: RLHF, reinforcement learning from
human feedback, is how LLMs get aligned to human preferences — it's the literal
"RL" in the assistant you're talking to. Learning to beat a game and learning to
be a helpful assistant are, mechanically, the same thing: maximize a reward signal
over a sequence of decisions.

---

[Slide: lab]

To the lab — and this one runs on your machine with no PyTorch, standard library
only. You'll train an agent on a little grid-world game: a start, a goal, some
pits to avoid. It begins knowing nothing, and you'll watch its win rate climb from
around two percent to roughly ninety as epsilon decays and the value propagates.
At the end it prints the policy it learned — an arrow in every cell — and the exact
winning path it discovered, dodging every pit. It was never told any of that. It
learned to beat the game from plus-one and minus-one. That's reinforcement
learning, end to end.
