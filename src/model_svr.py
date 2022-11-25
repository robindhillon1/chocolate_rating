# Author: DSCI_522_Group_5
# Date: 2022-11-25

""" Use training data set to train SVR model and save the model to file for further processing

Usage: model_svc.py --in_file=<in_file> --out_dir=<out_dir>
 
Options:
--in_file=<in_file>       Path (including filename) to training data (csv file)
--out_dir=<out_dir>       Path to folder where the model should be written
"""

import os
import numpy as np
import pandas as pd
from docopt import docopt
from sklearn.model_selection import cross_validate
from sklearn.svm import SVR
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import loguniform, randint, uniform
import pickle
# from sklearn.linear_model import Ridge

opt = docopt(__doc__)

def main(in_file, out_dir):
    # Read data from training data (csv)
    train_df = pd.read_csv(in_file)
    
    # Split into X and y
    X_train, y_train = train_df.drop(columns=['Rating']), train_df['Rating']
    
    # Set scoring metrics
    scoring_metrics = 'neg_mean_absolute_percentage_error'
    
    # Classify features into different types
    numeric_features = ['Cocoa_Percent']
    categorical_features = ['Company_(Manufacturer)', 'Company_Location', 'Country_of_Bean_Origin']
    text_features = 'Most_Memorable_Characteristics'
    drop_features = ['REF', 'Review_Date', 'Specific_Bean_Origin_or_Bar_Name', 'Ingredients']

    # Create column transformer
    preprocessor = make_column_transformer(
        (StandardScaler(), numeric_features),
        (OneHotEncoder(handle_unknown='ignore'), categorical_features),
        (CountVectorizer(), text_features),
        ("drop", drop_features)
    )
    
    # Create pipeline
    svr_pipe = make_pipeline(preprocessor, SVR())
    
    # Prepare hyperparameter tuning param_dist
    preprocessor.fit(X_train, y_train)
    len_vocab = len(preprocessor.named_transformers_['countvectorizer'].get_feature_names_out())
    param_dist = {'columntransformer__countvectorizer__max_features': randint(100, len_vocab),
                  'svr__gamma' : loguniform(1e-5, 1e3),
                  'svr__C' : loguniform(1e-3, 1e3),
                  'svr__degree': randint(2, 5)          
    }
    
    # Hyperparameter tuning via RandomizedSearchCV
    print('Hyperparameter tuning in progress...')
    random_search = RandomizedSearchCV(
        svr_pipe,
        param_dist,
        n_jobs=-1,
        n_iter=50,
        scoring=scoring_metrics,
        random_state=522
    )
    random_search.fit(X_train, y_train)
    
    print(f'Best params: {random_search.best_params_}')
    print(f'Best score: {random_search.best_score_} ({scoring_metrics})')
    
    filename = 'model_svr.sav'

    try:
        # Write model to file
        pickle.dump(random_search, open(out_dir + '/' + filename, 'wb'))
    except:
        os.makedirs(os.path.dirname(out_dir + '/'))
        pickle.dump(random_search, open(out_dir + '/' + filename, 'wb'))

if __name__ == "__main__":
    main(opt["--in_file"], opt["--out_dir"])
