import logging
from datetime import datetime
from typing import Dict, Tuple

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import wandb


def split_data(data: pd.DataFrame, parameters: Dict) -> Tuple:
    X = data[parameters["features"]]
    # FIXME: Maybe change y feature
    y = data["world_rank"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=parameters["test_size"], train_size=parameters["train_size"],
        random_state=parameters["random_state"]
    )
    return X_train, X_test, y_train, y_test


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> LinearRegression:
    init_wandb()
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    return regressor


def init_wandb():
    print('init wandb')
    current_timestamp = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
    wandb.init(project="wandb_asi", name=f'run_{current_timestamp}')


def close_wandb():
    wandb.finish()


def evaluate_model(
        regressor: LinearRegression, X_test: pd.DataFrame, y_test: pd.Series
):
    y_pred = regressor.predict(X_test)
    score = r2_score(y_test, y_pred)
    logger = logging.getLogger(__name__)
    logger.info("Model has a coefficient R^2 of %.3f on test data.", score)
    wandb.log({"r2_score": score})
    close_wandb()
    return score
