---
title: "29. ML Common Pitfalls and Debugging Guide"
category: Machine Learning
order: 29
tags:
  - machine-learning
  - debugging
  - pitfalls
  - troubleshooting
  - common-mistakes
summary: A symptom to cause to fix troubleshooting guide for the most common machine learning problems. When your model behaves weirdly, look up the symptom here and find out what is going wrong.
---

# ML Common Pitfalls and Debugging Guide

Every ML practitioner hits the same walls. This page is a symptom → cause → fix guide for the most common situations. If your model is misbehaving, find the symptom that matches yours and follow the fix.

---

## Symptom: Great training accuracy, poor test accuracy

**Diagnosis:** Classic **overfitting**. Your model memorized the training data including the noise, so it cannot generalize to new data.

**Common causes:**

* Model is too complex for the amount of data you have.
* You have too many features compared to rows.
* Your decision tree is too deep.
* You forgot to use regularization.
* You evaluated on training data by mistake.

**Fixes:**

1. Add **regularization** (Ridge, Lasso, `alpha` parameter, or for tree models, set `max_depth`, `min_samples_leaf`, increase `min_samples_split`).
2. Get **more data** if you can.
3. **Reduce features** with selection or PCA.
4. Use **cross validation** to confirm the problem is real, not just an unlucky split.
5. For neural nets, add **dropout** or **early stopping**.

---

## Symptom: Poor training accuracy AND poor test accuracy

**Diagnosis:** **Underfitting**. Your model is too simple or you are not giving it enough signal.

**Common causes:**

* Linear model on highly nonlinear data.
* `max_depth` too small in a tree.
* Too few features.
* Features are not on the same scale (for distance-based or regularized models).

**Fixes:**

1. Use a **more flexible model** (decision tree, random forest, gradient boosting).
2. **Add polynomial or interaction features**.
3. **Engineer better features** from your raw data.
4. **Reduce regularization** (lower `alpha`, higher `C` for logistic regression).
5. Make sure your **features are properly scaled**.

---

## Symptom: Model predicts the same class for everything

**Diagnosis:** Almost always **imbalanced classes**. The cheapest way to maximize accuracy is to always guess the majority class.

**Common causes:**

* 99% of your training labels are one class.
* You evaluated with accuracy on imbalanced data, so the issue is hidden.
* You did not balance, weight, or stratify.

**Fixes:**

1. **Stop using accuracy.** Use **F1**, **precision/recall**, or **ROC-AUC** instead.
2. Use `class_weight="balanced"` in scikit-learn models.
3. **Oversample the minority class** (SMOTE) or **undersample the majority class**.
4. Adjust the **decision threshold** (default 0.5 might not be right).
5. Use **stratified sampling** when splitting and cross-validating.

---

## Symptom: Test accuracy looks suspiciously high (99%+ on a hard problem)

**Diagnosis:** Almost always **data leakage**. Information from the test set or the future is sneaking into training.

**Common causes:**

* You **scaled the data before splitting** (the scaler saw the test set).
* You used the **target** as a feature, directly or indirectly.
* Your features include information that would not be available at prediction time (target leakage).
* You **upsampled or transformed** the data before splitting.
* Duplicate rows between train and test.

**Fixes:**

1. Always **split first**, then fit transformers only on training data.
2. Use **scikit-learn Pipelines** to prevent leakage automatically.
3. **Examine each feature** and ask: would I have this at the moment of prediction?
4. Look for **time-related features** that encode the future.
5. **Drop duplicates** before splitting.

---

## Symptom: KNN or K-Means gives weird results

**Diagnosis:** You probably **forgot to scale your features**. Distance-based algorithms are dominated by whichever feature has the biggest numeric range.

**Fixes:**

