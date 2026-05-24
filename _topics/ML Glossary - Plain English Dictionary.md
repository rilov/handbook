---
title: "19. ML Glossary - Plain English Dictionary"
category: Machine Learning
order: 19
tags:
  - machine-learning
  - glossary
  - reference
  - dictionary
  - jargon
summary: An A-to-Z plain English dictionary of every machine learning term used in this handbook. No equations, no jargon defined with more jargon. Just clear short explanations for every concept you will meet.
---

# ML Glossary - Plain English Dictionary

If you have ever read a tutorial and stopped because of an unfamiliar word, this page is for you. Every term used in this handbook is defined below in plain English. Read top to bottom or jump to whichever word confused you.

---

## A

**Accuracy.** The fraction of predictions that were correct. Total right divided by total predictions. Easy to understand but misleading when classes are imbalanced.

**AdaBoost.** A boosting algorithm that trains models one at a time, with each new model focusing on the examples the previous ones got wrong.

**Adjusted R².** R² that has been penalized for adding extra features. Stops you from being fooled into thinking a more complex model is better.

**Algorithm.** A specific recipe for learning patterns from data. Linear regression, K-Means, and XGBoost are all algorithms.

**Anomaly.** A data point that does not fit the rest. Anomaly detection is the task of finding them.

**Area Under the Curve (AUC).** A number between 0 and 1 that summarizes how good a classifier is. Higher is better. Usually shorthand for ROC-AUC.

---

## B

**Bagging.** "Bootstrap Aggregating." Training many models on random samples of your data and averaging their predictions. Random Forest is the most famous example.

**Bias (statistical).** Systematic error. A model with high bias is too simple and consistently misses the real pattern.

**Bias (ethical / data).** Unfairness in the data or predictions that systematically disadvantages a group. Not the same as statistical bias.

**Bias-Variance Tradeoff.** The fact that making a model less wrong on average (lower bias) usually means making it more sensitive to individual examples (higher variance), and vice versa.

**Binary Classification.** Yes-or-no prediction. Spam or not. Fraud or not.

**Boosting.** Training models sequentially, where each new model focuses on the mistakes of the previous ones.

**Bootstrap.** Drawing samples from your dataset with replacement (so the same row can appear multiple times). Used inside bagging and Random Forest.

---

## C

**CatBoost.** A modern gradient boosting library that handles categorical features especially well.

**Categorical Variable.** A feature that takes on a fixed set of values like colors or countries, as opposed to numbers.

**Centroid.** The "center" of a cluster, computed as the mean of all points in that cluster. Used by K-Means.

**Classification.** Predicting which category something belongs to.

**Clustering.** Grouping data points so that similar ones end up together, without using labels.

**Confusion Matrix.** A 2x2 table showing true positives, false positives, true negatives, and false negatives. The source of most classification metrics.

**Correlation.** A measure between -1 and 1 of how strongly two variables move together.

**Cosine Similarity.** A measure of similarity that compares the direction of two vectors and ignores their magnitude. Great for text and high-dimensional data.

**Cross Validation (CV).** Splitting your data into K parts, training on K-1 and testing on the last, then rotating. A more reliable way to estimate model performance than a single train-test split.

**Curse of Dimensionality.** The phenomenon that things get weird in high dimensions. Distances become meaningless, and you need exponentially more data.

---

## D

**Data Leakage.** When information from the test set or the future accidentally sneaks into training, giving you unrealistically high scores that will not hold up in real use.

**DBSCAN.** A clustering algorithm that finds groups of arbitrary shape based on density. Labels outliers as noise.

**Decision Boundary.** The line (or surface) in feature space that separates one class from another.

**Decision Tree.** A flowchart of yes/no questions that ends in a prediction. Easy to read and the building block of Random Forests and Gradient Boosting.

**Deep Learning.** Machine learning using neural networks with many layers. A specific subset of ML.

**Dendrogram.** The tree diagram produced by hierarchical clustering. Shows how points and clusters merge.

**Dependent Variable.** Another name for the target or label. The thing you are trying to predict.

**Dimensionality Reduction.** Squeezing many features down into fewer features while keeping as much information as possible. PCA is the most common method.

---

## E

**Elastic Net.** A regularized linear model that combines Ridge and Lasso penalties.

**Elbow Method.** A way to pick the number of clusters K by looking at where the WCSS curve bends.

**Encoding.** Turning non-numeric data (like categories) into numbers so a model can use them. One-hot, ordinal, and target encoding are the common types.

**Ensemble.** A model made by combining many smaller models. Random Forest and Gradient Boosting are ensembles.

**Entropy.** A measure of disorder or impurity, used by decision trees to decide where to split.

**Epoch.** One full pass through the training data. Most relevant to neural networks, less so for classical ML.

**Estimator.** The scikit-learn name for any model. Anything with `.fit()` and `.predict()` methods.

**Euclidean Distance.** Straight-line distance between two points. What a ruler measures.

**Evaluation.** Measuring how good a model is using metrics on data it has not seen.

---

## F

**F1 Score.** The harmonic mean of precision and recall. A good single-number summary when classes are imbalanced.

