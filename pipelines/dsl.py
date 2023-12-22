import os

from kfp import dsl, kubernetes
from kfp.compiler import Compiler
from kfpclientmanager import KFPClientManager


@dsl.container_component
def Train() -> dsl.ContainerSpec:
    image_name = os.getenv("IMAGE_NAME")
    model_output_path = os.getenv("MODEL_OUTPUT_PATH")
    version = os.getenv("MODEL_VERSION", "v1.0.0")
    return dsl.ContainerSpec(
        image= image_name,
        command=["python", "train.py"],
        args=[
                f"--model-base-path={model_output_path}",
                f"--model-version={version}"
            ]
    )


def mount_pvc(component, pvc_name):
    kubernetes.mount_pvc(
        component,
        pvc_name=pvc_name,
        mount_path='/data',
    )

@dsl.pipeline(
    name="FIFA Player Predict Pipeline",
    description="""
        A pipeline that uses a custom Docker image for data processing.
    """,
)
def fifa_predictior_pipeline():
    mount_pvc(Train(), 'dataset-pvc')


def deploy_pipeline(pipeline_file:str):
    namespace="kubeflow-user-example-com"
    api_url = os.getenv("KF_PIPELINES_ENDPOINT","http://192.168.0.150.nip.io/") + "/pipeline"
    version = os.getenv("MODEL_VERSION", "v1.0.0")
    client_manager = KFPClientManager(
        api_url=api_url,
        dex_username="user@example.com",
        dex_password="12341234"
    )
    Client = client_manager.create_kfp_client()

    pipelines = Client.list_pipelines(namespace=namespace)
    if pipelines.pipelines is not None:
        for pipeline in pipelines.pipelines:
            if pipeline.display_name == "fifa_predictior_pipeline":
                Client.upload_pipeline_version(
                                            pipeline_id=pipeline.pipeline_id,
                                            pipeline_package_path=pipeline_file,
                                            pipeline_version_name=version
                                        )
            return

    Client.upload_pipeline(
                pipeline_name="fifa_predictior_pipeline",
                pipeline_package_path=pipeline_file,
                namespace=namespace
                )


def create_pipeline(pipeline_file:str):
    Compiler().compile(fifa_predictior_pipeline, pipeline_file)
    deploy_pipeline(pipeline_file=pipeline_file)


if __name__ == "__main__":
    pipeline_file = "fifa_predictior_pipeline.yaml"
    create_pipeline(pipeline_file)


