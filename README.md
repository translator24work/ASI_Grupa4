# ASI_Grupa4

## Run tutorial:
* Create conda environment:
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
## Now you should be fine to use your pipeline :)