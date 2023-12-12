import pandas as pd
import logging
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


def train_model(X_train: pd.DataFrame, y_train: pd.DataFrame) -> BaseEstimator:
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model: BaseEstimator, X_train: pd.DataFrame, X_test: pd.DataFrame,
                   y_train: pd.Series, y_test: pd.Series):
    train_predictions = model.predict(X_train)
    test_predictions = model.predict(X_test)

    train_rmse = mean_squared_error(y_train, train_predictions, squared=False)
    test_rmse = mean_squared_error(y_test, test_predictions, squared=False)

    logger = logging.getLogger(__name__)
    logger.info(f"RMSE: \nTraining: {train_rmse},\nTesting: {test_rmse}")
