from kedro.pipeline import Pipeline, node, pipeline

from .nodes import handle_missing_values, normalize_numerical_data, encode_categorical_data, split_data


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=handle_missing_values,
                inputs="universities",
                outputs="universities_clean",
                name="handle_missing_values"
            ),
            node(
                func=normalize_numerical_data,
                inputs="universities_clean",
                outputs="universities_normalized",
                name="normalize_numerical_data"
            ),
            node(
                func=encode_categorical_data,
                inputs="universities_normalized",
                outputs="universities_encoded",
                name="encode_categorical_data"
            ),
            node(
                func=split_data,
                inputs=["universities_encoded", "params:model_options.test_size", "params:model_options.random_state"],
                outputs=["X_train", "X_val", "X_test", "y_train", "y_test"],
                name="split_data"
            )
        ]
    )
