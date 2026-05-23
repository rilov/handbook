---
title: "02. ML in Plain English - A Friendly Tour"
category: Machine Learning
order: 2
tags:
  - machine-learning
  - overview
  - non-technical
  - story
  - beginners
summary: A friendly story-style tour of every machine learning technique covered in this handbook. No math, no code, no jargon. Just a clear, plain English explanation of what each tool does and when you would actually use it in real life.
---

# ML in Plain English - A Friendly Tour

## Why this page exists

Machine learning has a lot of names. Linear regression, logistic regression, regularization, decision trees, random forests, gradient boosting, K-Means, hierarchical clustering, KNN.

When you read those words for the first time, they all sound like a bunch of math you do not want to do.

But here is the truth. Every one of these techniques was invented to solve a real problem that a real human had. If you understand the problem first, the technique stops looking like math and starts looking like common sense.

This page is a friendly tour. No equations. No code. No jargon. Just a story for each technique, told the way you would explain it to a friend over coffee.

By the end of this page you will know what each tool actually does, and roughly when you would reach for it in real life. Then when you go into the detailed tutorials, you will already have the big picture in your head.

Let us go.

---

## The big split, supervised vs unsupervised

Before we meet any specific tool, there is one fork in the road.

Imagine you run a small bakery. You have years of records. Some days you sold a lot of bread. Some days you sold very little. You have notes about each day: the weather, whether it was a weekend, whether there was a holiday, the price of flour.

Now ask yourself two very different questions.

**Question 1.** "Given tomorrow's weather and the day of the week, can you tell me how much bread I will sell?"

This is **supervised learning**. You have past examples where you know the answer (how much bread sold), and you want a model that can give you the answer for a new day.

**Question 2.** "I have five years of daily records. Can you tell me if there are some natural types of days, like 'busy weekend days' or 'rainy slow days', without me telling you what to look for?"

This is **unsupervised learning**. You have data but no answers. You just want to discover hidden structure.

