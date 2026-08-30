---
title: "Recommendation Systems - Part 3 - Models, Ranking and Multi-Modal Systems"
category: Advanced Machine Learning
order: 15
permalink: /topics/recommendation-systems-models-ranking-multimodal/
tags:
  - recommendation-systems
  - collaborative-filtering
  - matrix-factorization
  - learning-to-rank
  - negative-sampling
  - multi-modal
summary: "The main models and techniques: collaborative filtering, implicit matrix factorisation with ALS and BPR, learning-to-rank, negative sampling, feature generation and multi-modal recommendation."
date: 2026-08-30
---

# Recommendation Systems - Part 3 - Models, Ranking and Multi-Modal Systems

This part covers the models that turn data into recommendations. We start with the simplest user-item matching, move to latent-factor models, and end with modern ideas like multi-modal systems.

---

## 1. Collaborative filtering

Collaborative filtering means: use the behaviour of many users to guess what a single user will like.

There are two main directions.

- **User-user:** find people similar to you.
- **Item-item:** find items similar to the ones you already like.

### User-user collaborative filtering

The idea is simple.

1. Build a profile for each user. The profile is a vector of their past interactions.
2. Find the users whose profiles are most similar to the target user.
3. Recommend the items those similar users liked.

### Example

Three users have watched some of the same movies.

```
          Movie A   Movie B   Movie C   Movie D
Alice        5         3         0         4
Bob          4         3         0         5
Carol        0         4         5         1
```

Alice and Bob have very similar rows. If Bob loved movie B and movie D, those are safe recommendations for Alice.

Carol is different. Recommending Carol's favourites to Alice may not work.

### The user-user prediction formula

For user `u` and item `i`:

```
predicted_score(u, i) = average_score(u) +
    Σ similarity(u, v) × (actual_score(v, i) - average_score(v))
    ----------------------------------------------------------
                 Σ |similarity(u, v)|
```

The sum is over all users `v` who are similar to `u` and who have rated item `i`.

The formula does three things:
1. Start from the user's own average.
2. Add a weighted adjustment from similar users.
3. Divide by the total weight so the result is an average adjustment.

### Item-item collaborative filtering

This is often more practical than user-user, because user profiles are sparse and change quickly. Item profiles are usually more stable.

1. Build a profile for each item. The profile is the list of users who liked it.
2. Find the items most similar to the ones the target user already liked.
3. Recommend those items.

### The item-item similarity formula

For two items `i` and `j`, use the users who interacted with both.

```
cosine_similarity(i, j) = Σ (r_ui × r_uj)
                        / sqrt(Σ r_ui²) × sqrt(Σ r_uj²)
```

The sums are over all users `u` who have a score for both items. `r_ui` is the score user `u` gave to item `i`.

A high cosine similarity means the two items appeal to the same people.

### User-user vs item-item

| Situation | Better choice |
|-----------|---------------|
| Many more users than items | Item-item |
| Items change quickly | User-user |
| You want explanation | Item-item is easier to explain: "people who liked X also liked Y" |
| Sparsity is very high | Item-item is usually more stable |

---

## 2. Implicit matrix factorisation

Matrix factorisation is the most important classical model for large-scale recommendations. It learns hidden traits for users and items.

### The big picture

Imagine a huge table.

```
         Item 1   Item 2   Item 3   ...   Item n
User 1     ?        1        0     ...      ?
User 2     1        ?        1     ...      ?
User 3     0        0        ?     ...      1
...       ...      ...      ...    ...    ...
```

A `1` means the user interacted with the item. A `0` or `?` means they did not, or we do not know.

This table is mostly empty. We want to fill in the missing values with the probability that each user will like each item.

### The model idea

Give every user a small trait vector `p_u` and every item a small trait vector `q_i`.

```
predicted_score(u, i) = p_u · q_i
```

The dot product is:

```
p_u · q_i = p_u1 × q_i1 + p_u2 × q_i2 + ... + p_uk × q_ik
```

If the user and the item have similar traits, the dot product is high. If they have opposite traits, the dot product is low.

### Explicit feedback loss

When we have real ratings `r_ui`, the usual loss is squared error:

```
L = Σ (r_ui - p_u · q_i)²
```

We try to make the predicted score as close as possible to the real rating.

### Implicit feedback loss

When we only have clicks or views, the signal is different. We use a confidence value `c_ui` for each user-item pair.

