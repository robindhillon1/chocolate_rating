# Author: MDS Cohort7 522 Group 5
FROM continuumio/miniconda3:4.12.0

# Update apt
RUN apt-get update
RUN apt-get -y --no-install-recommends install

# Install R packages
RUN apt-get install -y r-base r-base-dev 

# Install R dependencies
RUN apt-get install -y libxml2-dev libcurl4-openssl-dev libssl-dev libfontconfig1-dev

RUN Rscript -e "install.packages('tidyverse', repos='https://cran.rstudio.com/')"
RUN Rscript -e "install.packages('broom', repos='https://cran.rstudio.com/')"
RUN Rscript -e "install.packages('docopt', repos='https://cran.rstudio.com/')"
RUN Rscript -e "install.packages('knitr', repos='https://cran.rstudio.com/')"
RUN Rscript -e "install.packages('kableExtra', repos='https://cran.rstudio.com/')"
RUN Rscript -e "install.packages('caret', repos='https://cran.rstudio.com/')"
RUN Rscript -e "install.packages('xfun', repos='https://cran.rstudio.com/')"

ENV PATH="/opt/conda/bin:${PATH}"

# Update conda
RUN conda update -n base -c conda-forge -y conda

# Install python packages
RUN conda install -c conda-forge -y altair==4.2.0
RUN conda install -c conda-forge -y scikit-learn>=1.1.3
RUN conda install -c conda-forge -y lxml==4.9.2
RUN conda install -c conda-forge -y pandoc==2.19.2

RUN pip install joblib==1.2.0 --quiet
RUN pip install mglearn==0.1.9 --quiet
RUN pip install psutil==5.9.4 --quiet
RUN pip install docopt-ng --quiet
RUN pip install vl-convert-python --quiet
