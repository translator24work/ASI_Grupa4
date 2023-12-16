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
* Define database, schema and table that will contain our data. Below is sql script that will create table (replace *your_schema* with your schema name):
```
-- Table: your_schema.cwur

-- DROP TABLE IF EXISTS your_schema.cwur;

CREATE TABLE IF NOT EXISTS your_schema.cwur
(
    world_rank integer,
    institution character varying COLLATE pg_catalog."default",
    country character varying COLLATE pg_catalog."default",
    national_rank integer,
    quality_of_education integer,
    alumni_employment integer,
    quality_of_faculty integer,
    publications integer,
    influence integer,
    citations integer,
    broad_impact double precision,
    patents integer,
    score double precision,
    year integer
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS your_schema.cwur
    OWNER to postgres;
```
* After that we can insert data from csv file into sql table (replace *your_table* with your table name and */path/to/your/file.csv* with path to your local cwurData.csv):
```
COPY your_table FROM '/path/to/your/file.csv' DELIMITER ',' CSV HEADER;
```
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