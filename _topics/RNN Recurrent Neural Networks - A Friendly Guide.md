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

## 8. Seeing the memory change — step by step

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

## 12. Real-world applications

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

## 13. The big limitation — forgetting long-ago things

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

## 14. Quick recap — test yourself

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

## Summary

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
| **Limitation** | Basic RNNs forget things from long ago — fixed by LSTM in Part 15 |

<div class="mermaid">
graph LR
    S1["Step 1\nread input 1"] -->|"update memory"| S2["Step 2\nread input 2"]
    S2 -->|"update memory"| S3["Step 3\nread input 3"]
    S3 -->|"update memory"| S4["Step N\nread input N"]
    S4 --> ANS["Final memory\n→ answer"]
</div>
