from kedro.pipeline import Pipeline, node, pipeline

from .nodes import read_data


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=read_data,
                inputs=["params:url", "params:path"],
                outputs="df",
                name="read_data"
            )
        ]
    )
