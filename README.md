# Chocolate Rating Predictor

* Authors:
    - Robin Dhillon
    - Lisha Gao
    - Markus Nam
    - Eyre Hong
    
# Introduction 

Have you ever wondered what makes chocolate taste good? Why do some people prefer dark chocolate and others like white chocolate? When you say you like certain kinds of chocolate, what are the factors that made you think so? Are there any ingredients in the chocolate that you want to avoid? To answer these questions, we decided to perform an analysis based on a dataset of 2,588 chocolate ratings compiled by Brady Brelinsk from the Manhattan Chocolate Society. The dataset is available to the public [here](http://flavorsofcacao.com/chocolate_database.html).

We want to create a model using different features provided related to the taste and flavors of the chocolate to predict the ratings. These features include `Manufacturer`, `Country of Bean Origin`, `Cocoa Percent`, and more. Through data wrangling and tuning machine learning models, our end goal is to optimize our machine learning model in order to give a relatively accurate prediction of the rating.

Since we have a predictive research question, we separate the dataset into train data and test data (75% and 25%, respectively) to avoid violation of the Golden Rule. Initial exploratory data analysis (EDA) will include investigating the data such as finding and replacing any missing values, and tables that summarize key info such as column datatypes and generate descriptive statistics will also be created. We need to make sure the number of missing values is within a reasonable range so that it will not affect the EDA. At this stage, we will only replace the missing values with NaN, and we may transform these data using `SimpleImputer` to replace them with the most frequent value or the mean based on the results of EDA. As a high level summary, we will also create a profile report that shows how the data columns are correlated, and these relationships will be explored visually via different plots such as bar charts and boxplots. As we delve deeper into the analysis, other plot types will most likely be used as well.

The data can also be preprocessed depending on the inferred important feature columns. For example, if we believe the `Ingredients` or `Most Memorable Characteristics` columns are indeed important for the model, we would need to split them by commas and possibly perform `OneHotEncoding` since these are categorical variables. We could use regression models for predictions such as `Decision Trees`, `SVM RBF`, `k-NN` (`k Nearest Neighbors`), and more. Note, however, that we will most likely use multiple models to explore which one model gives us the best results. These models will be fit to the training data and then evaluated by cross-validation. They will be further improved via hyperparameter optimization to obtain the best model, which will then be used for predictions on the test data. The hyperparameter optimization will be done via `GridSearchCV` or `RandomizedSearchCV`; depending on computation resources, `RandomizedSearchCV` would be more ideal. We will also check how our best model scores on the test data; it will be used to predict the chocolate rating of the test set and metrics such as the model accuracy will be obtained as well to gain an understanding of how our model will fare against deployment data. These results will ultimately be saved in a dataframe.

# Usage
goes here

# Dependencies
goes here
# License
The materials here for Chocolate Rating Predictor are licensed under the **Creative Commons Attribution 2.5 Canada License** ([CC BY 2.5 CA](https://creativecommons.org/licenses/by/2.5/ca/)). MIT License


# References

- Brady Brelinski and Andrea Brelinski. 2022. "chocolate_database" Flavor of Cacao, Mahanttan Chocolate Society http://flavorsofcacao.com

- Roger D. Peng and Elizabeth Matsui. 2017. "The Art of Data Science" https://bookdown.org/rdpeng/artofdatascience/ 