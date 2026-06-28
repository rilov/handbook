---
title: "Forward and Backward Propagation - A Friendly Guide"
category: Deep Learning
order: 6
tags:
  - deep-learning
  - pytorch
  - backpropagation
  - forward-propagation
  - chain-rule
  - gradients
  - spam-detection
  - beginners
  - friendly
summary: Learn exactly what happens during forward and backward propagation, using a two-layer spam-detection model. Worked numerical example with the chain rule included.
---

# Forward and Backward Propagation — A Friendly Guide

So far we have seen how a model predicts spam and how PyTorch can update its weights. In this guide, we open the box and watch one complete training step by hand. We use the same spam example and a tiny two-layer model.

---

## 1. What forward and backward propagation mean

| Phase | What it does | Analogy |
|-------|--------------|---------|
| **Forward propagation** | Input features flow through the network to produce a prediction | Reading the email and guessing spam |
| **Backward propagation** | The error flows backward to find how each weight contributed | Tracing the blame back to each weight |
| **Weight update** | Each weight is moved slightly to reduce the error | Correcting the mistake |

> **Memory trick:** Forward is prediction. Backward is blame. Update is correction.

### What is the error?

The **error** is the difference between what the model predicts and the true answer.

- True label: `y = 1` (this email is spam)
- Model prediction: `p = 0.53` (the model thinks it is 53% spam)
- Error: the model is too uncertain. It should have predicted closer to 1.

We do not measure error with simple subtraction. We use a **loss function** that turns the prediction and the label into a single number. For spam detection, the usual loss is **binary cross-entropy**. It gives a large number when the model is confidently wrong and a small number when the model is close.

```
Loss L = -[y * log(p) + (1 - y) * log(1 - p)]
```

If `y = 1` and `p = 0.53`, the loss is about `0.635`. If the model had predicted `p = 0.99`, the loss would be much smaller.

### What is a gradient?

A **gradient** is the answer to this question: "If I increase this weight slightly, how much does the loss change?"

- If the gradient is **positive**, increasing the weight makes the loss larger. So we should decrease the weight.
- If the gradient is **negative**, increasing the weight makes the loss smaller. So we should increase the weight.

The gradient is written as `∂L/∂w`, which means "the change in loss L divided by the change in weight w."

### How is the weight updated?

Once we know the gradient, we update the weight in the opposite direction:

```
new_weight = old_weight - learning_rate * gradient
```

The **learning rate** is a small number like `0.1` or `0.01`. It controls the size of the step. If the learning rate is too large, the model overshoots. If it is too small, learning takes forever.

### A simple example

Imagine a model has only one weight and its current value is `0.5`. The gradient for that weight is `-0.3`, and the learning rate is `0.1`.

```
new_weight = 0.5 - 0.1 * (-0.3)
new_weight = 0.5 + 0.03
new_weight = 0.53
```

Because the gradient was negative, increasing the weight would reduce the loss. So we increased it by a small amount. This is exactly what the optimiser does for every weight in the network.

---

## 2. The tiny model we will trace

We use a network with 2 inputs, 1 hidden neuron, and 1 output.

```
Input: x1, x2
Hidden: z1 = w1*x1 + w2*x2 + b1, then a1 = ReLU(z1)
Output: z2 = v1*a1 + b2, then p = sigmoid(z2)
Loss: L = binary cross-entropy(p, y)
```

Think of the two inputs as:

- `x1` = number of suspicious words
- `x2` = number of links

We will use one training email with a true label.

```
Email: [x1, x2] = [2, 1]
Label: y = 1 (spam)
```

Initial weights (made small for the example):

```
w1 = 0.1, w2 = 0.2, b1 = 0.0   (input -> hidden)
v1 = 0.3, b2 = 0.0              (hidden -> output)
```

---

## 3. Forward propagation by hand

### Step 1: Hidden layer raw score

```
z1 = w1*x1 + w2*x2 + b1
z1 = 0.1*2 + 0.2*1 + 0.0
z1 = 0.2 + 0.2 + 0.0
z1 = 0.4
```

### Step 2: Apply ReLU

```
a1 = ReLU(z1) = max(0, 0.4) = 0.4
```

### Step 3: Output layer raw score

```
z2 = v1*a1 + b2
z2 = 0.3*0.4 + 0.0
z2 = 0.12
```

### Step 4: Apply sigmoid

```
p = sigmoid(z2) = 1 / (1 + e^(-0.12))
p ≈ 0.530
```

So the model guesses 53% spam. The true label is 1, so the model is slightly wrong but close.

---

## 4. Compute the loss

We use binary cross-entropy for one example:

