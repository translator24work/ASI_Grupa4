import pandas as pd
import logging

import wandb
from autogluon.tabular import TabularPredictor
from datetime import datetime
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
from sklearn.model_selection import train_test_split


def init_wandb():
    current_timestamp = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
    wandb.init(project="wandb_asi", name=f'run_{current_timestamp}')


def close_wandb():
    wandb.finish()


def evaluate_model(universities: pd.DataFrame):
    init_wandb()

    x_train, x_test = train_test_split(universities)
    predictor = TabularPredictor(label='world_rank').fit(pd.DataFrame(x_train))

    y_test = predictor.predict(x_train)
    y_pred = predictor.predict(x_test)
    logger = logging.getLogger(__name__)

    r2_value = r2_score(y_test, y_pred)
    mse_value = mean_squared_error(y_test, y_pred, squared=True)
    rmse_value = mean_squared_error(y_test, y_pred, squared=False)
    mae_value = mean_absolute_error(y_test, y_pred)
    mape_value = mean_absolute_percentage_error(y_test, y_pred)

    logger.info("Model has R^2 of %.3f on test data.", r2_value)
    logger.info("Model has MSE of %.1f on test data.", mse_value)
    logger.info("Model has RMSE of %.1f on test data.", rmse_value)
    logger.info("Model has MAE of %.1f on test data.", mae_value)
    logger.info("Model has MAPE of %.3f on test data.", mape_value)

    # Feature importance
    importance_list = predictor.coef_
    importance_df = pd.DataFrame({'feature': x_test.columns, 'importance': importance_list})
    logger.info(f"Model importance {importance_df}")

    wandb.log({
        "importance": importance_df,
    })

    wandb.run.summary["r2"] = r2_value
    wandb.run.summary["mse"] = mse_value
    wandb.run.summary["rmse"] = rmse_value
    wandb.run.summary["mae"] = mae_value
    wandb.run.summary["mape"] = mape_value

    close_wandb()
    return r2_value, mse_value, rmse_value, mae_value, mape_value
