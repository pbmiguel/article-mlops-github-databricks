from invoke import task

from utils.builder_databricks_config import BuilderDatabricksConfigJob
from utils.builder_databricks_job import BuilderDatabricksJob


@task
def deploy_to_databricks(
        c,
        databricks_job_name= None,
        docker_url= None,
        docker_username= None,
        docker_password= None,
        num_workers=0,
        python_path="",
        python_params=""
):

    config = BuilderDatabricksConfigJob(
        name=databricks_job_name,
        python_path=python_path,
        python_params=python_params,
        docker_url=docker_url,
        docker_username=docker_username,
        docker_password=docker_password,
        number_workers=num_workers
    )
    BuilderDatabricksJob(config).build_job()



