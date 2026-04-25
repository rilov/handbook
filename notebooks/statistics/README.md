# Statistics Tutorial Notebooks

Practical Jupyter notebooks with real datasets for learning statistics concepts.

## 📚 Available Notebooks

### 1. Chapter 1: Exploratory Data Analysis (EDA)
**File:** `chapter1_eda_examples.ipynb`

**Dataset:** Iris Dataset (150 flower samples, 4 features, 3 species)

**What You'll Learn:**
- Loading and inspecting data
- Summary statistics (mean, median, std, etc.)
- Data visualization (histograms, box plots, scatter plots)
- Correlation analysis
- Finding patterns and outliers
- Multivariate analysis with pair plots

**Key Visualizations:**
- Distribution histograms
- Box plots for outlier detection
- Correlation heatmaps
- Scatter plots by species
- Pair plots showing all relationships

---

### 2. Chapter 2: Inferential Statistics
**File:** `chapter2_inferential_statistics_examples.ipynb`

**Dataset:** Penguins Dataset (333 Antarctic penguins with measurements)

**What You'll Learn:**
- Population vs sample concepts
- Central Limit Theorem in action
- Confidence intervals (95%, different sample sizes)
- Standard error and margin of error
- Making inferences about populations
- Comparing groups (Adelie vs Gentoo penguins)

**Key Visualizations:**
- Population vs sample distributions
- Central Limit Theorem demonstration
- Confidence interval ranges
- Effect of sample size on precision
- Species comparison plots

---

### 3. Chapter 3: Hypothesis Testing
**File:** `chapter3_hypothesis_testing_examples.ipynb`

**Dataset:** Tips Dataset (244 restaurant bills with tips, demographics, and timing)

**What You'll Learn:**
- The 5-step hypothesis testing process
- Formulating null and alternative hypotheses
- Calculating p-values
- Making statistical decisions
- Interpreting results

**Tests Covered:**
- **One-Sample t-Test**: Is the average tip $3.00?
- **Two-Sample t-Test**: Do smokers tip differently than non-smokers?
- **Proportion Test**: Do more than 50% of customers dine on weekends?

**Key Visualizations:**
- Distribution comparisons
- Box plot comparisons
- p-value visualization
- Critical regions diagram

---

## 🚀 Getting Started

### Prerequisites

Install required Python packages:

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn statsmodels jupyter
```

### Running the Notebooks

1. **Navigate to the notebooks directory:**
   ```bash
   cd /Users/rishan/handbook/notebooks/statistics
   ```

2. **Start Jupyter:**
   ```bash
   jupyter notebook
   ```

3. **Open a notebook** and run cells sequentially (Shift + Enter)

### Alternative: VS Code

1. Open the notebook in VS Code
2. Select Python kernel
3. Run cells with the play button or Shift + Enter

---

## 📊 Datasets Used

### Iris Dataset
- **Source:** UCI Machine Learning Repository (built into scikit-learn)
- **Size:** 150 samples
- **Features:** 
  - Sepal length (cm)
  - Sepal width (cm)
  - Petal length (cm)
  - Petal width (cm)
- **Target:** Species (Setosa, Versicolor, Virginica)
- **Use Case:** Classification, EDA, visualization

### Tips Dataset
- **Source:** Seaborn built-in dataset (waiter's records)
- **Size:** 244 samples
- **Features:**
  - Total bill ($)
  - Tip ($)
  - Sex (Male/Female)
  - Smoker (Yes/No)
  - Day (Thu/Fri/Sat/Sun)
  - Time (Lunch/Dinner)
  - Party size
- **Use Case:** Hypothesis testing, regression, group comparisons

---

## 🎯 Learning Path

**Recommended Order:**

1. **Start with Chapter 1 (EDA)**
   - Learn to explore and visualize data
   - Understand distributions and patterns
   - Build intuition about your data

2. **Move to Chapter 3 (Hypothesis Testing)**
   - Apply the 5-step process
   - Test claims about data
   - Make data-driven decisions

3. **Practice with your own data!**
   - Find datasets on [Kaggle](https://www.kaggle.com/datasets)
   - Apply the techniques you learned
   - Build your portfolio

---

## 💡 Tips for Success

### While Working Through Notebooks:

1. **Run cells in order** - Each cell may depend on previous ones
2. **Read the explanations** - Don't just run code, understand why
3. **Modify and experiment** - Change parameters, try different visualizations
4. **Take notes** - Document your insights and questions

### Common Issues:

**Problem:** "ModuleNotFoundError"
- **Solution:** Install missing package: `pip install <package-name>`

**Problem:** Plots not showing
- **Solution:** Add `%matplotlib inline` at the top of the notebook

**Problem:** Kernel died/crashed
- **Solution:** Restart kernel and run all cells again

---

## 📖 Additional Resources

### Online Datasets:
- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [UCI ML Repository](https://archive.ics.uci.edu/ml/index.php)
- [Data.gov](https://data.gov/)
- [Google Dataset Search](https://datasetsearch.research.google.com/)

### Documentation:
- [Pandas](https://pandas.pydata.org/docs/)
- [NumPy](https://numpy.org/doc/)
- [Matplotlib](https://matplotlib.org/stable/contents.html)
- [Seaborn](https://seaborn.pydata.org/)
- [SciPy Stats](https://docs.scipy.org/doc/scipy/reference/stats.html)

### Tutorials:
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)
- [Real Python Statistics](https://realpython.com/python-statistics/)

---

## 🤝 Contributing

Found an issue or want to add more examples?

1. Create a new notebook following the same structure
2. Use real, publicly available datasets
3. Include clear explanations and visualizations
4. Add it to this README

---

## 📝 Notes

- All datasets are publicly available and free to use
- Notebooks are designed for beginners but include advanced concepts
- Code is well-commented for learning purposes
- Visualizations use colorblind-friendly palettes

---

## ✅ Checklist

Before running notebooks, make sure you have:

- [ ] Python 3.7+ installed
- [ ] Jupyter Notebook or JupyterLab installed
- [ ] All required packages installed
- [ ] Basic understanding of Python
- [ ] Read the corresponding chapter in the handbook

---

## 🎓 What's Next?

After completing these notebooks:

1. **Chapter 4.1-4.3:** Specific hypothesis testing methods
2. **Machine Learning:** Apply statistics to build models
3. **Real Projects:** Use these skills on actual problems

Happy Learning! 📊🚀
