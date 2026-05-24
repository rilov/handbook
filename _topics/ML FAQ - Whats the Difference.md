---
title: "21. ML FAQ - What is the Difference Between..."
category: Machine Learning
order: 21
tags:
  - machine-learning
  - faq
  - comparison
  - differences
  - beginners
summary: A frequently asked questions page answering every common 'what's the difference between X and Y' question in machine learning. Quick, clear, side-by-side comparisons of the concepts that confuse beginners most.
---

# ML FAQ - What is the Difference Between...

Most confusion in machine learning is not about a single concept being hard. It is about two concepts that sound similar and you cannot tell apart. This page tackles every "what is the difference between X and Y" question that beginners actually ask.

---

## Supervised vs Unsupervised Learning

| | Supervised | Unsupervised |
|---|---|---|
| **You have** | Features + labels | Just features |
| **Goal** | Predict the label for new data | Find structure in the data |
| **Examples** | Spam filter, house prices | Customer segments, anomaly detection |
| **Algorithms** | Linear/Logistic Reg, Trees, Forests, Boosting, KNN | K-Means, Hierarchical, DBSCAN |

**One-line answer.** Supervised learns from answers, unsupervised has no answers.

---

## Regression vs Classification

Both are supervised learning, but the output is different.

| | Regression | Classification |
|---|---|---|
| **Output** | A continuous number | A category |
| **Example** | "What price will this house sell for?" | "Will this customer churn?" |
| **Metrics** | RMSE, MAE, R² | Accuracy, F1, ROC-AUC |
| **Common models** | Linear, Ridge, Random Forest Regressor | Logistic, Random Forest Classifier |

**One-line answer.** Regression predicts numbers, classification predicts labels.

---

## Linear Regression vs Logistic Regression

The names are confusingly similar.

| | Linear Regression | Logistic Regression |
|---|---|---|
| **Output** | Any real number | A probability (0 to 1) |
| **Used for** | Regression | Classification (despite the name) |
| **Curve** | Straight line | S-shaped sigmoid |
| **Example use** | Predict salary from years of experience | Predict if loan will default |

**One-line answer.** Linear regression draws a line, logistic regression squashes that line through a sigmoid to give probabilities.

---

## Ridge vs Lasso vs Elastic Net

All three are linear regression with regularization. The difference is what kind.

| | Ridge | Lasso | Elastic Net |
|---|---|---|---|
| **Penalty type** | L2 (squared coefficients) | L1 (absolute coefficients) | Both L1 and L2 |
| **What it does to weak features** | Shrinks them gently toward zero | Drives them exactly to zero | Mix of both |
| **Feature selection?** | No | Yes (automatic) | Partial |
| **Multicollinearity?** | Handles well | Picks one of correlated features | Balanced |
| **Use when** | All features matter a bit | Want a sparse model | You are not sure |

**One-line answer.** Ridge keeps everything, Lasso drops weak features, Elastic Net does both.

---

## Bagging vs Boosting

The two main ways to build an ensemble of models.

| | Bagging | Boosting |
|---|---|---|
| **How** | Train many models in parallel on random subsets | Train models sequentially, each fixing the previous one |
| **Goal** | Reduce variance | Reduce bias |
| **Famous example** | Random Forest | Gradient Boosting, XGBoost |
| **Parallel training?** | Yes | No, must be sequential |
| **Overfits easily?** | No, robust | Yes if not regularized |
| **Speed to train** | Fast (parallel) | Slow (sequential) |

**One-line answer.** Bagging is a parallel committee that votes. Boosting is a relay race where each runner fixes the previous one's mistakes.

---

## Random Forest vs Gradient Boosting

The two go-to ensemble methods.

| | Random Forest | Gradient Boosting |
|---|---|---|
| **Strategy** | Bagging | Boosting |
| **Trees built** | In parallel | Sequentially |
| **Tuning effort** | Low | High |
| **Default accuracy** | Strong | Often higher with tuning |
| **Overfits?** | Rarely | Yes, easily |
| **Best for** | Reliable baseline | Maximum accuracy on tabular data |

**One-line answer.** Random Forest is the reliable workhorse, Gradient Boosting (XGBoost/LightGBM) is the competition winner.

