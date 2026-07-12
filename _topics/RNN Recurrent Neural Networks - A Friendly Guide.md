---
title: "Part 14: RNN - Recurrent Neural Networks - A Friendly Guide"
category: Deep Learning
order: 14
tags:
  - deep-learning
  - rnn
  - recurrent-neural-networks
  - sequential-data
  - time-series
  - pytorch
  - beginners
  - friendly
summary: A beginner-friendly introduction to Recurrent Neural Networks. Learn why normal neural networks cannot handle sequences, how an RNN reads data step by step, and how to build one in PyTorch using simple everyday examples.
---

# Part 14: RNN — Recurrent Neural Networks — A Friendly Guide

Before we start, let us think about something simple.

You are reading this sentence right now.

You did not read all the words at once. You read **one word at a time, from left to right**. Each word you read changed your understanding of the next word. By the time you reached the word "sentence", you already knew the context from "You are reading this".

That is exactly how an RNN works.

---

## 1. Why order matters — a story

Look at these two sentences:

> Sentence A: "The food was **not** bad."
> Sentence B: "The food was bad, **not** good."

Both sentences have almost the same words. But one is a compliment and one is a complaint.

The difference is **order** — which word comes where.

Now imagine you gave these two sentences to the models we built in Parts 1–13. Those models see all the words at once — like looking at a scrambled pile of letters. They have no way to tell that "not" comes before "bad" in sentence A but after "bad" in sentence B.

An RNN fixes this. It reads **one word at a time**, remembering what came before. So by the time it reads "bad" in sentence A, it already knows "not" came just before it.

---

## 2. What is sequential data?

**Sequential data** is any data where the order matters.

Think of it this way: if you shuffled the pieces and the data stopped making sense — it is sequential.

| Example | What happens if you shuffle it? |
|---------|--------------------------------|
| A sentence | Becomes nonsense |
| Daily temperatures | You cannot tell if it is getting warmer or colder |
| A song | Sounds like random noise |
| Stock prices | You cannot spot a trend |
| A video | Frames are out of order — looks like a broken film |

<div class="mermaid">
graph LR
    A["Monday: 20°C"] --> B["Tuesday: 22°C"]
    B --> C["Wednesday: 24°C"]
    C --> D["Thursday: 26°C?"]
    style D fill:#f9f,stroke:#333
</div>

In this example, if we see temperatures going up each day — 20, 22, 24 — we expect the next one to also be higher. The **trend** is in the order. Shuffle the days and the trend disappears.

---

## 3. The problem with normal neural networks

In Part 1 we built a model that takes 5 numbers and gives back one answer:

```
[spam_words, links, known_sender, capitals, length] → model → spam or not
```

The model takes **all 5 numbers at the same time**. It does not matter which number goes first.

Now imagine instead of 5 features, you have a sentence:

```
"The food was not bad"
→ 5 words
→ but order matters!
```

If we try to feed all 5 words into a normal network at once, two problems appear:

**Problem 1 — Fixed size**

A normal network needs a fixed number of inputs. Always exactly 5 numbers — not 4, not 7.

But sentences have different lengths. "Hi" is 1 word. "The food at that restaurant near the town centre was absolutely not bad at all" is 17 words. A normal network cannot handle both.

**Problem 2 — No concept of order**

A normal network sees all words at the same time — like looking at a scrambled pile. It treats word 1 and word 5 as equally important. It does not know "not" came before "bad".

<div class="mermaid">
graph TD
    subgraph Normal["Normal Network - reads all at once"]
        W1["not"] --> NN["Neural Network"]
        W2["food"] --> NN
        W3["bad"] --> NN
        W4["was"] --> NN
        W5["The"] --> NN
        NN --> OUT1["??"]
    end
</div>

<div class="mermaid">
graph LR
    subgraph RNN_["RNN - reads one word at a time"]
        WA["The"] --> R1["RNN step 1"]
        R1 -->|memory| R2["RNN step 2"]
        WB["food"] --> R2
        R2 -->|memory| R3["RNN step 3"]
        WC["was"] --> R3
        R3 -->|memory| R4["RNN step 4"]
        WD["not"] --> R4
        R4 -->|memory| R5["RNN step 5"]
        WE["bad"] --> R5
        R5 --> OUT2["not spam - positive"]
    end
