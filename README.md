# ASI_Grupa4

## Project Description

This project serves as an advanced exploration into the realm of artificial intelligence, concentrating on the utilization of innovative AI tools. It delves into creating synthetic data to empower machine learning models, harnesses the power of AutoML for automated model selection and optimization, evaluates model performance rigorously, and implements strategies for efficient deployment. The initiative aims to demonstrate cutting-edge techniques in AI research and application, providing a framework for robust AI system development.

## Installation
* Clone the repository to your local machine:
```
git clone https://github.com/translator24work/ASI_Grupa4.git
```
*Create conda environment:
```
conda create --name kedro-environment python=3.10 -y
conda activate kedro-environment
conda install -c conda-forge kedro
conda install -c conda-forge kedro-viz
conda activate kedro-environment
```
* Install kedro dependencies:
```
cd kedro-asi/
pip install -r src/requirements.txt
```
* Install postgresql on your machine:
```
https://www.postgresql.org/download/
```
* Now we need to define database schema and table. In repository, you can find file named
`init.sql` that will do it.
* After executing this script you can use `dump.sql` that will insert data from csv file into sql table. You need to
replace path inside it (`/path/to/your/file.csv`) with correct path to your local `cwurData.csv`
* Now you need to place in `kedro-asi/conf/local/credentials.yml` (replace `your_username`, `your_password`, `your_database` with your proper postgresql configuration):
```
my_postgres_db:
  type: postgres
  host: localhost
  port: 5432
  username: your_username
  password: your_password
  database: your_database
```
## If you want to deploy pipeline with StreamLit you need to do:
```
cd kedro-asi/
streamlit run streamlit.py
```
## Dataset

The dataset  "World University Rankings" contains comprehensive data on the ranking of global universities. 
It includes various scores reflecting the quality of education and faculty, as well as the institution's international outlook and research influence. 
This dataset can be useful for analyzing trends in higher education, comparing institutions, and understanding the factors that contribute to a university's reputation and academic standing. 
[source: Kaggle][https://www.kaggle.com/datasets/mylesoneill/world-university-rankings/data](https://www.kaggle.com/datasets/mylesoneill/world-university-rankings/data)

## Stack

- **SDV**: synthetic data
- **AutoGluon**: training and choosing best model
- **Kedro**: pipeline
- **Weights&Biases**: evaluation
- **Streamlit**: deployment

