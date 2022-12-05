# Author: DSCI_522_Group_5
# Date: 2022-11-25
# Change log:
#     2022-12-05: Add output file existence test

""" Exploratory data analysis on the chocolate database found here: http://flavorsofcacao.com/chocolate_database.html. The plotted figures are saved as well. 

Usage: rating_eda.py --in_file=<in_file> --out_dir=<out_dir>
 
Options:
--in_file=<in_file>       Path (including filename) to raw data (csv file)
--out_dir=<out_dir>       Path to folder where the processed data should be written
"""

import os
import numpy as np
import pandas as pd
import altair as alt
import vl_convert as vlc

# Handle large data sets without embedding them in the notebook
#alt.data_transformers.enable('data_server')
alt.data_transformers.disable_max_rows()
# Include an image for each plot since Gradescope only supports displaying plots as images
alt.renderers.enable('mimetype')

from docopt import docopt
from sklearn.model_selection import train_test_split

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

    try:
        os.makedirs(os.path.dirname(out_dir + '/'))  # for plot saving
    except:
        pass

    # Read training data 
    train_df = pd.read_csv(f"{in_file}")

    ratings_train = alt.Chart(train_df,
                              title = "Barplot of chocolate ratings for train data"
    ).mark_bar().encode(
        x=alt.X('Rating', title='Rating', bin = alt.BinParams(maxbins = 20)),
        y=alt.Y('count()')).properties(width=400, height=300)
    save_chart(ratings_train, out_dir + '/ratings_train.png')
    
    # Drop the rows with blank ingredients, remove the first 2 characters which are meaningless, split the comma delimited text
    boom_train_ingredients = train_df['Ingredients']
    boom_train_ingredients = boom_train_ingredients.dropna()
    boom_train_ingredients = boom_train_ingredients.str[2:].str.split(',').explode()
    boom_train_ingredients = boom_train_ingredients.str.strip()

    # Calculate the count and format into dataframe
    boom_train_ingredients_df = pd.DataFrame(boom_train_ingredients.value_counts())
    boom_train_ingredients_df = boom_train_ingredients_df.rename(columns={'Ingredients': 'Count'})
    boom_train_ingredients_df.sort_values('Count', ascending=False)
    boom_train_ingredients_df = boom_train_ingredients_df.reset_index()
    boom_train_ingredients_df.columns=['Ingredients', 'Count']

    # Create a new column for percentage
    boom_train_ingredients_df['Percent'] = round(boom_train_ingredients_df['Count'] / sum(boom_train_ingredients_df['Count']) * 100, 2)

    boom_train_ingredients_df.to_csv(out_dir + '/ingredients.csv', index=False)

    # B = Beans, S = Sugar, S* = Sweetener other than white cane or beet sugar, C = Cocoa Butter, V = Vanilla, L = Lecithin, Sa = Salt
    ingredients_bar = alt.Chart(boom_train_ingredients_df,
                                title = "Barplot of chocolate ingredients"
    ).mark_bar().encode(
        x=alt.X('Count', title='Count'),
        y=alt.Y('Ingredients', sort='x', title='Ingredients')
    ).properties(
        width=400,
        height=200
    )
    save_chart(ingredients_bar, out_dir + '/ingredients_bar.png')

    # Analyse Most_Memorable_Characteristics

    # Split the comma delimited text
    boom_train_characteristics = train_df['Most_Memorable_Characteristics'].str.split(',').explode()

    # Calculate the count and format into dataframe
    boom_train_characteristics_df = pd.DataFrame(boom_train_characteristics.value_counts())
    boom_train_characteristics_df = boom_train_characteristics_df.rename(columns={'Most_Memorable_Characteristics': 'Count'})
    boom_train_characteristics_df.sort_values('Count', ascending=False)
    boom_train_characteristics_df = boom_train_characteristics_df.reset_index()
    boom_train_characteristics_df.columns=['Characteristics', 'Count']

    # Create a new column for percentage
    boom_train_characteristics_df['Percent'] = round(boom_train_characteristics_df['Count'] / sum(boom_train_characteristics_df['Count']) * 100, 2)

    boom_train_characteristics_df.to_csv(out_dir + '/characteristics.csv', index=False)

    characteristics_bar = alt.Chart(boom_train_characteristics_df[:20],
                                    title = "Barplot of memorable characteristics"
    ).mark_bar().encode(
    x=alt.X('Count', title='Count'),
    y=alt.Y('Characteristics', sort='x', title='Memorable Characteristics')
    ).properties(
        width=400,
        height=300
    )
    save_chart(characteristics_bar, out_dir + '/characteristcs_bar.png')

    temp_df = train_df.copy()

    temp_df['Rating_c'] = pd.cut(
        x=temp_df['Rating'],
        bins=[0, 1.99, 2.99, 3.49, 3.99, 5],
        labels=['Unpleasant', 'Disappointing', 'Recommended', 'Highly Recommended', 'Outstanding']
    )

    temp_df['Cocoa_c'] = pd.cut(
        x=temp_df['Cocoa_Percent'],
        bins=[40, 49, 59, 69, 79, 89, 100],
        labels=['40-49%', '50-59%', '60-69%', '70-79%', '80-89%', '90-100%']
    )

    heatmap_cocoa = alt.Chart(temp_df,
                              title = "Heatmap of ratings categories and cocoa type"
    ).mark_square().encode(
        x=alt.X('Cocoa_c', title='Cocoa Category'),
        y=alt.Y('Rating_c', title='Rating Category', sort=['Unpleasant', 'Disappointing', 'Recommended', 'Highly Recommended', 'Outstanding']),
        size='count()',
        color='count()'
    ).properties(
        width=200,
        height=100
    )
    save_chart(heatmap_cocoa, out_dir + '/heatmap_cocoa.png')

    temp_df2 = train_df.copy()
    top10 = temp_df2['Company_Location'].value_counts()[:10].index
    temp_df2['Company_Location2'] = np.where(temp_df2['Company_Location'].isin(top10), temp_df2['Company_Location'], 'Others')

    temp_df2_sort = temp_df2.groupby(by = 'Company_Location2')['Rating'].agg('mean')
    temp_df2_sort = temp_df2_sort.sort_values().index
    temp_df2_sort = temp_df2_sort.tolist()

    boxp2 = alt.Chart(temp_df2).mark_boxplot().encode(
        x=alt.X('Rating', scale=alt.Scale(domain=(0.5, 4.5))),
        y=alt.Y('Company_Location2', sort=temp_df2_sort, title='Company Location')  # sort=alt.EncodingSortField(op="mean", order='ascending'), 
    )

    meanp2 = boxp2.mark_circle(color='red').encode(
        x = 'mean(Rating)'
    )

    location_boxplot = (boxp2 + meanp2).properties(title=alt.TitleParams('Boxplot of chocolate rating vs company locations',
                                                                          anchor = "middle")
)
    save_chart(location_boxplot, out_dir + '/location_boxplot.png')

    temp_df3 = train_df.copy()
    top10 = temp_df3['Country_of_Bean_Origin'].value_counts()[:10].index
    temp_df3['Country_of_Bean_Origin2'] = np.where(temp_df3['Country_of_Bean_Origin'].isin(top10), temp_df3['Country_of_Bean_Origin'], 'Others')

    temp_df3_sort = temp_df3.groupby(by = 'Country_of_Bean_Origin2')['Rating'].agg('mean')
    temp_df3_sort = temp_df3_sort.sort_values().index
    temp_df3_sort = temp_df3_sort.tolist()

    boxp3 = alt.Chart(temp_df3).mark_boxplot().encode(
        x=alt.X('Rating', scale=alt.Scale(domain=(0.5, 4.5))),
        y=alt.Y('Country_of_Bean_Origin2', sort=temp_df3_sort, title='Country of Bean Origin')
    )

    meanp3 = boxp3.mark_circle(color='red').encode(
        x = 'mean(Rating)'
    )

    country_boxplot = (boxp3 + meanp3).properties(title=alt.TitleParams('Boxplot of chocolate rating vs cocoa bean origin location',
                                                                          anchor = "middle")
)
    save_chart(country_boxplot, out_dir + '/country_boxplot.png')   

    temp_df4 = train_df.copy()
    temp_df4a = temp_df4.groupby(by = 'Company_(Manufacturer)')['REF'].agg('count')
    mask4 = temp_df4a[temp_df4a >= 10].index
    temp_df4 = temp_df4[temp_df4['Company_(Manufacturer)'].isin(mask4)]

    temp_df4_sort = temp_df4.groupby(by = 'Company_(Manufacturer)')['Rating'].agg('mean')
    temp_df4_sort = temp_df4_sort.sort_values().index
    temp_df4_sort = temp_df4_sort.tolist()

    boxp4 = alt.Chart(temp_df4).mark_boxplot().encode(
        x=alt.X('Rating', scale=alt.Scale(domain=(0.5, 4.5))),
        y=alt.Y('Company_(Manufacturer)', sort=temp_df4_sort, title='Company (Manufacturer)')
    )

    meanp4 = boxp4.mark_circle(color='red').encode(
        x = 'mean(Rating)'
    )

    company_boxplot = (boxp4 + meanp4).properties(title=alt.TitleParams('Boxplot of chocolate rating vs manufacturer',
                                                                          anchor = "middle")
)
    save_chart(company_boxplot, out_dir + '/company_boxplot.png') 

    # Verify the existence of the output file(s)
    assert os.path.isfile(out_dir + '/ratings_train.png'), f"{out_dir}/ratings_train.png not found. Please check." 
    assert os.path.isfile(out_dir + '/ingredients_bar.png'), f"{out_dir}/ingredients_bar.png not found. Please check." 
    assert os.path.isfile(out_dir + '/characteristcs_bar.png'), f"{out_dir}/characteristcs_bar.png not found. Please check." 
    assert os.path.isfile(out_dir + '/heatmap_cocoa.png'), f"{out_dir}/heatmap_cocoa.png not found. Please check." 
    assert os.path.isfile(out_dir + '/location_boxplot.png'), f"{out_dir}/location_boxplot.png not found. Please check." 
    assert os.path.isfile(out_dir + '/country_boxplot.png'), f"{out_dir}/country_boxplot.png not found. Please check." 
    assert os.path.isfile(out_dir + '/company_boxplot.png'), f"{out_dir}/company_boxplot.png not found. Please check." 
    assert os.path.isfile(out_dir + '/ingredients.csv'), f"{out_dir}/ingredients.csv not found. Please check." 
    assert os.path.isfile(out_dir + '/characteristics.csv'), f"{out_dir}/characteristics.csv not found. Please check." 

if __name__ == "__main__":
    main(opt["--in_file"], opt["--out_dir"])