```
c_ui = 1 + α × observed_interactions(u, i)
```

Here `α` is a tuning number, usually something like 40. If a user watched a video ten times, we have more confidence that they like it than if they watched it once.

The loss becomes:

```
L = Σ c_ui × (p_ui - p_u · q_i)²
```

Where `p_ui` is 1 if the user interacted and 0 if not. The `c_ui` weight means frequent interactions matter more.

### Regularisation

We do not want the vectors to become huge. A small penalty keeps them modest:

```
L_total = L + λ × (Σ ||p_u||² + Σ ||q_i||²)
```

The `λ` controls the strength. A larger `λ` keeps vectors small. A smaller `λ` lets the model fit the data more closely.

---

## 3. Alternating least squares (ALS)

ALS is a clever way to solve the matrix factorisation problem.

### The two-team idea

We have two sets of unknowns: user vectors and item vectors. We cannot solve for both at the same time easily. But if we fix one set, the other set has a closed-form solution.

So we take turns.

1. Fix all item vectors `q_i`.
2. Solve for the best user vectors `p_u`.
3. Fix all user vectors `p_u`.
4. Solve for the best item vectors `q_i`.
5. Repeat.

Because each step is a simple least-squares problem, it is fast and stable.

### Why it works

Each step is a convex problem. That means there is a single best answer, and we can find it directly. By alternating, we slowly find a good pair of user and item vectors.

### The ALS update rule

For a fixed set of item vectors, the best user vector is:

```
p_u = (Q^T C_u Q + λI)^-1 Q^T C_u p_u_binary
```

Where:

- `Q` is the matrix of item vectors.
- `C_u` is a diagonal matrix of confidence values for user `u`.
- `p_u_binary` is the binary preference vector for user `u`.
- `λI` is the regularisation term.
- `^-1` means matrix inverse.

Then the same formula, with the roles swapped, gives the item vectors.

You do not need to remember this formula. The important idea is: hold one side still, solve the other side, then switch.

---

## 4. Bayesian personalised ranking (BPR)

BPR does not try to predict the exact score. It tries to make sure that for every user, the items they liked are ranked above the items they did not like.

### The triplet idea

For each user, create triples:

```
(user u, positive item i, negative item j)
```

- `i` is an item the user actually liked.
- `j` is an item the user did not like or did not see.

The goal is:

```
p_u · q_i  >  p_u · q_j
```

In words: the model should give a higher score to the liked item than to the disliked item.

### The BPR loss

The loss is:

```
L_BPR = -ln(σ(p_u · q_i - p_u · q_j))
```

Where `σ` is the sigmoid function:

```
σ(x) = 1 / (1 + e^(-x))
```

If `p_u · q_i` is much larger than `p_u · q_j`, then `p_u · q_i - p_u · q_j` is a large positive number. The sigmoid is close to 1, and the log of 1 is 0. So the loss is small. That is good.

If the model gets the order wrong, the difference is negative. The sigmoid is close to 0, and the log of a small number is very negative. With the minus sign in front, the loss becomes large. That is bad.

### Why BPR is popular

- It only needs positive and negative examples.
- It focuses on ranking, which is what most systems actually need.
- It is easy to train with stochastic gradient descent.

---

## 5. Learning-to-rank

Learning-to-rank trains a model to sort items correctly.

There are three styles.

### Pointwise

Predict a score for each item independently. Then sort by that score. Matrix factorisation and many neural models are pointwise.

```
score(u, i) = p_u · q_i
```

### Pairwise

Compare two items at a time. BPR is a pairwise method. It trains the model to rank positive items above negative items.

```
L = -ln(σ(score(u, i) - score(u, j)))
```

### Listwise

Compare the whole list at once. The model optimises the ranking of the full set of items. This can be more accurate but is also harder and slower.

```
L = -Σ P(actual order) × log(P(predicted order))
```

Listwise methods try to match the full probability distribution over rankings.

### When to use each

| Style | Use when |
|-------|----------|
| Pointwise | You have ratings or confidence scores. |
| Pairwise | You have implicit feedback and want ranking. |
| Listwise | You can afford more computation and want the best possible order. |

---

## 6. Negative sampling

In implicit feedback, we have lots of positive examples but no explicit negative examples. A user might not have clicked an item because they did not like it, or because they never saw it.

