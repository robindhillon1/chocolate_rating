# Author: DSCI_522_Group_5
# Date: 2022-11-25

""" Use training data set to get the baseline DummyRegressor model and save the model to file for further processing

Usage: model_baseline.py --in_file=<in_file> --out_dir=<out_dir>
 
Options:
--in_file=<in_file>       Path (including filename) to training data (csv file)
--out_dir=<out_dir>       Path to folder where the model should be written
"""

import os
import numpy as np
import pandas as pd
from docopt import docopt
from sklearn.model_selection import cross_validate
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import loguniform, randint, uniform
import pickle

opt = docopt(__doc__)

def main(in_file, out_dir):
    # Read data from training data (csv)
    train_df = pd.read_csv(in_file)
    
    # Split into X and y
    X_train, y_train = train_df.drop(columns=['Rating']), train_df['Rating']
    
    # Set scoring metrics
    scoring_metrics = 'neg_mean_absolute_percentage_error'
    
    # Create DummyRegressor model
    dr = DummyRegressor()
    
    # Fit the model
    dr.fit(X_train, y_train)
    
    # Get the predict Value
    dr_y_predit = dr.predict(X_test)
    
    # Get the MAPE test score
    dr_mape = mean_absolute_percentage_error(y_test, dr_y_predit)
    
    print(f'Dummy score: {dr_mape} ({scoring_metrics})')
    
    filename = 'model_baseline.sav'

    try:
        # Write model to file
        pickle.dump(dr, open(out_dir + '/' + filename, 'wb'))
    except:
        os.makedirs(os.path.dirname(out_dir + '/'))
        pickle.dump(dr, open(out_dir + '/' + filename, 'wb'))

if __name__ == "__main__":
    main(opt["--in_file"], opt["--out_dir"])
