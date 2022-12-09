FROM continuumio/miniconda3
RUN conda update -n base -c conda-forge -y conda
RUN apt-get update
RUN apt-get install -y libfontconfig1-dev
RUN conda install -c conda-forge -y r-base
RUN conda install -c conda-forge -y altair
RUN conda install -c conda-forge -y scikit-learn>=1.1.3
RUN conda install -c conda-forge -y lxml
RUN conda install -c conda-forge -y pandoc
RUN pip install joblib --quiet
RUN pip install mglearn --quiet
RUN pip install psutil --quiet
RUN pip install docopt-ng --quiet
RUN pip install vl-convert-python --quiet
RUN Rscript -e "install.packages(c('knitr', 'kableExtra', 'tidyverse', 'caret', 'xfun'), repos='https://cran.rstudio.com/')"