1. **Always StandardScaler** before KNN, K-Means, SVM, or any regularized linear model.
2. Use a **Pipeline** so you cannot forget.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", KMeans(n_clusters=4, n_init=10)),
])
```

---

## Symptom: Model performance is unstable, big swings between runs

**Diagnosis:** Either the **random seed** is varying, or you have **too little data**.

**Fixes:**

1. **Set random_state** on every component (split, model, cv).
2. Use **cross validation** (5 or 10 folds) and report the mean.
3. Get more data.
4. Try simpler models (they have less variance).

---

## Symptom: GridSearchCV is taking forever

**Diagnosis:** Combinatorial explosion. With many parameters and many values, the number of combinations explodes.

**Fixes:**

1. Use **RandomizedSearchCV** instead. Sample 50 random combinations rather than testing all 10,000.
2. Set `n_jobs=-1` to use all CPU cores.
3. **Narrow the grid** based on intuition. Tune one parameter at a time first.
4. Use fewer **cv folds** (3 instead of 10) for an initial pass, then refine.
5. For boosting, tune `n_estimators` with **early stopping** instead of grid search.

---

## Symptom: Coefficient signs flip when I add a feature

**Diagnosis:** **Multicollinearity**. Two of your features are correlated and the model cannot decide which one should get the credit.

**Fixes:**

1. Check **correlation matrix** and **VIF** (Variance Inflation Factor).
2. **Drop one** of the correlated features.
3. Use **Ridge regression** which handles multicollinearity gracefully.
4. **PCA** to combine correlated features into uncorrelated components.

---

## Symptom: My model says 99% accuracy but business says it is useless

**Diagnosis:** You optimized the **wrong metric**. Accuracy can be high while the model fails at the actual business problem.

**Fixes:**

1. **Understand the cost of errors.** Is a false positive more expensive than a false negative? Adjust your metric accordingly.
2. **Talk to stakeholders** about what mistakes hurt and which do not.
3. Use **precision** if false positives are costly, **recall** if false negatives are.
4. Look at the **confusion matrix** directly to see what kinds of mistakes the model makes.
5. Build a **custom scoring function** if no off-the-shelf metric fits.

---

## Symptom: Model worked in development, broken in production

**Diagnosis:** **Distribution shift**. The real-world data looks different from your training data.

**Common causes:**

* Customer behaviour changed (seasonal, post-COVID, etc.).
* Data pipeline changed (new columns, different formats).
* Feature engineering at predict time differs from training time.
* Time of day, region, or device mix changed.

**Fixes:**

1. **Monitor input distributions** in production. If they drift, retrain.
2. **Retrain regularly** on fresh data.
3. **Save the entire pipeline**, not just the model, so preprocessing matches.
4. **Set up A/B testing** or shadow deployment before full rollout.

---

## Symptom: Probabilities look weird (every prediction is 0.01 or 0.99)

**Diagnosis:** **Uncalibrated probabilities**. Some models (especially Random Forest and Gradient Boosting) output uncalibrated scores that do not correspond to true probabilities.

**Fixes:**

1. Use **CalibratedClassifierCV** to fix the probabilities.
2. Look at a **calibration curve** to confirm.
3. If you just need rankings, calibration is not necessary.

---

## Symptom: My loss is NaN or Inf

**Diagnosis:** Numerical issues. Most likely you have NaN values in your data, an extreme outlier, or a divide-by-zero in your code.

**Fixes:**

1. **Check for missing values** with `df.isnull().sum()`.
2. **Look for outliers** with `df.describe()`. Cap them if extreme.
3. **Scale features** so no value is astronomical.
4. For linear regression, look for **perfectly correlated features** (will cause singular matrices).

---

## Symptom: Models that should be similar give wildly different results

**Diagnosis:** Either **hyperparameters** are very different, or one model is misconfigured.

**Fixes:**

1. **Print the hyperparameters** of each model. They might have very different defaults.
2. Make sure both are evaluated on the **same train/test split**.
3. Make sure both use the **same preprocessing**.
4. Use the same **random_state** everywhere.

---

## Symptom: My elbow plot does not have a clear elbow

**Diagnosis:** Your data may not have natural clusters. Or it might have just one cluster, or many overlapping ones.

**Fixes:**

1. Try the **silhouette score** as a second opinion.
2. Plot the data in 2D with PCA or t-SNE to see if there is actually any structure.
3. Try **DBSCAN** which can find clusters of arbitrary shape.
4. Consider that maybe clustering is not the right approach for your data.

---

## Symptom: scikit-learn shows a warning about convergence

**Diagnosis:** The optimizer ran out of iterations before finding the best parameters.

**Fixes:**

1. **Increase `max_iter`** (default is 100 for logistic regression, often too low).
2. **Scale your features** so the optimization is well-conditioned.
3. **Reduce regularization** (`alpha` smaller, `C` larger) if it is too tight.

---

## Symptom: My features have hundreds of categories, model crashes

**Diagnosis:** **High cardinality categorical features**. One-hot encoding creates hundreds of columns.

**Fixes:**

1. Use **target encoding** or **frequency encoding** instead of one-hot.
2. **Group rare categories** into "Other".
3. Use **CatBoost** which handles high cardinality natively.
4. Encode as **embeddings** if using deep learning.

---

## Symptom: Time series cross validation is wrong

**Diagnosis:** Standard CV shuffles the data, which leaks the future into training.

**Fixes:**

1. Use **TimeSeriesSplit** from scikit-learn instead.
2. Never train on data from after the test period.
3. Always evaluate on a future hold-out, not random.

---

## A general checklist when nothing makes sense

When you are stuck and your model behaves bizarrely, run through this list:

1. **Did I look at the data?** Run `df.describe()` and `df.head()`. Plot histograms.
2. **Did I check for missing values?** `df.isnull().sum()`.
3. **Did I check class balance?** `df["target"].value_counts()`.
4. **Did I scale the features?** Required for distance-based and regularized models.
5. **Did I split before transforming?** Always split first.
6. **Did I use a Pipeline?** Pipelines prevent half the bugs in ML.
7. **Did I check the test set is held out?** Never seen during any tuning.
8. **Am I using the right metric?** Accuracy on imbalanced data lies.
9. **Did I set random_state?** For reproducible results.
10. **Did I try the simplest model first?** Linear/logistic regression is your sanity check.

If you go through this checklist and still cannot find the bug, write down what you tried and ask someone with fresh eyes. Half the time the issue is something you have looked at five times already and your brain skipped over it.

---

## A few timeless rules

* **Garbage in, garbage out.** No algorithm fixes bad data.
* **Simple beats clever.** Try the simplest model first. If it works, ship it.
* **Test data is sacred.** Do not look at it. Do not tune to it. Use it once, at the end.
* **A model is just an opinion.** It can be confidently wrong. Always check.
* **The hardest problems are not algorithm choice, they are data quality.** Spend 80% of your time on the data.

That is the entire debugging mindset condensed. Bookmark this page. You will need it.
