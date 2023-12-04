from kedro.pipeline import Pipeline, node, pipeline

from .nodes import evaluate_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=evaluate_model,
                inputs=["model", "X_val", "y_val"],
                outputs=["mse_val"],
                name="evaluate_model"
            )
        ]
    )
