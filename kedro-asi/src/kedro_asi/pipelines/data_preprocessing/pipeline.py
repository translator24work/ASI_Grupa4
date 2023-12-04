from kedro.pipeline import Pipeline, node, pipeline

from .nodes import preprocess_data, encode_categorical_data, prepare_data

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess_data,
                inputs=["df"],
                outputs=["X_train_numeric", "X_val_numeric", "X_test_numeric", "X_train_final", "X_val_final", "X_test_final", "y_train", "y_val", "y_test"],
                name="preprocess_data"
            ),
            node(
                func=prepare_data,
                inputs=["X_train_numeric", "X_val_numeric", "X_test_numeric", "X_train_final", "X_val_final", "X_test_final", "y_train", "y_val", "y_test"],
                outputs=["X_train_prepared", "X_val_prepared", "X_test_prepared", "y_train_prepared", "y_val_prepared", "y_test_prepared"],
                name="prepare_data"
            )
        ]
    )
