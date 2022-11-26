# Author: DSCI_522_Group_5
# Date: 2022-11-25


"""Get all models' results for a test data set
Usage: model_summary.py --in_file=<in_file> --model_dir=<model_dir> --dummy=<dummy> --svr=<svr> --ridge==<ridge> --out_dir=<out_dir>
 
Options:
--in_file=<in_file>       Mandatory option argument. Path of input data file.
--model_dir=<model_dir>   Mandatory option argument. Path of model directory.
--dummy=<dummy>           Mandatory option argument. Filename of dummy model.
--svr=<svr>               Mandatory option argument. Filename of SVR model.
--ridge=<ridge>           Mandatory option argument. Filename of Ridge model.
--out_dir=<out_dir>       Mandatory option argument. Path of output directory.
"""

import os
import pandas as pd
import numpy as np
from docopt import docopt

from sklearn.metrics import mean_absolute_percentage_error
import pickle

opt = docopt(__doc__)

def main(in_file, model_dir, dummy, svr, ridge, out_dir):
    
    # Read test data
    test_df = pd.read_csv(in_file)
    
    # Split into X and y
    X_test, y_test = test_df.drop(columns=['Rating']), test_df['Rating']
    
    # Read every sav model
    dummy_model = pickle.load(open(model_dir + '/' + dummy, 'rb'))
    svr_model = pickle.load(open(model_dir + '/' + svr, 'rb'))
    ridge_model = pickle.load(open(model_dir + '/' + ridge, 'rb'))
    
    # Get y predict for every model
    y_pred_dummy = dummy_model.predict(X_test)
    y_pred_svr = svr_model.predict(X_test)
    y_pred_ridge = ridge_model.predict(X_test)
    
    # Model MAPE score
    mape_dummy = mean_absolute_percentage_error(y_test, y_pred_dummy)
    mape_svr = mean_absolute_percentage_error(y_test, y_pred_svr)
    mape_ridge = mean_absolute_percentage_error(y_test, y_pred_ridge)

    # Create result dictionary
    result_dict = {'Model': ['DummyRegressor', 'SVR', 'Ridge'],
                   'MAPE Score': [mape_dummy, mape_svr, mape_ridge]}
    
    #Transfer into DataFrame
    result_df = pd.DataFrame(result_dict)  

    
    try:
        result_df.to_csv(out_dir + '/result_mape.csv', index=False)
    except:
        os.makedirs(os.path.dirname(out_dir + '/'))
        result_df.to_csv(out_dir + '/result_mape.csv', index=False)


if __name__ == "__main__":
    main(opt["--in_file"], opt["--model_dir"], opt["--dummy"], opt["--svr"], opt["--ridge"], opt["--out_dir"])