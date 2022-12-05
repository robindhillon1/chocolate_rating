# Author: DSCI_522_Group_5
# Date: 2022-11-21
# Change log:
#     2022-11-24: Add skiprows=[0]
#     2022-12-05: Add output file existence test

""" Preprocess chocolate data (from http://flavorsofcacao.com/chocolate_database.html). Write the training data and test data to separate files.

Usage: data_preprocessing.py --in_file=<in_file> --out_dir=<out_dir>
 
Options:
--in_file=<in_file>       Path (including filename) to raw data (csv file)
--out_dir=<out_dir>       Path to folder where the processed data should be written
"""

import os
import numpy as np
import pandas as pd
from docopt import docopt
from sklearn.model_selection import train_test_split

opt = docopt(__doc__)

def main(in_file, out_dir):
    # Read from raw data file downloaded from the source URL, and convert space in column names into underscore
    df = pd.read_csv(in_file, skiprows=[0], names=['REF', 'Company_(Manufacturer)', 'Company_Location', 'Review_Date', 'Country_of_Bean_Origin', 'Specific_Bean_Origin_or_Bar_Name', 'Cocoa_Percent', 'Ingredients', 'Most_Memorable_Characteristics', 'Rating'])
    
    # Split data into train_df and test_df
    train_df, test_df = train_test_split(df, test_size=0.25, random_state=522)
          
    # Remove '%' from the Cocoa_Percent feature
    train_df['Cocoa_Percent'] = train_df['Cocoa_Percent'].str.rstrip('%')
    test_df['Cocoa_Percent'] = test_df['Cocoa_Percent'].str.rstrip('%')

    # Replace missing value with np.nan
    train_df['Ingredients'] = train_df['Ingredients'].replace('', np.nan)
    test_df['Ingredients'] = test_df['Ingredients'].replace('', np.nan)

    try:
        train_df.to_csv(out_dir + '/train.csv', index=False)
        test_df.to_csv(out_dir + '/test.csv', index=False)
    except:
        os.makedirs(os.path.dirname(out_dir + '/'))
        train_df.to_csv(out_dir + '/train.csv', index=False)
        test_df.to_csv(out_dir + '/test.csv', index=False)

    # Verify the existence of the output file(s)
    assert os.path.isfile(out_dir + '/train.csv'), f"{out_dir}/train.csv not found. Please check." 
    assert os.path.isfile(out_dir + '/test.csv'), f"{out_dir}/test.csv not found. Please check." 
        
if __name__ == "__main__":
    main(opt["--in_file"], opt["--out_dir"])
