---
title: "Recommendation Systems - Part 2 - Framing, Data, Metrics and Baselines"
category: Advanced Machine Learning
order: 14
permalink: /topics/recommendation-systems-framing-data-metrics-baselines/
tags:
  - recommendation-systems
  - recsys-framing
  - evaluation-metrics
  - data-signals
  - baselines
summary: "The foundations of recommendation systems: how to frame the problem, what data to collect, how to build data contracts, how to split data without leaking the future, and the most useful offline evaluation metrics."
date: 2026-08-30
---

# Recommendation Systems - Part 2 - Framing, Data, Metrics and Baselines

This part builds the foundation. Before we train fancy models, we need to know what the problem is, what data we can use, how to avoid fooling ourselves with a bad test set, and how to measure success.

---

## 1. What problem are we really solving?

A recommendation system is a sorting machine. Given a person and a huge catalogue, it puts the items the person is most likely to enjoy at the top of the list.

There are several different ways to ask the question.

### The three common tasks

1. **Predict a rating.**
   "How many stars will Alice give to this movie?"
   This is a regression task. We minimise the error between the predicted and the actual star rating.

2. **Predict a ranking.**
   "Which ten movies should Alice see first?"
   This is a ranking task. We care about the order of the list, not the exact score.

3. **Predict the next action.**
   "What is Alice most likely to click or buy next?"
   This is a classification or click-through prediction task. We have positive and negative examples from real behaviour.

Most production systems end up as ranking or next-action problems, because the exact rating matters less than the order.

### A simple framing rule

- **Input:** a user, their past behaviour, and the item catalogue.
- **Output:** a sorted list of items the user is most likely to interact with.
- **Goal:** the best items should appear before the less interesting items.

---

## 2. Types of recommendation problems

Not every system needs the same design. The problem type shapes the model, the metric, and the data you collect.

### Explicit feedback problems

The user gives a direct opinion.

- Star ratings.
- Thumbs up or thumbs down.
- Written reviews.

These are gold, but rare. Most users do not rate. A movie site may have millions of views and only tens of thousands of ratings.

### Implicit feedback problems

The user gives an opinion through behaviour.

- Clicked on an item.
- Watched 90% of a video.
- Added to basket.
- Bought.
- Skipped after two seconds.

These are much more common, but the signal is noisy. A click does not always mean "I loved it." It may only mean the title was interesting.

### Session-based problems

The user is anonymous or new. We only have the current session. The model must recommend based on what has been viewed in this session.

This is common for news and e-commerce without accounts.

### Sequence problems

We have the exact order of actions over time. The model tries to predict the next item in the sequence. This is like language modelling, but for items.

### Diversity and serendipity problems

Sometimes the goal is not just accuracy. We also want the user to discover surprising things. A music app may want to mix known favourites with new genres.

---

## 3. The data we collect

Data is the raw material. The way you store and interpret it shapes everything that follows.

### User signals

Signals tell us who the user is and what they did.

| Signal | Meaning | Strength |
|--------|---------|----------|
| Viewed | The user opened the item. | Weak but abundant. |
| Clicked | The user actively selected it. | Slightly stronger. |
| Dwell time | How long they looked or listened. | Stronger. 30 seconds vs 30 minutes means very different things. |
| Added to cart | Strong interest. | Strong. |
| Purchased | Strongest positive signal. | Very strong. |
| Skipped | Not interested. | Negative signal. |
| Dislike | Explicit negative. | Strong negative. |

### Item signals

Signals about the items themselves.

- Category, brand, price, tags.
- Text description.
- Image or video.
- Popularity, average rating, recency.

### Context signals

Signals about the situation.

- Time of day, day of week, season.
- Device, location, platform.
- Whether the user is at home or commuting.

The same person wants different things on a Monday morning and a Friday night.

---

## 4. Data contracts and what the numbers really mean

A **data contract** is an agreement about what each event means. If one event is a "view" and another event is a "purchase," they are not the same thing.

### Why this matters

If you treat a one-second glance the same as a finished movie, the model learns nonsense.

A good data contract answers these questions for every event:

- **Who?** The user or session identifier.
- **What?** The item identifier.
- **When?** The exact timestamp.
- **How?** The action type: view, click, cart, purchase, skip, like, rate, etc.
- **Where?** The page or context.
- **How much?** Optional: dwell time, purchase value, rating value.

### The signal-strength idea

One way to turn a raw event into a number is to assign a weight.

```
signal_strength = weight(action) × confidence(action)
```

For example:

| Action | Weight | Reason |
|--------|--------|--------|
| View   | 1      | The user saw it. |
| Click  | 2      | They chose it. |
| Cart   | 4      | Strong interest. |
| Buy    | 8      | Strongest signal. |
| Skip   | -1     | Negative signal. |
| Dislike| -4     | Strong negative. |

These weights are engineering choices, not universal truths. A streaming app may value "watched to 80%" more than "clicked."

### Dwell time as a continuous signal

Dwell time can be used directly:

```
dwell_signal = min(dwell_time / target_time, 1.0)
```

If a song is three minutes and the user listened to all three minutes, the signal is 1.0. If they stopped after thirty seconds, the signal is 0.17.

---

## 5. Offline evaluation metrics

Before the system goes live, we test it on historical data. This is **offline evaluation**. We need metrics that tell us whether the ranking is good.

### The ideal outcome

If the user interacted with item A but not item B, then in the recommended list item A should appear above item B.

