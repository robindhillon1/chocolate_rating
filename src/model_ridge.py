# Author: DSCI_522_Group_5
# Date: 2022-11-25

""" Use training data set to train Ridge model and save the model to file for further processing

Usage: model_ridge.py --in_file=<in_file> --out_dir=<out_dir>
 
Options:
--in_file=<in_file>       Path (including filename) to training data (csv file)
--out_dir=<out_dir>       Path to folder where the model should be written
"""

import os
import numpy as np
import pandas as pd
from docopt import docopt
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_validate
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import loguniform, randint, uniform
import pickle
import altair as alt
import vl_convert as vlc

# Handle large data sets without embedding them in the notebook
alt.data_transformers.disable_max_rows()
# Include an image for each plot since Gradescope only supports displaying plots as images
alt.renderers.enable('mimetype')

opt = docopt(__doc__)

def save_chart(chart, filename, scale_factor=1):
    '''
    Save an Altair chart using vl-convert
    
    Parameters
    ----------
    chart : altair.Chart
        Altair chart to save
    filename : str
        The path to save the chart to
    scale_factor: int or float
        The factor to scale the image resolution by.
        E.g. A value of `2` means two times the default resolution.
    '''
    if filename.split('.')[-1] == 'svg':
        with open(filename, "w") as f:
            f.write(vlc.vegalite_to_svg(chart.to_dict()))
    elif filename.split('.')[-1] == 'png':
        with open(filename, "wb") as f:
            f.write(vlc.vegalite_to_png(chart.to_dict(), scale=scale_factor))
    else:
        raise ValueError("Only svg and png formats are supported")

        
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
    ridge_pipe = make_pipeline(preprocessor, Ridge())
    
    # Prepare hyperparameter tuning param_dist
    preprocessor.fit(X_train, y_train)
    len_vocab = len(preprocessor.named_transformers_['countvectorizer'].get_feature_names_out())
    param_dist = {'columntransformer__countvectorizer__max_features': randint(100, len_vocab),
                  'ridge__alpha': [0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10, 100]          
    }
    
    # Hyperparameter tuning via RandomizedSearchCV
    print('Hyperparameter tuning in progress...')
    random_search = RandomizedSearchCV(
        ridge_pipe,
        param_dist,
        n_jobs=-1,
        n_iter=50,
        scoring=scoring_metrics,
        random_state=522
    )
    random_search.fit(X_train, y_train)
    
    print(f'Best params: {random_search.best_params_}')
    print(f'Best score: {random_search.best_score_} ({scoring_metrics})')

    
    # Get feature names
    feature_names = numeric_features + (
        random_search.best_estimator_.named_steps['columntransformer']
            .named_transformers_['onehotencoder']
            .get_feature_names_out()
            .tolist()) + (
        random_search.best_estimator_.named_steps['columntransformer']
            .named_transformers_['countvectorizer']
            .get_feature_names_out()
            .tolist())
    
    # Extract top n positive and top n negative features
    n_top_bottom = 10
    coef_df = pd.DataFrame(data={"features": feature_names, "coefficients": random_search.best_estimator_.named_steps['ridge'].coef_})
    coef_df = coef_df.sort_values('coefficients', ascending=False)
    coef_df = pd.concat([coef_df.head(n_top_bottom), coef_df.tail(n_top_bottom)])
    

    # Prepare for predict_vs_true plot
    y_predict = random_search.predict(X_train)  
    plot_df = pd.DataFrame([y_train, y_predict]).T
    plot_df.columns = ['True', 'Predict']
    
    # Dummy dataframe for plotting a diagonal line
    dummy_df = pd.DataFrame({'True': [0, 5], 'Predict': [0, 5]})
    
    # Our plot
    predict_vs_true = alt.Chart(plot_df, title = "Predict vs True (Ridge)").mark_point().encode(
        x=alt.X('True'),
        y=alt.Y('Predict')
    ).properties(
        width=400,
        height=400
    )
    
    # The diagonal line
    diagonal = alt.Chart(dummy_df).mark_line(color='red').encode(
        x='True',
        y='Predict'
    )

    filename = 'model_ridge.sav'

    try:
        # Write model to file
        pickle.dump(random_search, open(out_dir + '/' + filename, 'wb'))
        save_chart(predict_vs_true + diagonal, out_dir + '/ridge_predict_vs_true.png')
        coef_df.to_csv(out_dir + '/ridge_coefficients.csv', index=False)  # output should have two columns: Features, Coefficients
    except:
        os.makedirs(os.path.dirname(out_dir + '/'))
        pickle.dump(random_search, open(out_dir + '/' + filename, 'wb'))
        save_chart(predict_vs_true + diagonal, out_dir + '/ridge_predict_vs_true.png')
        coef_df.to_csv(out_dir + '/ridge_coefficients.csv', index=False)  # output should have two columns: Features, Coefficients

if __name__ == "__main__":
    main(opt["--in_file"], opt["--out_dir"])
