---
title: "23. Reinforcement Learning - A Friendly Guide"
category: Machine Learning
order: 23
tags:
  - machine-learning
  - reinforcement-learning
  - rlhf
  - reward
  - agent
  - q-learning
  - policy
  - beginners
  - friendly
summary: A beginner-friendly guide to reinforcement learning. Learn how an agent learns by trial and error using rewards and punishments, how Q-learning works, and how RLHF is used to train language models like ChatGPT.
---

# Reinforcement Learning

## Learning by trial, error, and reward

A child learning to walk does not read a physics textbook. They try, fall, try again, and gradually learn what works through a cycle of actions and feedback. That is the essence of **reinforcement learning (RL)**.

In RL, a software **agent** takes **actions** in an **environment**. Each action produces a **reward** (positive or negative). Over time, the agent learns which actions lead to the most reward.

No labelled dataset. No explicit teacher. Just a cycle of trying and learning from the outcome.

This tutorial covers:

1. The key concepts — agent, environment, state, action, reward.
2. The exploration vs exploitation trade-off.
3. Q-learning — the foundational RL algorithm.
4. Deep Q-Networks (DQN).
5. Reinforcement Learning from Human Feedback (RLHF) — how ChatGPT is trained.
6. Python demonstration.

---

## 1. The key concepts

| Concept | Definition | Example (game of chess) |
|---------|-----------|------------------------|
| **Agent** | The learner / decision-maker | The chess-playing program |
| **Environment** | The world the agent operates in | The chess board |
| **State** | The current situation | Current positions of all pieces |
| **Action** | What the agent can do | Move a piece |
| **Reward** | Feedback signal after an action | +1 for winning, -1 for losing, 0 otherwise |
| **Policy** | The agent's strategy | "Given this board state, make this move" |
| **Episode** | One complete run from start to end | One complete chess game |

The goal: learn a **policy** that maximises **total reward** over time.

> **Memory trick:** RL is like training a dog. You don't explain the rules — you give treats (rewards) for good behaviour and none for bad. Over many repetitions, the dog learns what earns treats.

---

## 2. The reward signal drives everything

The reward signal is the only feedback the agent receives. Designing it carefully is crucial:

| Reward design | Consequence |
|--------------|-------------|
| +1 for winning a game | Agent learns winning strategies |
| +0.01 for each move survived | Agent learns to prolong the game (may not be what you want) |
| +1 for scoring, -0.01 per step | Agent learns to score efficiently |
| Sparse reward (only at the end) | Agent struggles to learn — no intermediate signal |

**Reward shaping** — adding intermediate rewards to help the agent learn faster — is a key part of RL system design.

---

## 3. Exploration vs exploitation

A fundamental tension in RL:

- **Exploitation** — do what you already know works (take the action with the highest known reward)
- **Exploration** — try something new (you might discover something even better)

A purely exploiting agent gets stuck in a local optimum. A purely exploring agent never capitalises on what it learned.

The **epsilon-greedy** strategy balances this:

```python
import random

epsilon = 0.1   # 10% chance of exploring

def choose_action(state, q_table, epsilon):
    if random.random() < epsilon:
        return random.choice(actions)   # explore
    else:
        return max(actions, key=lambda a: q_table[state][a])   # exploit
```

Typically epsilon starts high (lots of exploration) and decays over time as the agent learns.

---

## 4. Q-learning — the foundational algorithm

**Q-learning** learns a table of values `Q(state, action)` — the expected total future reward for taking action `a` in state `s`.

The **Bellman equation** updates Q values after each action:

```
Q(s, a) ← Q(s, a) + α × [r + γ × max Q(s', a') − Q(s, a)]
                           ↑                 ↑
                      immediate reward    best future reward
```

- **α (alpha)** — learning rate (how fast to update)
- **γ (gamma)** — discount factor (how much to value future rewards vs immediate)
- **r** — reward received
- **s'** — next state after taking action a

### Python example — simple grid world