**False Negative (FN).** Model predicted no, real answer was yes. The fraud you missed, the disease you failed to diagnose.

**False Positive (FP).** Model predicted yes, real answer was no. The legitimate email marked as spam.

**Feature.** A single input variable. Also called a predictor, attribute, or column.

**Feature Engineering.** Creating new useful features from your existing ones. Often more impactful than picking a fancy algorithm.

**Feature Importance.** A score for how much each feature contributed to predictions. Random Forests and Gradient Boosting give you this for free.

**Feature Scaling.** Adjusting features so they are on similar ranges. Essential for distance-based algorithms.

**Fitting.** Another word for training a model. The model "fits" its parameters to the data.

**Fold.** One of the K parts that data is split into for cross validation.

---

## G

**Generalization.** How well a model performs on new data it has not seen. The whole point of ML.

**Gini Impurity.** A measure of how mixed-up the classes are in a node of a decision tree.

**Gradient.** The direction of steepest increase of a function. In ML, we usually want to go in the opposite direction (gradient descent) to minimize error.

**Gradient Boosting.** A boosting method where each new model is trained to predict the residual errors of the previous ensemble.

**Gradient Descent.** An optimization method that takes small steps in the direction that reduces error the most.

**Grid Search.** Trying every combination of hyperparameters from a predefined list to find the best one.

---

## H

**Hamming Distance.** The number of positions where two equal-length strings or binary vectors differ.

**Hierarchical Clustering.** A clustering method that builds a tree of merges, from individual points up to one giant cluster.

**Hyperparameter.** A setting you choose before training, like the number of trees in a Random Forest or K in K-Means. Different from learned parameters.

**Hyperparameter Tuning.** Searching for the best hyperparameters using cross validation.

---

## I

**Imbalanced Data.** A dataset where one class is much more common than another (like 1% fraud, 99% normal). Standard accuracy is misleading on imbalanced data.

**Imputation.** Filling in missing values, usually with the mean, median, or a learned value.

**Independent Variable.** Another name for a feature. The input.

**Inertia.** Same as WCSS. The sum of squared distances within K-Means clusters.

**Information Gain.** How much a decision tree split reduces entropy. Higher is better.

**Instance.** A single row of data. Also called a sample, example, or observation.

---

## J

**Jaccard Similarity.** Size of the intersection divided by size of the union, used to compare sets.

---

## K

**K.** Just a number. Could mean number of clusters (K-Means), number of neighbours (KNN), or number of folds (K-fold CV).

**K-Fold Cross Validation.** Cross validation with K folds. K = 5 or 10 is most common.

**K-Means.** A clustering algorithm that partitions data into K groups by iteratively moving cluster centroids to the mean of their assigned points.

**K-Nearest Neighbours (KNN).** A classifier or regressor that predicts based on the K most similar training examples.

---

## L

**Label.** The answer for a given example. The thing you want to predict.

**Lasso Regression.** Linear regression with an L1 regularization penalty that drives weak coefficients exactly to zero.

**Lazy Learner.** A model that does no work at training time and all its work at prediction time. KNN is the classic example.

**Learning Rate.** A hyperparameter that controls how big a step the model takes at each training iteration. Mostly relevant to gradient boosting and neural networks.

**LightGBM.** A modern gradient boosting library known for speed on large datasets.

**Linear Regression.** Fitting a straight line (or hyperplane) through your data to predict a continuous value.

**Linkage.** In hierarchical clustering, the rule for measuring distance between two clusters. Single, complete, average, and Ward are the common types.

**Log Loss.** A metric that penalizes confident wrong predictions. Used when you need calibrated probabilities.

**Logistic Regression.** A classification model that outputs probabilities using the sigmoid function. Despite the name, it is used for classification, not regression.

**Loss Function.** A formula for how wrong a model is. Training minimizes the loss.

---

## M

**MAE (Mean Absolute Error).** The average size of errors, ignoring sign. Easy to explain.

**Manhattan Distance.** Distance measured along axes, like walking on a city grid. Also called L1.

**MAPE (Mean Absolute Percentage Error).** Error as a percentage. Useful for forecasting.

**Metric.** A number that measures how good predictions are. Accuracy, RMSE, F1, etc.

**Model.** The output of training. A function that takes features and predicts a target.

**MSE (Mean Squared Error).** Average of squared errors. Penalizes big errors more than small ones.

**Multicollinearity.** When two or more features are highly correlated with each other. Causes problems for linear models.

---

## N

**Neural Network.** A model made of layers of simple units (neurons) that pass signals to each other. The basis of deep learning.

**Noise.** Random variation in your data that does not come from the real pattern. Overfitting is learning the noise.

**Normalization.** Scaling features to a common range (usually 0 to 1). Sometimes used interchangeably with standardization.

---

## O

**Objective Function.** Same as loss function. The thing you are minimizing.

**One-Hot Encoding.** Turning one categorical column into multiple 0/1 columns, one for each category.

**Ordinal Encoding.** Mapping categories to integers when they have a natural order (small, medium, large).

