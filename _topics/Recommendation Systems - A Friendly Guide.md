---
title: "Recommendation Systems - A Friendly Guide"
category: Advanced Machine Learning
order: 13
permalink: /topics/recommendation-systems-friendly-guide/
tags:
  - recommendation-systems
  - collaborative-filtering
  - matrix-factorization
  - implicit-feedback
summary: "A beginner-friendly guide to how recommendation systems work: people-who-bought-this, people-like-you, hidden taste maps, and learning from clicks instead of star ratings."
date: 2026-08-30
---

# Recommendation Systems - A Friendly Guide

A recommendation system answers a simple question: **what should this person see next?**

It is the engine behind movie suggestions, music playlists, shopping suggestions and news feeds. This guide explains the big ideas in plain English.

---

## 1. The three big families

There are three ways to recommend something.

1. **Frequently together:** "People who bought X also bought Y."
2. **Taste neighbours:** "People like you enjoyed this."
3. **Hidden taste map:** "We can compress every person and every item into a small list of traits and guess missing likes."

A production system often combines all three.

---

## 2. Frequently together — the shop-shelf idea

This is the simplest recommendation of all.

Imagine a small grocery shop. Every time a customer checks out, you write the basket on a card. After a thousand customers you notice that **bread and butter** appear together over and over. So when someone puts bread in their basket, you say, "Would you like butter too?"

This method only cares about items. It does not care who the customer is. It just counts which pairs of items show up in the same basket, playlist or session.

### Why it works

- Simple to compute.
- No user profiles needed.
- Great for items that naturally belong together.

### Why it struggles

- Cannot recommend a brand-new item.
- Cannot personalise for one specific person.
- Makes the rich richer — popular items get recommended even more.

---

## 3. Taste neighbours — people like you

This is the most famous idea. Instead of looking at the item, look at the **person**.

### A tiny story

Alice loves sci-fi, documentaries and jazz. Bob loves sci-fi, documentaries and classical. They have two tastes in common. If Alice just discovered a great jazz album, the system might tell Bob, "Since you also like sci-fi and documentaries, you may enjoy this album."

This is **user-user** matching.

You can also flip it around. Instead of finding people like Alice, you can find **items like the ones Alice already likes**. If Alice loved movie A, and most people who loved movie A also loved movie B, recommend movie B.

That is **item-item** matching.

### Measuring similarity

The usual tool is a user-item table.

```
         Movie A   Movie B   Movie C
Alice       5         3          ?
Bob         5         2         4
Carol       1         4         5
Dave        3         3         5
```

For **user-user** similarity, treat each row as a vector. Alice and Bob are similar because their rows are close.

For **item-item** similarity, treat each column as a vector. Movie A and Movie B are compared using the ratings given by all users.

A common way to measure that distance is to look at the angle between the two vectors. A small angle means high similarity. This is the same idea as cosine similarity in many clustering and NLP tutorials.

### A worked example

Here is a tiny table of books.

| User  | Fantasy | Mystery | Romance | Sci-Fi |
|-------|---------|---------|---------|--------|
| Ada   |    1    |    0    |    1    |   1    |
| Ben   |    1    |    1    |    0    |   0    |
| Cal   |    0    |    1    |    1    |   1    |
| Dee   |    1    |    0    |    1    |   0    |

Ada likes Fantasy, Romance and Sci-Fi. Cal likes Mystery, Romance and Sci-Fi. Their tastes overlap on two out of three genres, so they are taste neighbours. If Cal loved a new Mystery book, the system may recommend it to Ada because their profiles are close.

---

## 4. Hidden taste map — the compressed profile

Real catalogues can have thousands of items. You cannot compare people by asking, "Do you like item 1, item 2, item 3 ... ?" for every single product.

Instead, imagine that every person and every item can be described by a small list of hidden traits.

For movies, the hidden traits might be things like:

- how much dark humour it contains
- how family-friendly it is
- how action-heavy it is
- how long and slow it is

A person has scores for each trait. An item has scores for each trait. If a person and an item have similar trait scores, the person will probably like the item.

This is the idea behind **matrix factorisation**. You learn the hidden trait scores from the data.

### Analogy: the flavour wheel

Think of a coffee taster's flavour wheel. It is impossible to describe every coffee by listing every chemical. Instead, experts use a small set of sliders: acidity, body, sweetness, bitterness, fruitiness. Two coffees are similar if their sliders are close. A person who loves fruity, low-bitterness coffees will probably like any coffee near that corner of the wheel.

Recommendation systems do the same thing. They invent the sliders from the data instead of asking a human to define them.

---

## 5. Implicit feedback — learning from clicks

Most of the time, people do not give star ratings. They just watch, click, buy or skip. This is called **implicit feedback**.

The signal is weaker than a five-star rating, but it is much more abundant.

| Type of feedback | What it tells you |
|------------------|-------------------|
| Clicked          | The title or cover was interesting enough to look at. |
| Watched 80%      | The user probably liked it. |
| Bought           | Strong positive signal. |
| Skipped quickly  | Probably not interested. |

A system with implicit feedback learns to predict whether a user will interact with an item. The prediction is usually a single score. Higher means "this user is more likely to engage with this item."

---

## 6. Two ways to learn the hidden taste map

There are many ways to train a matrix factorisation model. Two of the most common are:

### Team A / Team B racing

One team is in charge of the user trait scores. The other team is in charge of the item trait scores. They take turns. Team A fixes the item scores and improves the user scores. Then Team B fixes the new user scores and improves the item scores. They keep taking turns until the guesses stop improving.

This is the basic idea behind **alternating least squares**.

### Pair by pair ranking

Another approach does not try to predict the exact score. Instead, it asks a simpler question: for this user, should item A be ranked above item B?

For every user, you pick an item they liked and an item they did not like. The model learns to give the liked item a higher score than the disliked item. This is called pairwise ranking.

This is the basic idea behind **Bayesian personalised ranking**.

### Stopping the model from getting too confident

If a model is too confident, it memorises the training data and fails on new users or items. A small penalty on the size of the trait scores keeps the model humble. This penalty is called regularisation.

---

## 7. Which approach should you use?

| Situation | Start with |
|-----------|------------|
| You only have shopping baskets or playlists | Frequently together |
| You have explicit ratings like stars | User-user or item-item collaborative filtering |
| You have millions of clicks or views | Matrix factorisation with implicit feedback |
| You need quick, interpretable results | User-user or item-item with cosine similarity |
| You want the best possible score and have lots of data | Modern matrix factorisation libraries |

---

## 8. One-sentence takeaways

- **Frequently together** recommends items that are often seen together.
- **Collaborative filtering** recommends what similar people, or similar items, already liked.
- **Matrix factorisation** learns a hidden taste map for both people and items.
- **Implicit feedback** lets you learn from clicks, views and purchases instead of asking for ratings.
