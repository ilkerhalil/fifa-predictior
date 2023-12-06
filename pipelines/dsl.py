import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import (

    Artifact,
    Output

)



@dsl.container_component
def data_processing_op() -> dsl.ContainerSpec:
    return dsl.ContainerSpec(
        image="fifa-predictior:1.0.0",
        command=["python", "train.py"],

    )


@dsl.pipeline(
    name="FIFA Player Predict Pipeline",
    description="""
        A pipeline that uses a custom Docker image for data processing.
    """,
)
def fifa_predictior_pipeline():
    data_processing_op()


if __name__ == "__main__":
    kfp.compiler.Compiler().compile(fifa_predictior_pipeline, "fifa_predictior_pipeline")
    Output("fifa_predictior_pipeline.yaml", "fifa_predictior_pipeline.yaml")
