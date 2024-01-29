from pathlib import Path
import pandas as pd
import requests
import streamlit as st

model_path = max(Path('AutogluonModels').iterdir(), key=lambda x: x.stat().st_mtime)
SYNTHETIC_DATA_URL = "http://localhost:8000/synthetic"
RUN_PIPELINE_URL = "http://localhost:8000/run"
PREDICT_URL = "http://localhost:8000/predict"
PREDICT_URL_SYNTHETIC = "http://localhost:8000/predictSynthetic"


st.title('Streamlit app designed for working with Kedro pipelines ')

synthetic_data_amount = st.sidebar.number_input("Enter the number of synthetic samples to generate", min_value=1,
                                          max_value=1000, value=10)

if st.button('Start Kedro Pipeline'):
    response = requests.get(RUN_PIPELINE_URL)
    st.success('Kedro pipeline has been started')
    if response.status_code == 200:
        st.success('Kedro pipeline ended successfully!')
    else:
        st.error('There was some error while running Kedro pipeline')


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

    response = requests.post(PREDICT_URL, json=data_to_predict)

    if response.status_code == 200:
        prediction = response.json()
        st.success(f"Prediction: {prediction['prediction']}")
    else:
        st.error(f'There was some error while making prediction: {response}')


if st.sidebar.button('Generate Synthetic data'):
    synthetic_data_amount_json = {
        "number_of_rows": synthetic_data_amount
    }
    response = requests.post(SYNTHETIC_DATA_URL, json=synthetic_data_amount_json)
    if response.status_code == 200:
        st.success('Synthetic data has been generated')
        data = response.json()
        synthetic_data = pd.read_json(data['synthetic'])
        st.dataframe(synthetic_data)
    else:
        st.error('There was some error while creating synthetic data')
        st.write(response)


if st.sidebar.button('Make Prediction for synthetic data'):
    response = requests.get(PREDICT_URL_SYNTHETIC)
    if response.status_code == 200:
        prediction = response.json()
        st.success(f"Prediction for synthetic data: {prediction['prediction']}")
    else:
        st.error('There was some error while making prediction for synthetic data')