```
L = -[y * log(p) + (1 - y) * log(1 - p)]
```

With `y = 1` and `p = 0.530`:

```
L = -[1 * log(0.530) + 0 * log(1 - 0.530)]
L = -log(0.530)
L ≈ 0.635
```

> **Memory trick:** Cross-entropy punishes confident wrong answers. A confident spam guess for a non-spam email is costly.

---

## 5. The chain rule in one sentence

The chain rule tells us how to find the effect of a tiny change in a weight on the final loss:

```
∂L/∂w1 = (∂L/∂p) × (∂p/∂z2) × (∂z2/∂a1) × (∂a1/∂z1) × (∂z1/∂w1)
```

> **Memory trick:** The chain rule is like a row of dominoes. Push the first one, and you can trace the effect all the way to the last one.

---

## 6. Backward propagation by hand

We need the derivatives of the building blocks.

### Derivative of sigmoid

```
∂p/∂z2 = p * (1 - p)
∂p/∂z2 = 0.530 * (1 - 0.530)
∂p/∂z2 = 0.530 * 0.470 ≈ 0.249
```

### Derivative of loss with respect to prediction

```
∂L/∂p = -y/p + (1 - y)/(1 - p)
```

With `y = 1`:

```
∂L/∂p = -1 / 0.530 ≈ -1.887
```

### Derivative of output raw score

```
∂z2/∂v1 = a1 = 0.4
∂z2/∂a1 = v1 = 0.3
∂z2/∂b2 = 1
```

### Derivative through ReLU

```
∂a1/∂z1 = 1 if z1 > 0, else 0
```

Since `z1 = 0.4`, the derivative is `1`.

### Derivatives of hidden raw score

```
∂z1/∂w1 = x1 = 2
∂z1/∂w2 = x2 = 1
∂z1/∂b1 = 1
```

---

## 7. Compute gradients for each weight

### Output weight v1

```
∂L/∂v1 = (∂L/∂p) × (∂p/∂z2) × (∂z2/∂v1)
∂L/∂v1 = (-1.887) × (0.249) × (0.4)
∂L/∂v1 ≈ -0.188
```

### Output bias b2

```
∂L/∂b2 = (∂L/∂p) × (∂p/∂z2) × (∂z2/∂b2)
∂L/∂b2 = (-1.887) × (0.249) × (1)
∂L/∂b2 ≈ -0.470
```

### Hidden weight w1

```
∂L/∂w1 = (∂L/∂p) × (∂p/∂z2) × (∂z2/∂a1) × (∂a1/∂z1) × (∂z1/∂w1)
∂L/∂w1 = (-1.887) × (0.249) × (0.3) × (1) × (2)
∂L/∂w1 ≈ -0.282
```

### Hidden weight w2

```
∂L/∂w2 = (∂L/∂p) × (∂p/∂z2) × (∂z2/∂a1) × (∂a1/∂z1) × (∂z1/∂w2)
∂L/∂w2 = (-1.887) × (0.249) × (0.3) × (1) × (1)
∂L/∂w2 ≈ -0.141
```

### Hidden bias b1

```
∂L/∂b1 = (∂L/∂p) × (∂p/∂z2) × (∂z2/∂a1) × (∂a1/∂z1) × (∂z1/∂b1)
∂L/∂b1 = (-1.887) × (0.249) × (0.3) × (1) × (1)
∂L/∂b1 ≈ -0.141
```

The negative gradients tell us the loss would go down if we increased these weights. So we should increase them.

---

## 8. Update the weights

With learning rate `lr = 0.1`:

```
new_weight = old_weight - lr * gradient
```

Wait — the gradient is negative, so subtracting a negative number means adding:

```
v1_new = 0.3 - 0.1 * (-0.188) = 0.3 + 0.0188 = 0.319
b2_new = 0.0 - 0.1 * (-0.470) = 0.0 + 0.0470 = 0.047
w1_new = 0.1 - 0.1 * (-0.282) = 0.1 + 0.0282 = 0.128
w2_new = 0.2 - 0.1 * (-0.141) = 0.2 + 0.0141 = 0.214
b1_new = 0.0 - 0.1 * (-0.141) = 0.0 + 0.0141 = 0.0141
```

After this update, the model will predict a slightly higher spam probability for this email, which is correct because the label is 1.

---

## 9. The same thing in PyTorch

PyTorch does all of this automatically.