Almost everything in machine learning falls into one of these two camps. Now let us walk through the techniques you will meet.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    ML["<b>Machine Learning</b>"]
    ML --> SUP["<b>Supervised</b><br/>You have answers<br/>in the training data"]
    ML --> UNS["<b>Unsupervised</b><br/>No answers,<br/>just data"]
    SUP --> REG["<b>Regression</b><br/>predict a number<br/>(price, demand)"]
    SUP --> CLS["<b>Classification</b><br/>predict yes/no<br/>or a category"]
    UNS --> CLUS["<b>Clustering</b><br/>find hidden groups"]
    UNS --> SIM["<b>Similarity</b><br/>compare items"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class REG,CLS,CLUS,SIM gray
    class ML,SUP,UNS midgray
</div>

---

## Linear Regression, the straight line guesser

Imagine you want to predict the price of a house. You collect a bunch of past sales. For each house you know its size in square feet and what it sold for.

If you plotted these on a graph, you would see roughly that bigger houses sell for more. Not exactly, but roughly. If you took a ruler and drew the single best straight line through all those dots, you would have a tool that turns any house size into a predicted price.

That is **linear regression**. It is the act of finding the best straight line through your data.

When you have more than one input, like size and number of bedrooms and age, linear regression still works. It just becomes a "line" in many dimensions. You cannot draw it on paper anymore, but the math is the same.

**When you actually use linear regression in real life.**

* Predicting house prices, sales numbers, electricity demand, anything that is a continuous number.
* Estimating how much one thing affects another. "If I spend one more dollar on ads, how many more sales do I get?"
* As a quick, simple baseline before trying anything fancier.

It is the oldest, simplest tool in the kit. And often, it is good enough.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    D["<b>Past sales data</b><br/>house size + price"]
    D --> L["<b>Best straight line</b><br/>through the dots"]
    L --> P["<b>Predicted price</b><br/>for a new house"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class L gray
    class D,P midgray
</div>

---

## Logistic Regression, the yes-or-no decider

Now imagine your problem is different. Instead of predicting a number, you want a yes or no answer.

A customer signs up for your service. Will they cancel within a month? Yes or no?

A doctor takes a blood test. Does this person have the disease? Yes or no?

You cannot draw a straight line for yes-or-no questions. There is no "halfway yes". But there is a clever trick. You can draw a curve that smoothly slides from 0 (definitely no) to 1 (definitely yes), passing through 0.5 in the middle (could go either way).

That smooth curve is called the **sigmoid**, and the technique that uses it is called **logistic regression**.

Despite the misleading name (it has "regression" in it but it is actually used for classification), logistic regression is the standard yes-or-no model in the world. Banks use it to decide loans. Email providers use it for spam. Hospitals use it for risk prediction.

**When you actually use logistic regression in real life.**

* Will this customer churn? Yes or no.
* Is this transaction fraudulent? Yes or no.
* Will this patient respond to treatment? Yes or no.
* Will the visitor click the ad? Yes or no.

It is the bread-and-butter classifier of the business world.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    F["<b>Customer info</b><br/>age, usage, plan"]
    F --> S["<b>Sigmoid curve</b><br/>maps to 0...1"]
    S --> D{"<b>Threshold</b><br/>above 0.5?"}
    D -->|yes| Y["<b>Predict: Will churn</b>"]
    D -->|no| N["<b>Predict: Will stay</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class S,D gray
    class F,Y,N midgray
</div>

---

## Regularization, the discipline that stops models from going crazy

Both linear and logistic regression have a weakness. If you give them too many features, they get carried away.

Imagine a student studying for an exam. A focused student learns the main ideas and does well. A panicky student memorises every single page word for word and does brilliantly on the practice test but freezes on the real exam, because the real exam has slightly different questions.

That panicky student has **overfit** to the practice material. They learned the specifics but not the patterns.

Models do the same thing. If you give them too many features, they start to memorise the noise in your training data instead of the real signal. They look great on the data they saw and terrible on new data.

**Regularization** is the cure. It is a way of telling the model "be reasonable, do not trust any single feature too much". It gently shrinks the influence of each feature toward zero, keeping the model honest.

There are three main flavours.

* **Ridge** says "be reasonable, smooth things out a bit". It shrinks every feature gently.
* **Lasso** is stricter. It says "if a feature is not really pulling its weight, drop it completely". Lasso actually picks features for you.
* **Elastic Net** is the compromise child of Ridge and Lasso. A bit of both.

**When you actually use regularization in real life.**

* Almost any time you have more than a handful of features.
* When your model performs great on training data but poorly on new data.
* When you have many features and want the model to pick the important ones automatically.

In modern practice, regularization is on by default. It is not optional, it is hygiene.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    M["<b>Plain Model</b><br/>memorizes everything,<br/>including noise"]
    M --> R["<b>+ Regularization</b><br/>be reasonable,<br/>do not trust any single<br/>feature too much"]
    R --> RID["<b>Ridge</b><br/>shrink all features<br/>gently"]
    R --> LAS["<b>Lasso</b><br/>drop weak features<br/>completely"]
    R --> EL["<b>Elastic Net</b><br/>a bit of both"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class RID,LAS,EL gray
    class M,R midgray
</div>

---

## Decision Trees, the game of 20 questions

Linear models are smooth. They draw lines. But the world is often not smooth.

A loan officer probably does not say "every extra year of age adds 0.4 to your loan score". They probably say "if you are over 30 AND you have a stable job AND your debt-to-income is under 35%, then approve; otherwise reject".

That is a series of yes-or-no questions. It is also exactly what a **decision tree** does.

A decision tree is a flowchart that the computer learns from your data. At the top is the most useful yes-or-no question. Depending on the answer, it asks a follow-up question. Then another. Eventually it reaches an answer at the bottom of the tree.

It is like a game of 20 questions where the computer figured out the best questions to ask.

**When you actually use decision trees in real life.**

* When you need a model someone can read and understand. A decision tree is a flowchart. You can show it to your boss.
* When the relationships in your data are not smooth (steps and thresholds, not gradual slopes).
* As building blocks for more powerful models (we will get to those next).

A single decision tree by itself is rarely the best model in production. But trees are the secret ingredient in the most powerful classical ML techniques.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    Q1{"<b>Income > $50k?</b>"}
    Q1 -->|yes| Q2{"<b>Stable job?</b>"}
    Q1 -->|no| R1["<b>Reject</b>"]
    Q2 -->|yes| Q3{"<b>Debt < 35%?</b>"}
    Q2 -->|no| R2["<b>Reject</b>"]
    Q3 -->|yes| A1["<b>Approve</b>"]
    Q3 -->|no| R3["<b>Reject</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class Q1,Q2,Q3 gray
    class A1,R1,R2,R3 midgray
</div>

---

## Ensembles, the wisdom of crowds

Here is a fact that surprises people. If you ask one expert to estimate something tricky, they will be off by some amount. If you ask 100 amateurs and average their guesses, the average is often closer to the truth than the expert.

This is called the wisdom of crowds. And it applies to machine learning too.

A single decision tree is a bit of a know-it-all. It tends to overfit. But if you train 100 slightly different trees and let them vote, the result is dramatically better.

That is the idea behind **ensembles**. Combine many simple models, and the combination is smarter than any single one.

There are two main flavours of ensembles.

### Random Forests, the parallel committee

A **Random Forest** is just that. A forest of decision trees, each one trained on a slightly different slice of your data. To make a prediction, you ask every tree and take the majority vote.

Random Forest is one of the most reliable and useful algorithms in all of machine learning. It works on almost any problem with almost no tuning. It is often the second model people try (after a quick linear regression baseline) and very often the one they keep.

**When you actually use random forests in real life.**

* You want a strong model quickly with minimal tuning.
* You want a baseline before trying boosting.
* You want to know which features matter most. Random forests give you free feature importance scores.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    D["<b>Training data</b>"]
    D --> T1["<b>Tree 1</b>"]
    D --> T2["<b>Tree 2</b>"]
    D --> T3["<b>Tree 3</b>"]
    D --> TN["<b>Tree N</b>"]
    T1 --> V["<b>Majority Vote</b>"]
    T2 --> V
    T3 --> V
    TN --> V
    V --> P["<b>Final Prediction</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class T1,T2,T3,TN gray
    class D,V,P midgray
</div>

### Boosting, the relay race

A **Boosting** model is different in spirit. Instead of training many trees in parallel, you train them one at a time. Each new tree tries to fix the mistakes of the previous ones.

Think of it like a relay race where each runner picks up where the previous one left off. The first model gets some things right. The second model focuses on the things the first got wrong. The third focuses on what the first two missed together. After many rounds, the team performs incredibly well.

This idea is the basis of **AdaBoost**, **Gradient Boosting**, and the modern champions **XGBoost**, **LightGBM**, and **CatBoost**. These algorithms dominate most data science competitions and power countless real-world systems.

**When you actually use boosting in real life.**

* You want the absolute best accuracy you can get on tabular data.
* You have time to tune hyperparameters carefully.
* You are building a system where every percent of accuracy matters (fraud detection, ad ranking, credit scoring).

If you only ever learn one advanced technique, learn gradient boosting. It is the most powerful classical ML tool available today.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    D["<b>Data</b>"]
    D --> M1["<b>Model 1</b><br/>makes mistakes"]
    M1 -->|fix errors| M2["<b>Model 2</b><br/>fixes Model 1's<br/>mistakes"]
    M2 -->|fix errors| M3["<b>Model 3</b><br/>fixes what's left"]
    M3 -->|...| MN["<b>Model N</b>"]
    MN --> S["<b>Strong combined<br/>prediction</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class M1,M2,M3,MN gray
    class D,S midgray
</div>

Notice the difference. Random Forest trains all trees in parallel, voting. Boosting trains trees one at a time, each fixing the previous one's mistakes.

---

## Distance Metrics, the language of similarity

Now we shift from supervised learning to a different world.

Many machine learning problems are not about predicting things. They are about **comparing** things. "How similar are these two customers?" "Are these two documents about the same topic?" "Which existing product is this new product most like?"

To compare things, you need a way to measure similarity. That is what **distance metrics** are.

There are many ways to measure similarity, and they all sound technical, but the intuition is simple.

* **Euclidean distance** is just straight-line distance, the kind a ruler measures.
* **Manhattan distance** is taxi-cab distance, like walking on a city grid.
* **Cosine similarity** ignores size and only looks at direction. Two customers buy books and movies. Customer A bought 2 of each, Customer B bought 200 of each. By cosine, they are identical. They have the exact same taste, just different appetites.
* **Pearson correlation** asks whether two things move together. Stocks that rise and fall together have high correlation.
* **Jaccard** measures overlap between two sets. Two grocery lists with mostly the same items have high Jaccard.

Why does this matter? Because almost every unsupervised learning algorithm and many other tools depend on a choice of distance metric. Picking the wrong one can give you nonsense results.

**When you actually use distance metrics in real life.**

* Recommender systems use cosine similarity to find similar users or items.
* Search engines use distance between query vectors and document vectors.
* Document deduplication uses Jaccard on word sets.
* Financial analysis uses Pearson correlation between assets.

You will see distances everywhere once you start looking.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    Q["<b>How do you compare<br/>two items?</b>"]
    Q --> E["<b>Euclidean</b><br/>straight-line distance<br/>(ruler)"]
    Q --> C["<b>Cosine</b><br/>same direction<br/>ignore size"]
    Q --> PE["<b>Pearson</b><br/>do they move<br/>together?"]
    Q --> J["<b>Jaccard</b><br/>how much do their<br/>sets overlap?"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class E,C,PE,J gray
    class Q midgray
</div>

---

## K-Means Clustering, sorting things into piles without labels

Back to our bakery example. You have five years of daily records. No one ever told you what kinds of days exist. But you have a hunch that maybe there are a few natural types: busy weekend mornings, slow rainy weekdays, holiday rushes, normal quiet Tuesdays.

You want the computer to find these types automatically.

**K-Means** does exactly that.

You tell it "find me 4 groups". It looks at all your days, picks 4 starting points, and shuffles each day into the group whose center it is closest to. Then it recomputes the center of each group based on what is in it, and shuffles again. After a few rounds, the groups settle down, and you have 4 piles of similar days.

It is like sorting laundry. Throw it on the floor, group similar items together, look at the piles, adjust until each pile makes sense.

**When you actually use K-Means in real life.**

* Customer segmentation. "Find me natural groups of customers based on their behaviour."
* Image compression. Group similar pixel colors together.
* Document clustering. "Find me natural groups of articles based on their content."
* Anomaly detection. Anything that does not fit any group nicely is potentially suspicious.

K-Means is fast, simple, and works on huge datasets. But you have to tell it how many groups to look for, and it assumes the groups are roughly round blobs.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    D["<b>Pile of\nunlabelled data</b>"]
    D --> A["<b>Pick K starting<br/>centers (e.g. K=3)</b>"]
    A --> B["<b>Assign each point<br/>to nearest center</b>"]
    B --> C["<b>Move each center<br/>to mean of its points</b>"]
    C --> CH{"<b>Did anything<br/>change?</b>"}
    CH -->|yes| B
    CH -->|no| F["<b>K clean groups</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class B,C gray
    class D,A,CH,F midgray
</div>

---

## Hierarchical Clustering, the family tree of your data

K-Means gives you flat groups. Hierarchical clustering gives you a **tree**.

Imagine you ran a DNA analysis on every species on Earth. You would find that humans cluster tightly with chimps. Then humans and chimps together cluster with gorillas. Then primates as a whole cluster with other mammals. And so on, all the way up to the tree of life.

That nested tree is what hierarchical clustering produces. It does not ask "how many groups?" up front. It just builds the entire tree, from individual data points at the leaves up to one giant cluster at the root.

You then look at the tree and decide where to cut. Cut high to get a few big groups. Cut low to get many small groups. The choice is yours.

**When you actually use hierarchical clustering in real life.**

* When you want to **see the structure** of your data, not just get labels.
* When the groups are naturally nested (subspecies inside species inside genus).
* When you have small to medium datasets and want a beautiful visualisation called a **dendrogram**.
* In biology, gene analysis, document organization, anywhere relationships have natural depth.

It is slower than K-Means on large data, but the tree it produces is uniquely useful for exploration.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    ROOT["<b>All Animals</b>"]
    ROOT --> MAM["<b>Mammals</b>"]
    ROOT --> BIR["<b>Birds</b>"]
    MAM --> PRI["<b>Primates</b>"]
    MAM --> CAN["<b>Canines</b>"]
    PRI --> HUM["<b>Humans</b>"]
    PRI --> CHI["<b>Chimps</b>"]
    CAN --> DOG["<b>Dogs</b>"]
    CAN --> WOL["<b>Wolves</b>"]
    BIR --> EAG["<b>Eagles</b>"]
    BIR --> SPA["<b>Sparrows</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class HUM,CHI,DOG,WOL,EAG,SPA gray
    class ROOT,MAM,BIR,PRI,CAN midgray
</div>

This is exactly what hierarchical clustering builds, automatically, from your data. Cut the tree at any level to get the number of groups you want.

---

## K-Nearest Neighbours, the algorithm with no training

The last one on our tour is also the simplest. So simple that some people argue it does not really do "machine learning" at all.

**K-Nearest Neighbours**, almost always called **KNN**, works like this.

You want to predict something about a new data point. To do it, you look at the K most similar data points you have already seen, and you copy their answer.

That is the whole thing.

If those K neighbours all said "yes", your prediction is yes. If they all spent around 50 dollars, your prediction is 50 dollars. There is no fancy training, no model to build. The "model" is just the data.

It is exactly what a doctor does when they say "this patient looks a lot like three cases I have seen before, and all three turned out to be X."

**When you actually use KNN in real life.**

* As a quick, simple baseline. If your fancy model cannot beat KNN, something is wrong.
* Recommender systems. "Find me users who are most similar to this user, and recommend what they liked."
* Image recognition with small datasets.
* Anomaly detection. If a new point's nearest neighbours are very far away, it might be an outlier.

KNN is slow on huge datasets because every prediction has to compare against all the training data. But for small to medium problems, it is fast, simple, and often surprisingly good.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    N["<b>New data point</b><br/>(no label)"]
    N --> F["<b>Find the K nearest<br/>training points</b><br/>(e.g. K=5)"]
    F --> V["<b>They vote</b><br/>4 say YES, 1 says NO"]
    V --> P["<b>Prediction: YES</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class F,V gray
    class N,P midgray
</div>

---

## Putting it all together, when to use what

Here is the same tour as a cheat sheet you can come back to.

| Your problem | The tool |
|---|---|
| Predict a continuous number (price, demand, score) | Linear Regression |
| Predict yes or no | Logistic Regression |
| You have too many features and your model is overfitting | Regularization (Ridge, Lasso, Elastic Net) |
| You need a model someone can read and explain | Decision Tree |
| You want a strong, reliable model with little tuning | Random Forest |
| You want maximum accuracy on tabular data | Gradient Boosting (XGBoost, LightGBM, CatBoost) |
| You want to find hidden groups in unlabelled data, fast | K-Means Clustering |
| You want to see the full nested structure of your data | Hierarchical Clustering |
| You want a quick baseline based on similar past examples | K-Nearest Neighbours |
| You need to measure how similar two things are | Distance and Similarity Metrics |

That is the entire toolkit. Every technique you will meet in the rest of the handbook fits somewhere in this table.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    START{"<b>What is your<br/>problem?</b>"}
    START -->|"have labels"| SUP["<b>Supervised</b>"]
    START -->|"no labels"| UNS["<b>Unsupervised</b>"]

    SUP -->|"predict a<br/>number"| NUM{"<b>Regression</b>"}
    SUP -->|"predict yes/no<br/>or category"| CAT{"<b>Classification</b>"}

    NUM -->|"simple, fast"| LR["<b>Linear Regression</b>"]
    NUM -->|"complex patterns"| RF1["<b>Random Forest /<br/>Gradient Boosting</b>"]

    CAT -->|"yes / no"| LOG["<b>Logistic Regression</b>"]
    CAT -->|"need explainable"| DT["<b>Decision Tree</b>"]
    CAT -->|"max accuracy"| XGB["<b>XGBoost / LightGBM</b>"]
    CAT -->|"quick baseline"| KNN["<b>KNN</b>"]

    UNS -->|"find groups"| GRP{"<b>Clustering</b>"}
    UNS -->|"compare items"| DIST["<b>Distance Metrics</b>"]

    GRP -->|"fast, flat groups"| KM["<b>K-Means</b>"]
    GRP -->|"see full structure"| HC["<b>Hierarchical</b>"]

    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class LR,RF1,LOG,DT,XGB,KNN,KM,HC,DIST gray
    class START,SUP,UNS,NUM,CAT,GRP midgray
</div>

Use this flowchart as your decision tree (pun intended) when picking an algorithm for a new problem.

---

## A few honest truths before you go in

Before you dive into the detailed tutorials, here are a few honest things that nobody tells beginners.

**Most real ML work is not about the algorithm.** It is about getting the data right. Cleaning, fixing missing values, picking the right features, handling weird edge cases. The algorithm itself is usually a one-line call.

**There is no single best algorithm.** Random Forest is great. XGBoost is often better. Logistic regression sometimes beats both. It depends on the data. Always try a few and compare.

**Simple beats clever, most of the time.** A well-tuned linear or logistic regression often beats a poorly tuned neural network. Start simple, only go complex if simple is not enough.

**Tuning matters.** Every algorithm has knobs (hyperparameters). The defaults are reasonable but not optimal. Cross validation and grid search are how you find good settings.

**Measure on data you have not seen.** It is easy to fool yourself by looking at training scores. The only score that matters is the score on data the model has never seen.

If you remember nothing else, remember this. Machine learning is just a collection of clever ways to find patterns in data. Each technique on this page is just one such way, designed for one specific kind of problem. Once you know which problem you have, picking the technique is easy.

Welcome to machine learning. Now let us go learn the details.
