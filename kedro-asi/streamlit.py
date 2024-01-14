import streamlit as st
from kedro.framework.startup import bootstrap_project
from kedro.framework.session import KedroSession
from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd

# Załadowanie kontekstu Kedro
project_path = Path.cwd()
bootstrap_project(project_path)

with KedroSession.create(project_path) as session:
    st.title('Kedro pipeline')

    if st.button('Start Kedro Pipeline'):
        session.run(pipeline_name="__default__")
        st.success('Pipeline has been started successfully!')
