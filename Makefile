# Chocolate Rating Data Pipe
# Author: DSCI 522 Group 5
# Date: 2022-12-01
# Change log:
#     2022-12-05: Reduce number of options of model_summary.py

all: doc/chocolate_rating.html results/result_mape.csv results/svr_predict_vs_true.png results/ridge_predict_vs_true.png results/ridge_coefficients.csv results/characteristcs_bar.png results/company_boxplot.png

# download data
data/raw/chocolate_raw.csv: src/download_data.py
	python src/download_data.py --url=http://flavorsofcacao.com/database_w_REF.html --out_file=data/raw/chocolate_raw.csv

# preprocessing (e.g. data cleaning and data split into train and test)
data/processed/train.csv data/processed/test.csv: src/data_preprocessing.py data/raw/chocolate_raw.csv
	python src/data_preprocessing.py --in_file=data/raw/chocolate_raw.csv --out_dir=data/processed/

# exploratory data analysis
results/company_boxplot.png results/country_boxplot.png results/location_boxplot.png results/heatmap_cocoa.png results/characteristcs_bar.png results/ingredients_bar.png results/ratings_train.png results/characteristics.csv results/ingredients.csv: src/rating_eda.py data/processed/train.csv
	python src/rating_eda.py --in_file=data/processed/train.csv --out_dir=results/

# tune model baseline
results/model_baseline.sav: src/model_baseline.py data/processed/train.csv
	python src/model_baseline.py --in_file=data/processed/train.csv --out_dir=results/

# tune model SVR
results/model_svr.sav results/svr_predict_vs_true.png: src/model_svr.py data/processed/train.csv
	python src/model_svr.py --in_file=data/processed/train.csv --out_dir=results/

# tune model Ridge
results/model_ridge.sav results/ridge_predict_vs_true.png results/ridge_coefficients.csv: src/model_ridge.py data/processed/train.csv
	python src/model_ridge.py --in_file=data/processed/train.csv --out_dir=results/

# generate scores on test data
results/result_mape.csv: src/model_summary.py data/processed/test.csv results/model_baseline.sav results/model_svr.sav results/model_ridge.sav
	python src/model_summary.py --in_file=data/processed/test.csv --model_dir=results/ --out_dir=results/

# render report
doc/chocolate_rating.html: doc/chocolate_rating.Rmd doc/references.bib results/result_mape.csv results/ridge_coefficients.csv results/characteristcs_bar.png results/company_boxplot.png results/ridge_predict_vs_true.png results/svr_predict_vs_true.png
	Rscript -e "rmarkdown::render('doc/chocolate_rating.Rmd')"

clean:
	rm -rf data/raw/*
	rm -rf data/processed/*
	rm -rf results/*
	rm -rf doc/chocolate_rating.html
	rm -rf doc/chocolate_rating.md