Negative sampling is how we create negative examples to train the model.

### Random negative sampling

For each positive pair `(u, i)`, pick a random item `j` that the user has not interacted with. Treat `j` as a negative.

This is simple, but the random item is often very easy to recognise as negative. The model does not learn much.

### Hard negative sampling

Pick items that are popular and similar to the positive item, but the user did not choose them. These are harder to distinguish.

For example, if a user bought a mystery novel, a hard negative might be another popular mystery novel that they did not buy.

### In-batch negative sampling

Use the other positive examples in the same training batch as negatives. This is fast and works well for neural recommenders.

### The negative sampling ratio

A common choice is to use a few negatives for every positive. For example, four negatives per positive.

```
number_of_negatives = k × number_of_positives
```

A larger `k` gives the model more negative examples to learn from, but also makes training slower.

### Why negative sampling matters

Without negatives, the model would learn that every user-item pair is positive. Negative examples force the model to learn what users do not want, not just what they do want.

---

## 7. Feature engineering for recommendations

Good features make every model better. Here are the main types.

### User features

- Past interactions: items, categories, brands.
- Frequency: how often they visit, buy or watch.
- Recency: time since last interaction.
- Demographics: age, location, language.
- Time patterns: morning vs evening, weekday vs weekend.

### Item features

- Category, brand, price, age, popularity.
- Content: text, images, audio, video.
- Quality: average rating, return rate, dwell time.
- Trend: rising or falling popularity.

### Context features

- Device, location, time of day.
- Season, weather, holidays.
- Whether the user is in a rush or browsing.

### Sequence features

Instead of just a list of items, capture the order.

- Last five items viewed.
- Items viewed in the current session.
- Time between interactions.

### Feature crosses

Some combinations matter more than the individual parts.

For example, `category_morning` might tell you that users in the morning prefer news, while in the evening they prefer movies.

```
category_morning = category × time_of_day
```

Modern models can learn some crosses automatically, but hand-crafted crosses are still useful.

---

## 8. Multi-modal recommendation systems

So far, we have used interaction data. But real catalogues also have text, images, sound, and video.

A multi-modal system uses more than one type of input.

### Text as a signal

For products, we have titles and descriptions. We can turn the text into a vector using a language model. Two items with similar descriptions get similar vectors.

```
item_text_vector = language_model(description)
```

### Images as a signal

For fashion or furniture, the visual look is important. A computer-vision model can turn an image into a vector. Two visually similar items get similar vectors.

```
item_image_vector = vision_model(image)
```

### Audio and video

For music and movies, the raw content can be converted into vectors. A song with a similar mood and tempo gets a similar vector.

### Cold start

A common problem is the **cold start**: a brand-new item has no interactions yet. Multi-modal features help here. Even if no one has bought the new item, the system can recommend it to users who liked similar-looking or similar-described items.

### Fusing modalities

The system must combine the different vectors. A simple way is to concatenate them:

```
item_vector = [interaction_vector, text_vector, image_vector]
```

Then use this combined vector in a matrix factorisation or neural model. Modern systems can also use attention to decide which modality matters most for each user and item.

---

## 9. Building a small end-to-end system

Here is a simple blueprint.

1. **Collect events** with a clear data contract: who, what, when, how.
2. **Choose the problem type:** explicit rating, implicit click, ranking, or next action.
3. **Split the data** by time or by user. Make sure there is no leakage.
4. **Build baselines:** global popularity, item co-occurrence, recent history.
5. **Measure with offline metrics:** Recall, Precision, NDCG, MRR, coverage, personalisation.
6. **Train a simple matrix factorisation** model with ALS or BPR.
7. **Add negative sampling** and learning-to-rank if needed.
8. **Add features and multi-modal signals** for better cold-start and quality.
9. **Run an online A/B test** to confirm the offline gains appear in production.

---

## 10. One-sentence takeaways

- **Collaborative filtering** matches users to users or items to items.
- **Matrix factorisation** learns hidden user and item traits as vectors.
- **ALS** solves the problem by alternating between fixing users and fixing items.
- **BPR** trains the model to rank positive items above negatives.
- **Learning-to-rank** can be pointwise, pairwise, or listwise.
- **Negative sampling** creates the negative examples the model needs to learn.
- **Feature engineering** adds user, item, context, and sequence signals.
- **Multi-modal systems** use text, images, and audio to help cold-start items.
