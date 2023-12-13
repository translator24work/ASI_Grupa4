import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from typing import Dict, Tuple


def handle_missing_values(universities: pd.DataFrame) -> pd.DataFrame:
    universities = universities.drop(columns=['broad_impact'])
    return universities.dropna()


def normalize_numerical_data(universities: pd.DataFrame) -> pd.DataFrame:
    numerical_cols = ['score', 'patents', 'year', 'citations', 'publications',
                      'influence', 'quality_of_faculty', 'alumni_employment', 'alumni_employment',
                      'quality_of_education', 'national_rank']

    scaler = StandardScaler()
    universities[numerical_cols] = scaler.fit_transform(universities[numerical_cols])

    imputer = SimpleImputer(strategy='mean')
    universities[numerical_cols] = imputer.fit_transform(universities[numerical_cols])
    return universities


def encode_categorical_data(universities: pd.DataFrame) -> pd.DataFrame:
    categorical_cols = ['country', 'institution']
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded = encoder.fit_transform(universities[categorical_cols])
    universities = universities.drop(categorical_cols, axis=1)
    universities = pd.concat([universities, pd.DataFrame(encoded)], axis=1)
    return universities


def split_data(universities: pd.DataFrame, parameters: Dict) -> Tuple:
    universities.columns = universities.columns.astype(str)
    X = universities.drop('world_rank', axis=1)
    y = universities['world_rank']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=parameters["test_size"],
                                                        train_size=parameters["train_size"],
                                                        random_state=parameters["random_state"])
    return X_train, X_test, y_train, y_test