### Recall

Recall asks, "Of the items the user actually liked, how many did we put in the top list?"

```
Recall@K = (number of liked items in top K) / (total number of liked items)
```

If a user liked 10 items and we put 4 of them in the top 20, then `Recall@20 = 4 / 10 = 0.4`.

### Precision

Precision asks, "Of the items we put in the top list, how many did the user actually like?"

```
Precision@K = (number of liked items in top K) / K
```

If we recommend 20 items and 4 are liked, `Precision@20 = 4 / 20 = 0.2`.

### Hit rate

Hit rate is a simple yes-or-no version of recall.

```
HitRate@K = 1 if at least one liked item is in the top K, else 0
```

It is easy to understand but does not care about the exact position.

### Mean Reciprocal Rank (MRR)

MRR cares about the first good item.

```
MRR = (1 / rank of the first relevant item) averaged over all users
```

If the first relevant item is at position 3 for one user and position 1 for another, the average is `(1/3 + 1/1) / 2 = 0.667`.

### Mean Average Precision (MAP)

MAP is precision averaged over every position where a relevant item appears.

For one user, **Average Precision (AP)** is:

```
AP = (1 / number of liked items) × Σ Precision at each rank where a liked item appears
```

Then MAP is the average of AP across all users. It rewards putting many relevant items near the top.

### Normalised Discounted Cumulative Gain (NDCG)

NDCG is the most common ranking metric when items are not equally relevant.

If a user liked an item a little, that is worth some points. If they loved it, it is worth more points. Positions near the top count more than positions further down.

The formula works in two steps.

1. Compute the **Discounted Cumulative Gain (DCG)** at rank `K`:

```
DCG@K = Σ (relevance_score at position i) / log2(i + 1)
```

2. Divide by the **Ideal DCG (IDCG)**, which is the best possible score:

```
NDCG@K = DCG@K / IDCG@K
```

Because of the `log2(i + 1)` in the denominator, a highly relevant item at position 1 gives a much bigger score than the same item at position 10.

### Coverage

Coverage asks, "How many different items does the system ever recommend?" A system that recommends the same popular items to everyone has low coverage.

```
Coverage = (number of unique recommended items) / (total number of items)
```

A good system balances accuracy with coverage, so long-tail items also get a chance.

### Personalisation

Personalisation measures how different the recommendations are from one user to another. If every user sees the same list, personalisation is zero.

```
Personalisation = average dissimilarity between pairs of users' top-K lists
```

This is not always desirable. Some users in a community may genuinely like the same things. But a low score is often a warning sign that the system is too generic.

---

## 6. Evaluation splits and leakage prevention

The biggest mistake in recommendation evaluation is to let the model peek at the future.

### The golden rule

A model should only be trained on events that happened **before** the events it is tested on.

If you use a click from Tuesday to recommend an item that was viewed on Monday, the model has seen the future. That is **leakage**, and it makes the results look much better than they really are.

### Time-based split

Sort every interaction by timestamp.

1. Train on the oldest 80%.
2. Validate on the next 10%.
3. Test on the newest 10%.

This mirrors the real world. The model is trained on the past and tested on the future.

### User-based split

A stronger split is to hide all future interactions of some users.

1. Pick a set of test users.
2. Use their past interactions for training.
3. Hide their future interactions for testing.

This is more realistic. In production, the model sees a user's past and must predict their future.

### Leave-one-out

A common benchmark style is to hide exactly one interaction per user. The model is given the user's other interactions and must predict the hidden one.

This is simple and fast, but it does not represent the real world perfectly. Users usually have many future actions, not just one.

### Popularity leakage

A subtle form of leakage is to include the test item in the popularity count used during training. For example, if you compute how often an item was bought in the whole dataset, and that includes test data, the model has an unfair advantage.

Always compute popularity from training data only.

---

## 7. Baseline models

Before you build a complex model, you need a simple baseline. A baseline sets a floor. If your fancy model cannot beat a simple rule, it is not ready.

### 1. Global popularity

Recommend the most popular items to everyone.

```
score(item) = number of times the item was interacted with
```

This is surprisingly strong. It has no personalisation, but it works because popularity often means quality.

### 2. Personal popularity

Recommend the items that the current user has interacted with the most.

```
score(item for user u) = number of times u interacted with item
```

This is the "just show me more of the same" baseline.

### 3. Item co-occurrence

If a user has item A, recommend the items most often seen with A.

```
score(item B for user with A) = count of sessions with both A and B
```

This is the bread-and-butter baseline for shopping carts.

### 4. Recent history

Recommend the most recent items the user looked at, or items similar to them.

This is a strong baseline for news, short videos, and feeds, because users often want more of what they were just looking at.

### 5. Simple matrix factorisation

A small latent-factor model is a good middle baseline. It is not as trivial as popularity, but not as complex as a neural network.

### How to use baselines

1. Build the baseline first.
2. Measure it with the same metrics you plan to use for the final model.
3. Only move to a complex model when you can clearly beat the baseline.

---

## 8. Putting it together: a one-page checklist

Before training a recommendation model, ask:

1. What is the real goal — rating, ranking, or next action?
2. Is the data explicit or implicit?
3. Do we have user accounts, or are we session-based?
4. How strong is each signal?
5. What time split are we using?
6. Are we leaking any future information?
7. What baseline are we trying to beat?
8. Which metric matters most for the business?

If you answer these clearly, the rest of the pipeline becomes much easier.
