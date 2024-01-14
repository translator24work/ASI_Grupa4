import streamlit as st
from kedro.framework.startup import bootstrap_project
from kedro.framework.session import KedroSession
from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd
import joblib

# Load your trained model
model = joblib.load('AutogluonModels/ag-20231213_182836/predictor.pkl')

# Załadowanie kontekstu Kedro
project_path = Path.cwd()
bootstrap_project(project_path)

with KedroSession.create(project_path) as session:
    st.title('Kedro pipeline')

    if st.button('Start Kedro Pipeline'):
        session.run(pipeline_name="__default__")
        st.success('Pipeline has been started successfully!')

    with st.form(key='predict_form'):
        world_rank = st.number_input('World Rank', min_value=1)
        institution = st.text_input('Institution', value="")
        country = st.text_input('Country', value="")
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
            'institution': instituion,
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
        data_to_predict_df = pd.DataFrame([data_to_predict])

        # Make a prediction
        prediction = model.predict(data_to_predict_df)

        # Display the prediction
        st.success(f'Prediction Score: {prediction}')
