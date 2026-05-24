# Machine Learning Notebooks - Hands-on Practice

Practice notebooks for every major ML topic in the handbook. Each notebook is **self-contained** — load the data, train, evaluate, and try the exercises at the end.

## How to run

### Option 1: Google Colab (recommended, zero setup)

1. Go to [colab.research.google.com](https://colab.research.google.com).
2. **File → Upload notebook**.
3. Pick the `.ipynb` file from this folder.
4. Run all cells (Runtime → Run all).

All datasets load automatically (sklearn, seaborn, or public URLs). No Kaggle login needed for any notebook.

### Option 2: Run locally

```bash
pip install numpy pandas scikit-learn matplotlib seaborn scipy xgboost lightgbm jupyter
jupyter notebook
```

Then open any `.ipynb` file.

## Notebook list

| # | Notebook | Topic | Dataset |
|---|---------|-------|---------|
| 01 | `01_linear_regression.ipynb` | Predict house prices, simple and multiple linear regression | California Housing (sklearn) |
| 02 | `02_logistic_regression.ipynb` | Binary classification, sigmoid, ROC, confusion matrix | Titanic (seaborn) |
| 03 | `03_regularization.ipynb` | Ridge, Lasso, Elastic Net, coefficient shrinkage paths | California Housing |
| 04 | `04_decision_trees.ipynb` | Train, visualize, and overfit a decision tree | Iris (sklearn) |
| 05 | `05_random_forest.ipynb` | Bagging vs single tree, feature importance | Breast Cancer (sklearn) |
| 06 | `06_gradient_boosting_xgboost.ipynb` | Boosting and XGBoost, GridSearchCV tuning | Titanic |
| 07 | `07_distance_metrics.ipynb` | Euclidean, Manhattan, Cosine, Pearson, Jaccard | Iris + synthetic sets |
| 08 | `08_kmeans_clustering.ipynb` | K-Means, elbow method, silhouette | Synthetic blobs + Mall Customers |
| 09 | `09_hierarchical_clustering.ipynb` | Dendrograms, linkage methods, ARI | Iris |
| 10 | `10_knn.ipynb` | KNN classification with and without scaling | Iris + Wine |
| 11 | `11_end_to_end_titanic.ipynb` | **Capstone:** complete pipeline from CSV to evaluation | Titanic |

## Suggested learning order

1. Start with **01 - Linear Regression** to learn the core ML workflow.
2. Move to **02 - Logistic Regression** for your first classifier.
3. Try **03 - Regularization** to understand overfitting fixes.
4. Do **04 - Decision Trees** to see a different model family.
5. Then **05 - Random Forest** and **06 - Gradient Boosting** for ensembles.
6. Switch to unsupervised: **07 - Distance Metrics**, **08 - K-Means**, **09 - Hierarchical**.
7. Round it out with **10 - KNN**.
8. Finish with **11 - End-to-End Titanic** which ties everything together.

## Common Kaggle datasets to try after these

Once you finish these notebooks, swap in a real Kaggle dataset and rerun your pipeline:

| Project type | Kaggle dataset |
|---|---|
| Tabular regression | [House Prices: Advanced Regression Techniques](https://www.kaggle.com/c/house-prices-advanced-regression-techniques) |
| Tabular classification | [Titanic - Machine Learning from Disaster](https://www.kaggle.com/c/titanic) |
| Customer segmentation | [Customer Segmentation - Mall Customers](https://www.kaggle.com/datasets/vjchoudhary7/customer-segmentation-tutorial-in-python) |
| Image classification | [Digit Recognizer (MNIST)](https://www.kaggle.com/c/digit-recognizer) |
| Text / NLP | [SMS Spam Collection](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset) |
| Fraud detection (imbalanced) | [Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) |

### Loading Kaggle datasets in Colab

```python
# In Colab cell:
from google.colab import files
files.upload()  # upload kaggle.json
!mkdir -p ~/.kaggle && mv kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json
!pip install -q kaggle
!kaggle datasets download -d <dataset-slug>
!unzip -q <file>.zip
```

## Tips for getting the most out of these

1. **Run every cell**, do not just read. The code is the learning.
2. **Try the exercises** at the end of each notebook. They build real intuition.
3. **Modify hyperparameters** and see what changes. Get a feel for the knobs.
4. **Compare to the corresponding tutorial** in the handbook for the deeper explanation.
5. **Save your modified notebooks** to your own GitHub or Google Drive.

## Rebuilding the notebooks

If you ever want to regenerate or modify them, edit `_build_notebooks.py` and run:

```bash
python _build_notebooks.py
```

That will overwrite all 11 notebooks with the latest version.

---

Happy learning! 🚀