**Out-of-Bag (OOB).** In bagging, the data points not used to train a particular tree. They can be used as a free validation set.

**Outlier.** A point that is far from the rest of the data. Can mess up distance-based algorithms.

**Overfitting.** When a model learns the training data so well, including its noise, that it performs poorly on new data.

---

## P

**P-Value.** A statistical measure of how surprising a result would be under the assumption of no real effect. Lower means more interesting. Used in classical statistics more than ML.

**Pearson Correlation.** A measure of linear association between two variables, from -1 to 1.

**Pipeline.** A chain of preprocessing steps and a model bundled into one object. Prevents data leakage.

**Polynomial Features.** Squared, cubed, and interaction terms added to features so linear models can fit curves.

**Precision.** Of the items you predicted positive, what fraction really were positive. High precision = few false alarms.

**Prediction.** The output of a trained model when given new features.

**Predictor.** Another name for a feature.

**Probability Calibration.** Adjusting a model's probability outputs so that "70% confidence" actually means "right 70% of the time."

---

## Q

**Quantile.** A cut point that divides a dataset into equal parts. The median is the 50% quantile.

---

## R

**R² (R-squared).** The fraction of variance in the target that your model explains. 1.0 is perfect, 0 is useless, negative is worse than guessing the mean.

**Random Forest.** An ensemble of many decision trees, each trained on a random subset of data and features, that vote on the answer.

**Recall.** Of the actually positive items, what fraction did you catch. High recall = few missed cases.

**Regression.** Predicting a continuous number.

**Regularization.** Penalty added to a model's loss to discourage complexity and prevent overfitting.

**Reinforcement Learning.** Learning by trial and error, with rewards for good actions and punishments for bad ones.

**Residual.** The difference between the actual and predicted value. What gradient boosting tries to fix.

**Ridge Regression.** Linear regression with an L2 regularization penalty that shrinks all coefficients gently.

**RMSE (Root Mean Squared Error).** The square root of MSE. Has the same units as the target. The most common regression metric.

**ROC Curve.** A plot of true positive rate vs false positive rate at different classification thresholds.

**ROC-AUC.** Area under the ROC curve. A threshold-independent measure of classifier quality.

---

## S

**Sample.** A single row of data. Also called an instance or example.

**Scaling.** See feature scaling.

**Scikit-learn.** The most popular classical ML library in Python.

**Sensitivity.** Same as recall.

**Sigmoid.** The S-shaped curve that maps any real number into the range 0 to 1. Used by logistic regression.

**Silhouette Score.** A clustering quality metric ranging from -1 to 1. Higher means better separation.

**Specificity.** Of the actually negative items, what fraction did you correctly label negative.

**Standardization.** Scaling each feature to have mean 0 and standard deviation 1. Done by StandardScaler.

**Stratified Sampling.** Sampling that preserves class proportions. Important for splitting imbalanced data.

**Supervised Learning.** Learning from labelled examples. Regression and classification.

**SVM (Support Vector Machine).** A classifier that finds the widest margin between classes.

---

## T

**Target.** The thing you want to predict. Same as label.

**Target Encoding.** Replacing a category with the mean target value of that category. Powerful but risky for leakage.

**Test Set.** The portion of data held back and used only for final evaluation. Never touched during training.

**Threshold.** The cutoff for converting a probability into a yes/no decision. Default is 0.5.

**Training.** Showing a model your data so it can learn the patterns. Also called fitting.

**Training Set.** The portion of data used to teach the model.

**True Negative (TN).** Model said no, real answer was no.

**True Positive (TP).** Model said yes, real answer was yes.

---

## U

**Underfitting.** When a model is too simple to capture the patterns in the data. Bad on both training and test.

**Unsupervised Learning.** Learning patterns from data without labels.

---

## V

**Validation Set.** A portion of data used for tuning hyperparameters during training, kept separate from both the training set and the final test set.

**Variance (statistical).** How much predictions change as the training data changes. High variance models overfit.

**VIF (Variance Inflation Factor).** A diagnostic for detecting multicollinearity. VIF above 5 or 10 is a warning.

---

## W

**Ward Linkage.** A hierarchical clustering linkage method that merges the pair of clusters causing the smallest increase in within-cluster variance.

**WCSS (Within-Cluster Sum of Squares).** Sum of squared distances from each point to its cluster's centroid. K-Means minimizes this.

**Weights.** The numerical parameters a model learns during training. In linear models, the coefficients.

---

## X

**X.** The standard symbol for the feature matrix. Each row is a sample, each column is a feature.

**XGBoost.** "Extreme Gradient Boosting." A highly optimized gradient boosting library, famous for winning competitions.

---

## Y

**y.** The standard symbol for the target vector. The thing you are trying to predict.

---

## Z

**Zero-Shot.** Making predictions on classes the model never saw during training. More relevant to deep learning than classical ML.

---

## A closing tip

If you keep meeting a word that is not in this glossary, please open an issue or just search. ML has thousands of terms but only a few dozen really matter. The ones in this glossary cover 95% of what you will need to read any classical ML tutorial.
