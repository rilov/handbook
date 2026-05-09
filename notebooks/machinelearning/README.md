# Machine Learning Notebooks

Welcome to the Machine Learning tutorial notebooks! 🚀

## 📚 Notebooks

### 1. Simple Linear Regression (`01_simple_linear_regression.ipynb`)
**Difficulty:** Beginner  
**Topics Covered:**
- Creating and visualizing data
- Training a simple linear regression model
- Understanding slope and intercept
- Making predictions
- Evaluating model performance (R², MSE, MAE)
- Visualizing the regression line

**What You'll Learn:**
- How to predict house prices from size
- How to interpret model coefficients
- How to evaluate if your model is good

---

### 2. Multiple Linear Regression (`02_multiple_linear_regression.ipynb`)
**Difficulty:** Beginner-Intermediate  
**Topics Covered:**
- Working with multiple features
- Feature correlation analysis
- Interpreting coefficients for each feature
- Making predictions with multiple inputs
- Feature importance visualization

**What You'll Learn:**
- How to use multiple features (size, bedrooms, age, location)
- How each feature affects the price
- How to identify the most important features

---

### 3. Advanced Linear Regression (`03_advanced_linear_regression.ipynb`)
**Difficulty:** Intermediate-Advanced  
**Topics Covered:**
- Checking all 5 assumptions of linear regression
- Feature scaling (StandardScaler, MinMaxScaler)
- Regularization techniques (Ridge, Lasso, Elastic Net)
- Handling multicollinearity
- Model comparison

**What You'll Learn:**
- How to check if your model is valid
- When and how to scale features
- How to prevent overfitting
- How to choose the best model

---

### 4. Logistic Regression (`04_logistic_regression.ipynb`)
**Difficulty:** Beginner-Intermediate  
**Topics Covered:**
- The sigmoid function visualization
- Binary classification (Pass/Fail prediction)
- Decision boundaries
- Confusion matrix
- ROC curve and AUC
- Custom thresholds

**What You'll Learn:**
- How to do classification with logistic regression
- How to interpret probabilities
- All evaluation metrics for classification
- How to tune the decision threshold

---

### 5. Regularization Deep Dive (`05_regularization.ipynb`)
**Difficulty:** Intermediate-Advanced  
**Topics Covered:**
- Why we need regularization (overfitting demo)
- Ridge (L2) regression
- Lasso (L1) regression - feature selection
- Elastic Net - combining both
- Hyperparameter tuning with cross-validation
- Comparing all methods

**What You'll Learn:**
- How regularization prevents overfitting
- The difference between L1 and L2
- How Lasso automatically selects features
- How to auto-tune hyperparameters

---

## 📊 Data Files

### `data/house_prices.csv`
Sample house price dataset with the following features:
- **size**: House size in square feet (1000-4000)
- **bedrooms**: Number of bedrooms (1-5)
- **age**: Age of house in years (0-50)
- **location**: Location score from 1-10
- **price**: House price in thousands of dollars

**Download:** You can download this file and use it in the notebooks!

---

## 🚀 Getting Started

### Prerequisites
Install required libraries:
```bash
pip install numpy pandas matplotlib seaborn scikit-learn scipy statsmodels
```

### Running the Notebooks
1. Start Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
2. Navigate to the `notebooks/machinelearning/` folder
3. Open any notebook (`.ipynb` file)
4. Run cells sequentially (Shift + Enter)

### Recommended Order
1. Start with `01_simple_linear_regression.ipynb`
2. Move to `02_multiple_linear_regression.ipynb`
3. Finish with `03_advanced_linear_regression.ipynb`

---

## 💡 Tips

### For Beginners:
- Run each cell one at a time
- Read the explanations carefully
- Try modifying the code to see what happens
- Don't worry if you don't understand everything at first!

### For Intermediate Learners:
- Try changing the data
- Experiment with different parameters
- Add your own visualizations
- Try the exercises at the end of each notebook

### For Advanced Learners:
- Use your own datasets
- Implement additional regularization techniques
- Add cross-validation
- Try polynomial features

---

## 📖 Additional Resources

### Tutorials
- [Linear Regression - Introduction](../../topics/linear-regression-introduction)
- [Linear Regression - Advanced Topics](../../topics/linear-regression-advanced-topics)

### Documentation
- [Scikit-learn Linear Models](https://scikit-learn.org/stable/modules/linear_model.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)

---

## 🎯 Learning Objectives

After completing these notebooks, you will be able to:
- ✅ Build and train linear regression models
- ✅ Interpret model coefficients and predictions
- ✅ Check if model assumptions are met
- ✅ Scale features appropriately
- ✅ Apply regularization to prevent overfitting
- ✅ Compare different models and choose the best
- ✅ Visualize results effectively

---

## 🤝 Contributing

Found a bug or have a suggestion? Feel free to:
- Open an issue
- Submit a pull request
- Suggest improvements

---

## 📝 License

These notebooks are provided for educational purposes.

---

**Happy Learning! 🎓**

For questions or feedback, please refer to the main handbook documentation.
