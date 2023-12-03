import pandas as pd


def preprocess_universities(universities: pd.DataFrame) -> pd.DataFrame:
    return universities


def create_model_input_table(
        universities: pd.DataFrame
) -> pd.DataFrame:
    universities = universities.drop_duplicates()
    # TODO: Do some more preprocessing
    # TODO: maybe remove broad_impact column? (seems to be empty in most records)
    return universities