---

## Decision Tree vs Random Forest

| | Decision Tree | Random Forest |
|---|---|---|
| **Number of trees** | One | Many (usually 100-500) |
| **Interpretability** | Easy to read as flowchart | Hard to read directly |
| **Overfits?** | Yes, easily | No, much more robust |
| **Accuracy** | Lower | Higher |
| **Use when** | You need to explain decisions | You need accuracy |

**One-line answer.** A Random Forest is just many decision trees voting together.

---

## K-Means vs Hierarchical Clustering

| | K-Means | Hierarchical |
|---|---|---|
| **Need to pick K up front?** | Yes | No |
| **Output** | Flat groups | Tree of merges (dendrogram) |
| **Speed** | Fast on big data | Slow on big data |
| **Shape of clusters** | Spherical | Arbitrary |
| **Best for** | Quickly finding K groups | Exploring data structure |

**One-line answer.** K-Means gives you flat groups, Hierarchical gives you a tree you can cut at any level.

---

## Clustering vs Classification

Easy to confuse since both produce groups.

| | Clustering | Classification |
|---|---|---|
| **Type** | Unsupervised | Supervised |
| **Labels needed?** | No | Yes |
| **Output groups** | Discovered from data | Predefined by you |
| **Example** | "Find natural customer types" | "Is this customer high-value: yes/no?" |

**One-line answer.** Classification predicts a known category, clustering discovers unknown categories.

---

## Accuracy vs Precision vs Recall vs F1

The four metrics every beginner mixes up.

| | What it measures | Use when |
|---|---|---|
| **Accuracy** | Fraction of predictions correct | Classes are balanced |
| **Precision** | Of predicted positives, how many are real | False alarms are costly (spam, fraud) |
| **Recall** | Of real positives, how many you caught | Missed cases are costly (disease, security) |
| **F1** | Balance of precision and recall | Imbalanced classes, need single number |

**One-line answer.** Accuracy is overall correctness. Precision is "how trustworthy is a positive prediction." Recall is "how complete is the model at finding positives." F1 balances precision and recall.

---

## RMSE vs MAE vs R²

The three main regression metrics.

| | What it tells you | Range | Pros | Cons |
|---|---|---|---|---|
| **MAE** | Average size of error | 0 to ∞ | Easy to explain | Doesn't punish big errors |
| **RMSE** | Like MAE but punishes large errors | 0 to ∞ | Most common reporting metric | Sensitive to outliers |
| **R²** | Fraction of variance explained | -∞ to 1 | Easy to compare models | Not in original units |

**One-line answer.** RMSE and MAE measure how big errors are. R² measures how much of the variance you explained.

---

## ROC-AUC vs PR-AUC

Both are areas under curves used for classification.

| | ROC-AUC | PR-AUC |
|---|---|---|
| **Curve** | True Positive Rate vs False Positive Rate | Precision vs Recall |
| **Good for** | Balanced data | Imbalanced data |
| **Insensitive to** | Class imbalance | Class imbalance (good!) |

**One-line answer.** On imbalanced data, prefer PR-AUC. On balanced data, ROC-AUC is fine.

---

## Training Set vs Validation Set vs Test Set

| | Training | Validation | Test |
|---|---|---|---|
| **Used for** | Fitting the model | Tuning hyperparameters | Final honest evaluation |
| **Size** | ~70% | ~15% | ~15% |
| **Model sees it during fitting?** | Yes | For tuning only | Never |

**One-line answer.** Train teaches the model. Validation picks the best version. Test gives the honest final score.

---

## Overfitting vs Underfitting

| | Underfitting | Overfitting |
|---|---|---|
| **Model is** | Too simple | Too complex |
| **Training score** | Bad | Great |
| **Test score** | Bad | Bad |
| **Fix** | Bigger model, more features, less regularization | Smaller model, more data, more regularization |

**One-line answer.** Underfit: too simple, fails on everything. Overfit: too complex, memorized noise.

---

## Bias vs Variance

The two ways a model can be wrong.