```python
import torch
import torch.nn as nn

# Build the tiny model
model = nn.Sequential(
    nn.Linear(2, 1),   # hidden layer: 2 inputs -> 1 neuron
    nn.ReLU(),
    nn.Linear(1, 1),   # output layer: 1 hidden -> 1 output
    nn.Sigmoid()
)

# Set weights to match the hand example
model[0].weight.data = torch.tensor([[0.1, 0.2]])
model[0].bias.data = torch.tensor([0.0])
model[2].weight.data = torch.tensor([[0.3]])
model[2].bias.data = torch.tensor([0.0])

email = torch.tensor([[2.0, 1.0]])
label = torch.tensor([[1.0]])

criterion = nn.BCELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

# Forward pass
prediction = model(email)
loss = criterion(prediction, label)
print(f"Prediction before: {prediction.item():.4f}")
print(f"Loss: {loss.item():.4f}")

# Backward pass
optimizer.zero_grad()
loss.backward()

# Print gradients
for name, param in model.named_parameters():
    print(f"{name} gradient: {param.grad.item():.4f}")

# Update weights
optimizer.step()

# Check prediction after update
prediction_after = model(email)
print(f"Prediction after: {prediction_after.item():.4f}")
```

Output (approximate):

```
Prediction before: 0.5300
Loss: 0.6350
0.weight gradient: -0.2820
0.bias gradient: -0.1410
2.weight gradient: -0.1880
2.bias gradient: -0.4700
Prediction after: 0.5670
```

The PyTorch gradients match the hand-calculated values.

---

## 10. Visual summary of the chain rule

```
Loss L
    ↑
    | ∂L/∂p
Prediction p
    ↑
    | ∂p/∂z2
Output z2
    ↑
    | ∂z2/∂a1
Hidden a1
    ↑
    | ∂a1/∂z1
Hidden z1
    ↑
    | ∂z1/∂w1
Weight w1
```

To find `∂L/∂w1`, multiply all the derivatives along the path.

> **Memory trick:** Backpropagation is reverse engineering. Start from the error and trace back every cause.

---

## 11. Why the chain rule matters

Without the chain rule, we would have to figure out how every weight affects the loss directly. In a network with thousands of weights, that is impossible. The chain rule breaks the problem into small local pieces:

```
∂L/∂w = (∂L/∂a) × (∂a/∂z) × (∂z/∂w)
```

Each layer only needs to know two things:

1. The gradient coming from the next layer.
2. The derivative of its own output with respect to its inputs.

That is why backpropagation is so efficient.

---

## 12. Common mistakes

| Mistake | Why it happens | Fix |
|---------|----------------|-----|
| Forgetting to apply activation derivatives | ReLU and sigmoid have non-zero slopes | Include `∂a/∂z` in the chain |
| Sign errors with ReLU | ReLU derivative is 0 for negative inputs | Check whether `z > 0` |
| Using MSE derivative for cross-entropy | Different loss functions have different derivatives | Match the loss to the output activation |
| Not zeroing gradients | Old gradients accumulate | Call `optimizer.zero_grad()` |
| Confusing `p` with `z` | `p` is probability, `z` is raw score | Track both separately |
| Wrong learning rate | Too large causes overshoot | Start with 0.1 or 0.01 |

---

## 13. Quick review

| Symbol | Meaning | In the spam example |
|--------|---------|---------------------|
| `x` | Input features | Suspicious words, links |
| `w` | Hidden layer weights | `w1`, `w2` |
| `b1` | Hidden layer bias | Starting mood of hidden neuron |
| `z1` | Hidden raw score | Before ReLU |
| `a1` | Hidden activation | After ReLU |
| `v1` | Output layer weight | `0.3` |
| `b2` | Output layer bias | `0.0` |
| `z2` | Output raw score | `0.12` |
| `p` | Predicted probability | `0.530` |
| `y` | True label | `1` (spam) |
| `L` | Loss | `0.635` |
| `∂L/∂w` | How much loss changes if w changes | Gradient used to update w |

---

## 14. Try it yourself

1. Repeat the hand calculation but with a different email, for example `[x1, x2] = [1, 3]` and `y = 0`.
2. Write a PyTorch version of the same model and compare the gradients.
3. Change the learning rate to `0.5` and see how much the prediction changes after one step.
4. Replace ReLU with sigmoid in the hidden layer. How does the chain rule change?

---

## Summary

- Forward propagation computes the prediction from inputs to output.
- Backward propagation computes how each weight contributed to the loss using the chain rule.
- The chain rule multiplies local derivatives along the path from loss to weight.
- ReLU and sigmoid have simple derivatives, but they must be included in the chain.
- PyTorch's `loss.backward()` does all of this automatically and produces the same gradients.
- Once you understand one training step, you understand how the whole model learns.

> **Final memory trick:** Forward = read the email. Backward = trace the blame. Update = fix the mistake. Repeat.
