from kedro.pipeline import Pipeline, node, pipeline

from .nodes import train_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=train_model,
                inputs=["X_train", "y_train"],
                outputs=["model"],
                name="train_model"
            )
        ]
    )