| | Bias | Variance |
|---|---|---|
| **Cause** | Model is too simple | Model is too sensitive |
| **Effect** | Consistently wrong in the same way | Wildly different on different data |
| **Sign** | Underfitting | Overfitting |
| **Reduce by** | More complex model, more features | More data, regularization, ensembling |

**One-line answer.** High bias = always wrong the same way. High variance = answers swing wildly.

---

## L1 vs L2 Regularization

| | L1 (Lasso) | L2 (Ridge) |
|---|---|---|
| **Penalty formula** | Sum of absolute coefficients | Sum of squared coefficients |
| **Effect** | Pushes weak coefs to exactly zero | Shrinks all coefs toward zero |
| **Feature selection** | Yes | No |
| **Stability** | Less stable (picks one of correlated features) | More stable |

**One-line answer.** L1 cuts features off, L2 just turns them down.

---

## Euclidean vs Cosine Distance

| | Euclidean | Cosine |
|---|---|---|
| **Measures** | Straight-line distance | Angle between vectors |
| **Sensitive to magnitude?** | Yes | No |
| **Good for** | Continuous numeric features | Text, sparse high-dimensional data |
| **Range** | 0 to ∞ | -1 to 1 (similarity) |

**One-line answer.** Euclidean cares about size, cosine cares about direction.

---

## Standardization vs Normalization

These words get used loosely. Strict definitions:

| | Standardization | Normalization (Min-Max) |
|---|---|---|
| **Transforms to** | Mean 0, std 1 | Range 0 to 1 |
| **Sensitive to outliers?** | Less | More |
| **Common name** | StandardScaler | MinMaxScaler |
| **Best for** | Most ML models | Neural nets, image data |

**One-line answer.** Standardization centers and scales by std. Normalization squeezes into a 0-1 range.

---

## One-Hot vs Ordinal vs Target Encoding

The three ways to handle categorical features.

| | One-Hot | Ordinal | Target |
|---|---|---|---|
| **What it does** | One 0/1 column per category | Each category → integer | Each category → mean target |
| **When to use** | No order between categories | Categories have order | High cardinality |
| **Risk** | Many extra columns | Implies false ordering | Data leakage if done wrong |

**One-line answer.** One-hot for unordered, ordinal for ordered, target for high-cardinality.

---

## Train Test Split vs Cross Validation

| | Train/Test Split | Cross Validation |
|---|---|---|
| **What** | Split once into train and test | Repeat split K times, average |
| **Speed** | Fast | K times slower |
| **Reliability** | Less reliable | More reliable |
| **Use for** | Final test set | Hyperparameter tuning |

**One-line answer.** Cross validation is just multiple train/test splits averaged together for stability.

---

## Hyperparameter vs Parameter

| | Parameter | Hyperparameter |
|---|---|---|
| **Set by** | The training process | You, before training |
| **Examples** | Slope of regression line, weights | `max_depth`, `n_estimators`, `learning_rate` |
| **Tuned via** | The data | Grid search, manual tuning |

**One-line answer.** Parameters are learned, hyperparameters are chosen.

---

## scikit-learn vs XGBoost vs LightGBM

| | scikit-learn | XGBoost | LightGBM |
|---|---|---|---|
| **Strength** | All-around classical ML | Boosting, top accuracy | Fast boosting on huge data |
| **Speed** | Moderate | Fast | Fastest |
| **Best for** | Learning, prototyping | Competitions, production | Large datasets |

**One-line answer.** scikit-learn for everything, XGBoost/LightGBM when you need top-tier boosting.

---

## Model vs Algorithm vs Estimator

These are used interchangeably but have subtle differences.

* **Algorithm.** A general recipe (e.g. "Linear Regression").
* **Model.** A specific trained instance with learned parameters.
* **Estimator.** scikit-learn's name for anything with `.fit()` and `.predict()` methods.

**One-line answer.** Algorithm is the recipe, model is the trained dish, estimator is the scikit-learn term.

---

## Final tip

If your question is "what's the difference between X and Y" and it is not here, the answer is usually:

1. They are different in **what they predict** (regression vs classification),
2. Or different in **how they predict it** (one algorithm vs another),
3. Or different in **what they measure** (one metric vs another).

Once you classify the question into one of those three, the actual difference is almost always one or two sentences.
