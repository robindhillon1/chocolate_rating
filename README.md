# Chocolate Rating Predictor

* Authors:
    - Robin Dhillon
    - Lisha Gao
    - Markus Nam
    - Eyre Hong
    

The goal of our analysis is to predict the rating of chocolate depending on specific features such as the `Cocoa Percent`, the `Company Location`, `Country of Bean Origin`, and more. Since we have a predictive research question, we separate the dataset into train data and test data (75% and 25%, respectively) to avoid violation of the Golden Rule. Initial exploratory data analysis (EDA) will include investigating the data such as finding and replacing any missing values, and tables that summarize key info such as column datatypes and generate descriptive statistics will also be created. As a high level summary, we will also create a profile report that shows how the data columns are correlated, and these relationships will be explored visually via different plots such as bar charts and boxplots. As we delve deeper into the analysis, other plot types will most likely be used as well.

The data can also be preprocessed depending on the inferred important feature columns. For example, if we believe the `Ingredients` or `Most Memorable Characteristics` columns are indeed important for the model, we'd need to split them by commas and possibly perform `OneHotEncoding` since these are categorical variables. We could use regression models for predictions such as `Decision Trees`, `SVM RBF`, `k-NN` (`k Nearest Neighbors`), and more. Note, however, that we will most likely use multiple models to explore which one model gives us the best results. These models will be fit to the training data and then evaluated by cross-validation. They will be further improved via hyperparameter optimization to obtain the best model, which will then be used for predictions on the test data. The hyperparameter optimization will be done via `GridSearchCV` or `RandomizedSearchCV`; depending on computation resources, `RandomizedSearchCV` would be more ideal. We will also check how our best model scores on the test data; it will be used to predict the chocolate rating of the test set and metrics such as the model accuracy will be obtained as well to gain an understanding of how our model will fare against deployment data. These results will ultimately be saved in a dataframe.

# License  **CHECK THIS. DELETE ONCE FINAL**
The materials here for Chocolate Rating Predictor are licensed under the **Creative Commons Attribution 2.5 Canada License** ([CC BY 2.5 CA](https://creativecommons.org/licenses/by/2.5/ca/)). 

# References  **CHECK THIS. DELETE ONCE FINAL**

Brelinski, Brady. "Flavors of Cacao - Chocolate Database", Retrieved November 16, 2022 from http://flavorsofcacao.com/chocolate_database.html. 

