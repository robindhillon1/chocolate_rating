# Author: MDS Cohort7 522 Group 5
FROM continuumio/miniconda3

RUN apt-get update
RUN apt-get -y --no-install-recommends install
RUN apt-get install -y r-base r-base-dev
RUN apt-get install -y libfontconfig1-dev
RUN apt-get install -y libcurl4-openssl-dev
RUN apt-get install -y libssl-dev
RUN apt-get install -y libxml2-dev

RUN Rscript -e "install.packages(c('knitr', 'kableExtra', 'tidyverse', 'caret', 'xfun'), repos='https://cran.rstudio.com/')"

RUN conda update -n base -c conda-forge -y conda
RUN conda install -c conda-forge -y altair
RUN conda install -c conda-forge -y scikit-learn>=1.1.3
RUN conda install -c conda-forge -y lxml
RUN conda install -c conda-forge -y pandoc

RUN pip install joblib --quiet
RUN pip install mglearn --quiet
RUN pip install psutil --quiet
RUN pip install docopt-ng --quiet
RUN pip install vl-convert-python --quiet