from fastapi import FastAPI, HTTPException, Request
from autogluon.tabular import TabularPredictor
from kedro.framework.startup import bootstrap_project
from kedro.framework.session import KedroSession
from kedro.config import ConfigLoader
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from sdv.lite import SingleTablePreset
from sdv.metadata import SingleTableMetadata

app = FastAPI()
DATABASE_SCHEMA_NAME = 'cwur'
SYNTHETIC_DATA_TABLE_NAME = 'synthetic_cwur'
PRODUCTION_DATA_TABLE_NAME = 'cwur'


@app.get('/run')
async def run_pipeline():
    try:
        project_path = Path.cwd()
        bootstrap_project(project_path)
        with KedroSession.create(project_path) as session:
            session.run(pipeline_name="__default__")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/logs')
async def see_kedro_logs():
    try:
        log_file_path = Path.cwd() / 'info.log'
        with open(log_file_path, 'r') as log_file:
            log_contents = log_file.read()
            return {"logs": log_contents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/predict')
async def make_prediction(request: Request):
    try:
        global predictor
        model_directory = Path('AutogluonModels')
        if not model_directory.exists():
            raise FileNotFoundError(f"Could not find directory with Autogluon Models: {model_directory}")
        latest_model_path = max(model_directory.iterdir(), key=lambda x: x.stat().st_mtime)
        if not latest_model_path.is_dir():
            raise FileNotFoundError(f"Could not find specific model: {latest_model_path}")
        print('Znalazłem model poprawnie')
        input_data = await request.json()
        data = pd.DataFrame([input_data])
        predictor = TabularPredictor.load(str(latest_model_path))
        prediction = predictor.predict(data)
        return {"prediction": prediction.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/predictSynthetic')
async def make_prediction_for_synthetic():
    try:
        global predictor
        model_directory = Path('AutogluonModels')
        if not model_directory.exists():
            raise FileNotFoundError(f"Could not find directory with Autogluon Models: {model_directory}")
        latest_model_path = max(model_directory.iterdir(), key=lambda x: x.stat().st_mtime)
        if not latest_model_path.is_dir():
            raise FileNotFoundError(f"Could not find specific model: {latest_model_path}")
        created_predictor = TabularPredictor.load(str(latest_model_path))
        conf_loader = ConfigLoader(conf_source=str(Path.cwd() / 'conf'))
        credentials = conf_loader.get("local/credentials", "credentials.yml")
        db_username = credentials["postgres"]["username"]
        db_password = credentials["postgres"]["password"]
        db_host = credentials["postgres"]["host"]
        db_port = credentials["postgres"]["port"]
        database_name = credentials["postgres"]["database"]
        user = db_username
        password = db_password
        host = db_host
        database = database_name
        connection_string = f"postgresql://{user}:{password}@{host}:{db_port}/{database}"
        engine = create_engine(connection_string)
        synthetic_data = pd.read_sql_table(SYNTHETIC_DATA_TABLE_NAME, engine, DATABASE_SCHEMA_NAME)
        prediction = created_predictor.predict(synthetic_data)
        return {"prediction": prediction.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/synthetic')
async def generate_synthetic_data(request: Request):
    try:
        number_of_rows = await request.json()
        metadata = SingleTableMetadata()
        conf_loader = ConfigLoader(conf_source=str(Path.cwd() / 'conf'))
        credentials = conf_loader.get("local/credentials", "credentials.yml")
        db_username = credentials["my_postgres_db"]["username"]
        db_password = credentials["my_postgres_db"]["password"]
        db_host = credentials["my_postgres_db"]["host"]
        db_port = credentials["my_postgres_db"]["port"]
        database_name = credentials["my_postgres_db"]["database"]
        user = db_username
        password = db_password
        host = db_host
        database = database_name
        connection_string = f"postgresql://{user}:{password}@{host}:{db_port}/{database}"
        engine = create_engine(connection_string)
        real_data = pd.read_sql_table(PRODUCTION_DATA_TABLE_NAME,
                                      engine,
                                      DATABASE_SCHEMA_NAME)
        metadata.detect_from_dataframe(real_data)
        metadata.update_column(column_name='institution', sdtype='categorical')

        synthesizer = SingleTablePreset(metadata, name='FAST_ML')
        synthesizer.fit(data=real_data)
        synthetic_data = synthesizer.sample(num_rows=number_of_rows['number_of_rows'])
        synthetic_data.to_sql(SYNTHETIC_DATA_TABLE_NAME,
                              engine,
                              DATABASE_SCHEMA_NAME,
                              if_exists='append',
                              index=False)

        return {"synthetic": synthetic_data.to_json()}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))
