from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_model_input_table, preprocess_universities


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess_universities,
                inputs="universities",
                outputs="preprocessed_universities",
                name="preprocess_universities_node"
            ),
            node(
                func=create_model_input_table,
                inputs="preprocessed_universities",
                outputs="model_input_table",
                name="create_model_input_table_node"
            )
        ]
    )