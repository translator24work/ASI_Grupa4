import streamlit as st
from kedro.framework.startup import bootstrap_project
from kedro.framework.session import KedroSession
from kedro.config import ConfigLoader
from pathlib import Path
import requests
import pandas as pd
import psycopg2
import numpy as np
from autogluon.tabular import TabularPredictor
#from sdv.lite import SingleTablePreset
#from sdv.metadata import SingleTableMetadata
#from sdv.metadata import SingleTableMetadata


# Załadowanie kontekstu Kedro
project_path = Path.cwd()
bootstrap_project(project_path)


FASTAPI_ENDPOINT = "http://localhost:8000/predict"
SYNTHETIC_DATA_SCRIPT = "main.py"

conf_loader = ConfigLoader(conf_source=str(Path.cwd() / 'conf'))

with KedroSession.create(project_path) as session:
    st.title('Kedro pipeline')

    if st.button('Start Kedro Pipeline'):
        session.run(pipeline_name="__default__")
        st.success('Pipeline has been started successfully!')

    if st.button('Generate synthetic data'):
        metadata = SingleTableMetadata()

        # odczytanie credentials
        conf_loader = ConfigLoader(conf_source=str(Path.cwd() / 'conf'))
        credentials = conf_loader.get("local/credentials", "credentials.yml")
        # Parametry połączenia z bazą danych
        db_username = credentials["postgres"]["username"]
        db_password = credentials["postgres"]["password"]
        db_host = credentials["postgres"]["host"]
        db_port = credentials["postgres"]["port"]
        db_name = credentials["postgres"]["name"]

        # Łączenie z bazą danych
        connection = psycopg2.connect(
            dbname=db_name,
            user=db_username,
            password=db_password,
            host=db_host,
            port=db_port
        )

        # Wczytywanie danych z bazy danych do DataFrame
        query = "SELECT * FROM cwur.cwur"
        real_data = pd.read_sql(query, connection)

        # Zamykanie połączenia
        connection.close()

        meta_data = metadata.detect_from_dataframe(real_data)

        synthesizer = SingleTablePreset(metadata, name='FAST_ML')
        synthesizer.fit(data=real_data)

        synthetic_data = synthesizer.sample(num_rows=500)

        st.write('About synthetic data:')
        st.dataframe(synthetic_data)

    with st.form(key='predict_form'):
        world_rank = st.number_input('World Rank', min_value=1)
        institution = st.text_input('Institution', value="Harvard University")
        country = st.text_input('Country', value="USA")
        national_rank = st.number_input('National Rank', min_value=1)
        quality_of_education = st.number_input('Quality of Education', min_value=1)
        alumni_employment = st.number_input('Alumni Employment', min_value=1)
        quality_of_faculty = st.number_input('Quality of Faculty', min_value=1)
        publications = st.number_input('Publications', min_value=1)
        influence = st.number_input('Influence', value=1)
        citations = st.number_input('Citations', value=1)
        broad_impact = st.number_input('Broad Impact', value=1)
        patents = st.number_input('Patents', value=1)
        score = st.number_input('Score', value=1)
        year = st.number_input('Year', value=1)

        submit_button = st.form_submit_button('Make a Prediction')

    if submit_button:
        # preparing data for prediction
        data_to_predict = {
            'world_rank': world_rank,
            'institution': institution,
            'country': country,
            'national_rank': national_rank,
            'quality_of_education': quality_of_education,
            'alumni_employment': alumni_employment,
            'quality_of_faculty': quality_of_faculty,
            'publications': publications,
            'influence': influence,
            'citations': citations,
            'broad_impact': broad_impact,
            'patents': patents,
            'score': score,
            'year': year
        }
        print(data_to_predict)

        # Wysyłanie żądania do FastAPI
        response = requests.post(FASTAPI_ENDPOINT, json=data_to_predict)

        if response.status_code == 200:
            prediction = response.json()
            st.success(f"Prediction Score: {prediction}")
        else:
            st.error("Error while making predictions")