```python
import numpy as np
import random

# 4x4 grid world
# Agent starts at (0,0), goal at (3,3), cliff at (2,2)
# Actions: 0=up, 1=right, 2=down, 3=left

GRID_SIZE = 4
ACTIONS   = [0, 1, 2, 3]   # up, right, down, left
GOAL      = (3, 3)
CLIFF     = (2, 2)

def step(state, action):
    r, c = state
    if action == 0: r = max(r-1, 0)
    elif action == 1: c = min(c+1, GRID_SIZE-1)
    elif action == 2: r = min(r+1, GRID_SIZE-1)
    elif action == 3: c = max(c-1, 0)
    next_state = (r, c)
    if next_state == GOAL:  return next_state, +10, True
    if next_state == CLIFF: return next_state,  -5, True
    return next_state, -0.1, False   # small penalty per step

# Q-table: state → action → value
Q = {}
for r in range(GRID_SIZE):
    for c in range(GRID_SIZE):
        Q[(r,c)] = {a: 0.0 for a in ACTIONS}

alpha = 0.1   # learning rate
gamma = 0.9   # discount factor
epsilon = 0.3 # exploration rate

for episode in range(2000):
    state = (0, 0)
    for _ in range(100):
        # Choose action
        if random.random() < epsilon:
            action = random.choice(ACTIONS)
        else:
            action = max(ACTIONS, key=lambda a: Q[state][a])

        next_state, reward, done = step(state, action)

        # Bellman update
        best_next = max(Q[next_state].values())
        Q[state][action] += alpha * (reward + gamma * best_next - Q[state][action])

        state = next_state
        if done:
            break

# Show learned policy
print("Learned policy (best action at each cell):")
arrows = {0: '↑', 1: '→', 2: '↓', 3: '←'}
for r in range(GRID_SIZE):
    row = ''
    for c in range(GRID_SIZE):
        if (r,c) == GOAL:  row += ' G '
        elif (r,c) == CLIFF: row += ' X '
        else:
            best = max(ACTIONS, key=lambda a: Q[(r,c)][a])
            row += f' {arrows[best]} '
    print(row)
```

---

## 5. Deep Q-Networks (DQN)

For complex environments (like video games with pixel inputs), a Q-table is too large. **DQN** replaces the Q-table with a neural network:

```
State (pixels or features) → Neural Network → Q-values for each action
```

```python
import torch
import torch.nn as nn

class DQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim)
        )

    def forward(self, state):
        return self.net(state)   # returns Q-value for each action

# Usage with OpenAI Gymnasium
import gymnasium as gym

env = gym.make('CartPole-v1')
state_dim  = env.observation_space.shape[0]   # 4 (cart position, velocity, pole angle, angular velocity)
action_dim = env.action_space.n               # 2 (push left or right)

dqn = DQN(state_dim, action_dim)
optimizer = torch.optim.Adam(dqn.parameters(), lr=0.001)
# Full DQN training loop uses experience replay and a target network
```

---

## 6. Reinforcement Learning from Human Feedback (RLHF)

RLHF is how models like ChatGPT are trained to be helpful and safe. It has three stages:

### Stage 1 — Supervised Fine-Tuning (SFT)
Start with a pre-trained language model. Fine-tune it on a curated dataset of (prompt, good response) pairs written by humans.

```
Prompt:   "Explain gradient descent"
Response: "Gradient descent is an optimisation algorithm..." (human-written)
```

### Stage 2 — Train a reward model
Show human raters multiple model responses to the same prompt. They rank them from best to worst. A **reward model** is trained to predict these human rankings.

```
Response A: "Gradient descent minimises a loss function by..."  → rank 1 (best)
Response B: "I don't know what gradient descent is"            → rank 3 (worst)
Response C: "It's an algorithm for training neural networks"   → rank 2
```

### Stage 3 — RL fine-tuning with PPO
The language model is treated as an RL agent. For each response it generates, the reward model assigns a score. The model is updated using **Proximal Policy Optimisation (PPO)** to generate responses with higher reward scores.

```
Language model (agent)
    ↓ generates response
Reward model
    ↓ scores the response
PPO algorithm
    ↓ updates language model weights to increase score
    ↑_____________________________________________|
              repeat thousands of times
```

```
RLHF pipeline:
Pre-trained LLM
    → SFT on demonstrations
    → Reward model trained on human rankings
    → PPO fine-tuning guided by reward model
    → ChatGPT / Claude / Gemini
```

> **Memory trick:** RLHF is like training a new employee. First you show them good examples (SFT). Then you have customers rate their work (reward model). Then you give the employee feedback based on customer ratings and they improve (PPO).

---

## 7. RL vs supervised learning

| Aspect | Supervised Learning | Reinforcement Learning |
|--------|--------------------|-----------------------|
| Labels | Explicit correct answers | Only a reward signal |
| Timing | Label available immediately | Reward may come much later |
| Data | Static dataset | Generated by agent's own actions |
| Examples | Spam classifier, image classifier | Game playing, robotics, RLHF |

---

## 8. Where RL is used today

| Application | What the agent learns |
|-------------|----------------------|
| Game playing (AlphaGo, AlphaZero) | Winning strategies in games |
| Robotics | How to walk, grasp, navigate |
| Recommendation systems | Which content maximises engagement |
| Trading algorithms | When to buy and sell |
| ChatGPT / Claude (RLHF) | How to give helpful, safe responses |
| Data centre cooling (DeepMind) | How to minimise energy use |

---

## Summary

- RL trains an **agent** to maximise **reward** by taking **actions** in an **environment**.
- No labelled data — only a reward signal after each action.
- **Q-learning** maintains a table of expected future rewards for each (state, action) pair.
- **DQN** replaces the Q-table with a neural network for complex environments.
- **RLHF** applies RL to language models: human raters rank outputs, a reward model captures their preferences, and PPO fine-tunes the LLM to generate higher-ranked responses.
- The exploration vs exploitation trade-off is central to all RL algorithms.