</div>

The RNN knows "not" came before "bad". The normal network does not.

---

## 4. The key idea — hidden state (memory)

The thing that makes an RNN different is one simple idea:

> **After reading each word, the RNN keeps a small note about what it just read. It carries that note to the next step.**

This note is called the **hidden state**. It is just a list of numbers — but those numbers are a summary of everything the RNN has read so far.

Think of it like reading a diary:

<div class="mermaid">
graph LR
    D1["Day 1 entry\nRead it"] --> N1["Your memory\nafter day 1"]
    N1 --> D2["Day 2 entry\nRead it"]
    D2 --> N2["Your memory\nafter day 2\nupdated"]
    N2 --> D3["Day 3 entry\nRead it"]
    D3 --> N3["Your memory\nafter day 3\nupdated again"]
    N3 --> ANS["Now answer\na question\nabout the diary"]
</div>

The **hidden state** plays the role of "your memory". At every page:
- You read the new entry (new input)
- You combine it with what you already remember (old hidden state)
- You update your memory (new hidden state)
- You carry that updated memory to the next page

---

## 5. How one RNN step works — very simply

Let us trace through one step, using temperature data.

**The situation:** The RNN has already read Monday (20°C) and Tuesday (22°C). Now it reads Wednesday (24°C).

**Before this step:**
- Current input = 24 (Wednesday's temperature)
- Old memory = some numbers representing "temperatures were 20 then 22"

**What the RNN does:**

```
Step 1: Take today's temperature number (24)
Step 2: Take the old memory numbers
Step 3: Mix them together (multiply by weights, add them up)
Step 4: Squeeze the result between -1 and +1 using tanh
Step 5: This is the new memory — it now knows about 20, 22, and 24
```

<div class="mermaid">
graph TD
    Input["Today's input\n24°C"] --> Mix["Mix together\nwith weights"]
    OldMem["Old memory\nknows about 20 and 22"] --> Mix
    Mix --> Tanh["tanh function\nsquash between -1 and 1"]
    Tanh --> NewMem["New memory\nnow knows about 20, 22, and 24"]
    NewMem --> NextStep["Carry to next step"]
</div>

The **tanh** function just keeps the numbers from getting too big. Think of it like a volume knob that stops at maximum — it cannot go above 1 or below -1.

The numbers inside the memory are called a **hidden state**. They are just regular numbers — not words, not temperatures directly. They are the network's own internal representation of what it has seen.

---

## 6. The same brain at every step

Here is something very important and a bit surprising.

The RNN uses **exactly the same weights at every single step**.

Whether it is reading word 1 or word 50 — the same multiplication, the same numbers, the same calculation.

This is like how you use the same brain to understand every word you read. Your brain does not change between page 1 and page 100. What changes is your memory of what you have already read.

<div class="mermaid">
graph LR
    X1["20°C\nDay 1"] --> Cell1["RNN Cell\nsame weights"]
    H0["Memory: 0\nno history yet"] --> Cell1
    Cell1 --> H1["Memory: h1\nknows day 1"]

    X2["22°C\nDay 2"] --> Cell2["RNN Cell\nsame weights"]
    H1 --> Cell2
    Cell2 --> H2["Memory: h2\nknows days 1 and 2"]

    X3["24°C\nDay 3"] --> Cell3["RNN Cell\nsame weights"]
    H2 --> Cell3
    Cell3 --> H3["Memory: h3\nknows all 3 days"]

    H3 --> Pred["Predict\nDay 4"]
</div>

Notice: all three cells say "same weights". The same small set of weights handles step 1, step 2, step 3, and every step after that.

This is why RNNs can handle **any length of sequence** — there is no fixed input size. You just keep applying the same cell as many times as needed.

---

## 7. Unfolding — drawing the RNN across time

When people draw an RNN in a diagram, they often show it in two ways.

**Folded view** — the compact view:

<div class="mermaid">
graph LR
    X["Input x"] --> RNN["RNN Cell"]
    RNN -->|hidden state| RNN
    RNN --> OUT["Output"]
</div>

The arrow looping back means "the hidden state goes back into the same cell on the next step."

**Unfolded view** — the same thing but stretched out across time:

<div class="mermaid">
graph LR
    X1["x1\nDay 1"] --> C1["RNN Cell"]
    H0["h0 = 0\nstart"] --> C1
    C1 --> H1["h1\nmemory"]

    X2["x2\nDay 2"] --> C2["RNN Cell"]
    H1 --> C2
    C2 --> H2["h2\nmemory"]

    X3["x3\nDay 3"] --> C3["RNN Cell"]
    H2 --> C3
    C3 --> H3["h3\nmemory"]

    H3 --> OUT["Predict\nDay 4"]
</div>

Both diagrams mean the same thing. The unfolded view just makes it easier to see what is happening at each step.

---

## 8. How the RNN learns — backpropagation through time (BPTT)

We know how the RNN makes predictions — it reads forward step by step.

But how does it **learn**? How does it know to change its weights?

It uses the same idea as every other neural network: **backpropagation**. Look at the mistake, then go backwards through the network and adjust the weights.

For a normal network, "going backwards" means going backwards through the layers — Layer 3 → Layer 2 → Layer 1.

For an RNN, "going backwards" means going backwards **through time steps** — Step 50 → Step 49 → Step 48 → ... → Step 1.

This is called **Backpropagation Through Time (BPTT)**.

### What does BPTT look like?

Here is the unfolded RNN again. This time, let us show both directions — forward and backward:

<div class="mermaid">
graph LR
    X1["x1"] --> C1["Step 1"]
    H0["h0"] --> C1
    C1 --> H1["h1"]

    X2["x2"] --> C2["Step 2"]
    H1 --> C2
    C2 --> H2["h2"]

    X3["x3"] --> C3["Step 3"]
    H2 --> C3
    C3 --> H3["h3"]

    H3 --> OUT["Output"]
    OUT --> LOSS["Loss\nhow wrong?"]

    LOSS -->|"gradient flows back"| C3
    C3 -->|"gradient flows back"| C2
    C2 -->|"gradient flows back"| C1
</div>

The **forward pass** goes left to right — the RNN makes a prediction.
The **backward pass** goes right to left — the error signal flows backwards to teach the RNN what went wrong.

### What is a gradient?

A gradient is just a number that tells each weight: **"move this much in this direction to reduce the error"**.

A big gradient = change the weight a lot.
A small gradient = change the weight a little.
A gradient of zero = do not change this weight at all — it has stopped learning.

### The chain of multiplications

Here is the important part.

When the error flows backwards from Step 3 to Step 2, it gets **multiplied by a number**.
When it then flows from Step 2 to Step 1, it gets **multiplied again**.
And again. And again. All the way back to Step 1.

Each multiplication uses the same weight value — the recurrent weight that connects hidden states.

```
Gradient at Step 50 = original error
Gradient at Step 49 = error × weight × activation_derivative
Gradient at Step 48 = error × weight × weight × activation_derivative × activation_derivative
Gradient at Step  1 = error × (weight × activation_derivative) × ... × (50 times)
```

This chain of multiplications is fine for short sequences. It becomes a big problem for long ones.

---

## 9. The two gradient problems — vanishing and exploding

Depending on the value being multiplied at each step, one of two things happens:

---

### Problem 1 — Vanishing gradient (the most common)

If the number being multiplied at each step is **less than 1**, the gradient shrinks with every step.

```
Start with:     1.0
After 1 step:   1.0  × 0.9 = 0.9
After 2 steps:  0.9  × 0.9 = 0.81
After 5 steps:  0.59
After 10 steps: 0.35
After 20 steps: 0.12
After 50 steps: 0.000052   ← almost zero
```

By the time the gradient reaches the early steps, it is so tiny that the weights there barely change. Those early steps **stop learning**.

<div class="mermaid">
graph RL
    L["Loss"] -->|"gradient = 1.0"| S50["Step 50\ngradient: 1.0"]
    S50 -->|"× 0.9"| S49["Step 49\ngradient: 0.9"]
    S49 -->|"× 0.9"| S48["Step 48\ngradient: 0.81"]
    S48 -->|"× 0.9 × 0.9 × ..."| S1["Step 1\ngradient: 0.000052"]
    style S1 fill:#ffcccc
    style L fill:#4CAF50,color:#fff
</div>

> **Real-world effect:** The RNN can only learn from recent steps. Anything said early in a long sentence — or early in a long time series — is completely ignored.

---

### Why does this happen so often?

It is because of the **tanh** and **sigmoid** activation functions that RNNs use.

Both of these functions **squash** their input into a small range:
- `tanh` squashes to between **-1 and +1**
- `sigmoid` squashes to between **0 and 1**

When you take the derivative (the slope) of these functions, the result is almost always **less than 1**.

```
tanh derivative at 0    = 1.0   (maximum)
tanh derivative at 1    = 0.42
tanh derivative at 2    = 0.07
tanh derivative at 3    = 0.009  ← very small
```

So in practice, the number being multiplied at every step is usually much less than 1. Vanishing gradients are the **default** outcome for basic RNNs.

---

### Problem 2 — Exploding gradient

If the number being multiplied at each step is **greater than 1**, the gradient grows with every step.

```
Start with:     1.0
After 1 step:   1.0  × 1.1 = 1.1
After 2 steps:  1.1  × 1.1 = 1.21
After 5 steps:  1.61
After 10 steps: 2.59
After 20 steps: 6.73
After 50 steps: 117  ← enormous
```

When the gradient is enormous, the weight update is enormous. The weights jump to extreme values. The model breaks — it starts producing `NaN` (not a number) or infinite values.

<div class="mermaid">
graph RL
    L2["Loss"] -->|"gradient = 1.0"| S50b["Step 50\ngradient: 1.0"]
    S50b -->|"× 1.1"| S49b["Step 49\ngradient: 1.1"]
    S49b -->|"× 1.1"| S48b["Step 48\ngradient: 1.21"]
    S48b -->|"× 1.1 × 1.1 × ..."| S1b["Step 1\ngradient: 117"]
    style S1b fill:#ff4444,color:#fff
    style L2 fill:#4CAF50,color:#fff
</div>

> **Real-world effect:** Training becomes completely unstable. The loss jumps all over the place or becomes `NaN`. The model never converges.

---

### Summary of the two problems

| Problem | What multiplier does | What happens to gradient | Effect on training |
|---------|---------------------|--------------------------|-------------------|
| **Vanishing** | Multiplier < 1 (e.g. 0.9) | Shrinks to near zero | Early steps stop learning — model forgets long-ago info |
| **Exploding** | Multiplier > 1 (e.g. 1.1) | Grows to huge number | Weights update wildly — training crashes |

---

### Fix 1 — Gradient clipping (fixes exploding)

Exploding gradients have a simple fix called **gradient clipping**.

Before updating the weights, we check: is any gradient too large? If yes, we cut it down to a maximum allowed value.

```python
import torch
import torch.nn as nn

model     = TemperatureRNN()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(300):
    prediction = model(X)
    loss = loss_fn(prediction, y)

    optimizer.zero_grad()
    loss.backward()

    # Gradient clipping — cut any gradient larger than 1.0
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

    optimizer.step()
```

This is like saying: "No matter how angry the error signal is, I will only listen to it up to a certain volume."

Gradient clipping is **one line of code** and is commonly used in practice.

**But** — gradient clipping does **not** fix the vanishing gradient problem. If the gradient is already near zero, clipping does nothing. The early steps still learn nothing.

---

### Fix 2 — Better architecture (fixes vanishing)

To truly fix the vanishing gradient problem, we need to change how the network is designed.

The key insight: instead of multiplying the gradient through every step, we need a path where gradients can flow backwards **without being multiplied by something less than 1** at every step.

This is exactly what **LSTM** and **GRU** were designed to do.

<div class="mermaid">
graph LR
    subgraph Basic["Basic RNN — gradient shrinks at every step"]
        S1r["Step 1\nlearns nothing"] -.->|"tiny gradient"| S2r["Step 2"] -.->|"small gradient"| S3r["Step 3"] -->|"normal gradient"| LOSS1["Loss"]
        style S1r fill:#ffcccc
    end

    subgraph LSTM_["LSTM — gradient highway stays open"]
        S1l["Step 1\nlearns correctly"] ==>|"gradient highway"| S2l["Step 2"] ==>|"gradient highway"| S3l["Step 3"] --> LOSS2["Loss"]
        style S1l fill:#4CAF50,color:#fff
    end
</div>

LSTM adds a **cell state** — a separate memory channel that runs straight through time. Gradients can flow along this channel without shrinking. This is how LSTM can learn from events that happened hundreds of steps ago.

That is exactly what Part 15 covers in full detail.

---

## 10. Seeing the memory change — step by step

Let us actually run this in Python and watch the memory change at each step.

```python
import torch
import torch.nn as nn

# One RNN — we will build it manually to see inside
input_size  = 1   # one number per step (temperature)
hidden_size = 4   # memory = 4 numbers

# The weights — these stay the same at every step
W_input  = nn.Linear(input_size,  hidden_size, bias=False)
W_hidden = nn.Linear(hidden_size, hidden_size, bias=True)

# Step function: takes current input + old memory, gives new memory
def rnn_step(current_input, old_memory):
    return torch.tanh(W_input(current_input) + W_hidden(old_memory))

# Start: memory = all zeros (the RNN knows nothing yet)
memory = torch.zeros(1, hidden_size)
print(f"Start     → memory: {memory.detach().numpy().round(2)}")

# Process three days, one at a time
days = [("Monday",    20.0),
        ("Tuesday",   22.0),
        ("Wednesday", 24.0)]

for day_name, temp in days:
    x = torch.tensor([[temp]])
    memory = rnn_step(x, memory)
    print(f"{day_name} ({temp}°C) → memory: {memory.detach().numpy().round(3)}")
```

Output:
```
Start     → memory: [[0. 0. 0. 0.]]
Monday    (20.0°C) → memory: [[ 0.999  0.891 -0.723  0.445]]
Tuesday   (22.0°C) → memory: [[ 1.000  0.997 -0.912  0.781]]
Wednesday (24.0°C) → memory: [[ 1.000  0.999 -0.961  0.893]]
```

What you see:
- The memory starts at zero — the RNN knows nothing
- After Monday, the memory changes — it has "seen" 20°C
- After Tuesday, the memory changes again — it now knows about both 20 and 22
- After Wednesday, the memory holds a compressed summary of all three days
- We can now use that final memory to predict Thursday

The memory numbers (0.999, 0.891, etc.) are **not** temperatures. They are the network's own internal code — a compressed representation of the history.

---

## 9. Using PyTorch's built-in RNN

You do not need to write the step function yourself. PyTorch has `nn.RNN` that does all of this automatically:

```python
import torch
import torch.nn as nn

rnn = nn.RNN(
    input_size=1,     # how many numbers per time step
    hidden_size=8,    # how many numbers in the memory
    batch_first=True  # means: input shape is (batch, steps, features)
)

# One sequence of 5 days
# Shape must be (batch_size, number_of_steps, features_per_step)
#              (    1      ,       5        ,       1          )
x = torch.tensor([[[20.0],   # Day 1
                   [22.0],   # Day 2
                   [24.0],   # Day 3
                   [23.0],   # Day 4
                   [25.0]]]) # Day 5

output, h_final = rnn(x)

print("output shape:", output.shape)
# (1, 5, 8) → hidden state at EVERY step
# 1 sequence, 5 steps, 8 memory numbers per step

print("h_final shape:", h_final.shape)
# (1, 1, 8) → hidden state at the LAST step only
```

Two things come back:

| Name | Shape | What it contains | When to use it |
|------|-------|-----------------|----------------|
| `output` | `(1, 5, 8)` | Memory at **every** step | When you need a label at every position (e.g. tag each word) |
| `h_final` | `(1, 1, 8)` | Memory at the **last** step only | When you need one answer for the whole sequence (e.g. spam or not) |

---

## 10. Full working example — predicting next day temperature

Let us build a complete model that learns from historical temperatures and predicts the next day.

```python
import torch
import torch.nn as nn

torch.manual_seed(42)

# --- Step 1: Create training data ---
# We have 12 days of temperature readings
temperatures = [20, 22, 24, 23, 25, 26, 24, 22, 21, 23, 25, 27]

# We create sequences of length 3:
# Given [day1, day2, day3] → predict day4
X_list, y_list = [], []
for i in range(len(temperatures) - 3):
    X_list.append(temperatures[i : i+3])      # 3 days input
    y_list.append(temperatures[i + 3])         # next day target

# Convert to PyTorch tensors
# X shape: (num_samples, 3, 1) — num_samples sequences, 3 steps, 1 number per step
X = torch.tensor(X_list, dtype=torch.float32).unsqueeze(-1)
y = torch.tensor(y_list, dtype=torch.float32).unsqueeze(-1)

print(f"Training samples: {len(X)}")
print(f"X shape: {X.shape}")  # e.g. (9, 3, 1)
print(f"y shape: {y.shape}")  # e.g. (9, 1)

# --- Step 2: Build the model ---
class TemperatureRNN(nn.Module):
    def __init__(self):
        super().__init__()
        # RNN: reads one day at a time, memory size = 16 numbers
        self.rnn    = nn.RNN(input_size=1, hidden_size=16, batch_first=True)
        # Linear: takes the final memory (16 numbers) and outputs 1 predicted temperature
        self.linear = nn.Linear(16, 1)

    def forward(self, x):
        output, h_final = self.rnn(x)
        # h_final shape: (1, batch_size, 16) — we need (batch_size, 16)
        h = h_final.squeeze(0)
        return self.linear(h)

model = TemperatureRNN()

# --- Step 3: Set up training ---
loss_fn   = nn.MSELoss()   # measures how far our prediction is from the real temperature
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# --- Step 4: Train ---
print("\nTraining...")
for epoch in range(300):
    prediction = model(X)
    loss = loss_fn(prediction, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print(f"  Epoch {epoch:3d}  loss: {loss.item():.4f}")

# --- Step 5: Predict ---
print("\nTesting...")
model.eval()
with torch.no_grad():
    # Given: 23, 25, 27°C — what comes next?
    test_input = torch.tensor([[[23.0], [25.0], [27.0]]])
    predicted  = model(test_input).item()
    print(f"  Input:     23°C, 25°C, 27°C")
    print(f"  Predicted: {predicted:.1f}°C")
```

Expected output:
```
Training samples: 9
X shape: torch.Size([9, 3, 1])
y shape: torch.Size([9, 1])

Training...
  Epoch   0  loss: 523.4821
  Epoch 100  loss: 2.1043
  Epoch 200  loss: 0.3812

Testing...
  Input:     23°C, 25°C, 27°C
  Predicted: 28.3°C
```

The loss goes down — the model is learning the pattern that temperatures rise by about 2 degrees each day.

---

## 11. What the model structure looks like

<div class="mermaid">
graph LR
    subgraph Input["Input: 3 days"]
        D1["23°C\nDay 1"]
        D2["25°C\nDay 2"]
        D3["27°C\nDay 3"]
    end

    subgraph RNN_["RNN — reads one day at a time"]
        D1 --> R1["Step 1\nmemory: h1"]
        R1 --> R2["Step 2\nmemory: h2"]
        D2 --> R2
        R2 --> R3["Step 3\nmemory: h3"]
        D3 --> R3
    end

    subgraph Output_["Output"]
        R3 --> LIN["Linear layer\nh3 → 1 number"]
        LIN --> PRED["Predicted\n28.3°C"]
    end
</div>

---

## 13. Real-world applications

RNNs are used everywhere data has an order:

| Application | Input sequence | What the RNN outputs |
|-------------|---------------|---------------------|
| **Predicting tomorrow's weather** | Last 7 days of temperature | Tomorrow's temperature |
| **Spam detection** | Words in an email, one by one | Spam / not spam |
| **Google autocomplete** | Words you have typed | Next word suggestion |
| **Voice assistants** | Audio frames, one by one | Words you said |
| **Stock market prediction** | Daily prices | Tomorrow's price |
| **Subtitles / transcription** | Audio | Text |
| **Grammar check** | Words in a sentence | Which words are wrong |

---

## 14. The big limitation — forgetting long-ago things

> This section is a quick visual reminder. The full technical explanation of *why* this happens is in Section 9 above (vanishing gradients).

RNNs have one weakness that matters a lot.

Imagine reading a very long book. You reach chapter 20. Someone asks you about a small detail from chapter 1. You might not remember it — too many things have happened since.

An RNN has exactly the same problem. The memory (hidden state) gets updated at every step. Over many steps, early information gets overwritten. By step 50, what happened at step 1 is mostly gone.

<div class="mermaid">
graph LR
    W1["The\ncat"] -->|"strong memory"| W2["sat\non"]
    W2 -->|"weaker memory"| W3["the\nold"]
    W3 -->|"weaker still"| W4["wooden\nchair"]
    W4 -->|"very faint"| W5["was\nhungry"]
    style W1 fill:#4CAF50,color:#fff
    style W5 fill:#ffcccc
</div>

The word "cat" from the beginning is barely remembered by the time the RNN reaches "was hungry" at the end.

This is called the **vanishing gradient problem**, and it was a big limitation of basic RNNs.

The solution is **LSTM** and **GRU** — two improved versions of RNN with a much better memory system. That is exactly what Part 15 covers.

---

## 15. Quick recap — test yourself

Read each question. Try to answer before looking.

---

**Q1: What is the difference between a normal network and an RNN?**

A normal network reads all the input at once — order does not matter.
An RNN reads one step at a time, remembering what came before.

---

**Q2: What is the hidden state?**

It is the RNN's memory. After each step, the RNN updates it.
It carries a summary of everything read so far to the next step.

---

**Q3: Does the RNN use different weights at step 1 vs step 10?**

No. The same weights are used at every step.
This is why RNNs can handle sequences of any length.

---

**Q4: You have 7 days of sales data. What shape is the input to an RNN?**

`(1, 7, 1)` — 1 sequence, 7 steps, 1 number per step.

---

**Q5: What is the big weakness of a basic RNN?**

It forgets things from long ago. The memory fades over many steps.
LSTM and GRU fix this — covered in Part 15.

---

**Q6: What is BPTT?**

Backpropagation Through Time. It is how an RNN learns — the error signal flows backwards through every time step, adjusting weights at each one.

---

**Q7: What are the two gradient problems? How are they different?**

Vanishing gradient — the error signal shrinks to almost zero as it flows back. Early time steps learn nothing. The RNN forgets long-ago information.

Exploding gradient — the error signal grows to a huge number as it flows back. Weights update wildly and training crashes.

---

**Q8: How do you fix exploding gradients?**

Gradient clipping — one line of code: `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`. It cuts the gradient down to a maximum allowed value before the weight update.

---

**Q9: Why does vanishing gradient happen so often in basic RNNs?**

Because `tanh` and `sigmoid` activation functions squash their output to small values. Their derivatives are almost always less than 1. Multiply many numbers less than 1 together and the result approaches zero.

---

## 16. Summary

```
Normal network reads everything at once — no concept of order
RNN reads one step at a time — order matters, memory carries forward
```

| Concept | Simple meaning |
|---------|---------------|
| **Sequential data** | Data where order matters — sentences, temperatures, prices |
| **Hidden state** | The RNN's memory — a list of numbers updated at every step |
| **Same weights** | The same calculation is used at every step — works for any length |
| **Unfolding** | Drawing the RNN stretched out across time — one box per step |
| **BPTT** | Backpropagation Through Time — the error flows backwards through every time step to teach the model |
| **Vanishing gradient** | Error signal shrinks to zero as it flows back — early steps stop learning |
| **Exploding gradient** | Error signal grows huge as it flows back — weights update wildly, training crashes |
| **Gradient clipping** | One line of code that caps the gradient so exploding cannot happen |
| **Fix for vanishing** | LSTM and GRU — architectures with a protected memory channel so gradients can flow without shrinking |

<div class="mermaid">
graph LR
    S1["Step 1\nread input 1"] -->|"update memory"| S2["Step 2\nread input 2"]
    S2 -->|"update memory"| S3["Step 3\nread input 3"]
    S3 -->|"update memory"| S4["Step N\nread input N"]
    S4 --> ANS["Final memory\n→ answer"]
</div>
