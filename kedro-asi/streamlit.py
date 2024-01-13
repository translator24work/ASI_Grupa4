import streamlit as st
from kedro.framework.startup import bootstrap_project
from kedro.framework.session import KedroSession
from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd

# Załadowanie kontekstu Kedro
project_path = Path.cwd()
bootstrap_project(project_path)

# Database connection (modify with actual database details)
engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')

with KedroSession.create(project_path) as session:
    st.title('Aplikacja Streamlit do Zarządzania Danymi CWUR')

    if st.button('Uruchom Potok Kedro'):
        session.run(pipeline_name="__default__")
        st.success('Potok został uruchomiony!')

    with st.form(key='cwur_data_form'):
        world_rank = st.number_input('World Rank', min_value=1)
        institution = st.text_input('Institution')
        country = st.text_input('Country')
        national_rank = st.number_input('National Rank', min_value=1)
        quality_of_education = st.number_input('Quality of Education', min_value=1)
        alumni_employment = st.number_input('Alumni Employment', min_value=1)
        quality_of_faculty = st.number_input('Quality of Faculty', min_value=1)
        publications = st.number_input('Publications', min_value=1)
        influence = st.number_input('Influence', min_value=1)
        citations = st.number_input('Citations', min_value=1)
        broad_impact = st.number_input('Broad Impact', min_value=1.0, format='%f')
        patents = st.number_input('Patents', min_value=1)
        score = st.number_input('Score', min_value=1.0, format='%f')
        year = st.number_input('Year', min_value=1900, max_value=2100, step=1)
        submit_button = st.form_submit_button('Dodaj dane')

    if submit_button:
        # Prepare data for insertion
        data_to_insert = {
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

        # Insert data into the database
        try:
            df_to_insert = pd.DataFrame([data_to_insert])
            df_to_insert.to_sql('cwur', con=engine, schema='cwur', if_exists='append', index=False)
            st.success('Dane zostały dodane!')
        except Exception as e:
            st.error(f'Błąd podczas dodawania danych: {e}')
