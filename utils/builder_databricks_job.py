from databricks_cli.configure.provider import get_config, set_config_provider, EnvironmentVariableConfigProvider
from databricks_cli.jobs.api import JobsApi, JobsService
from databricks_cli.sdk import ApiClient

from utils.builder_databricks_config import BuilderDatabricksConfigJob


class BuilderDatabricksJob:
    jobs_service: JobsService
    api_client: ApiClient
    jobs_api: JobsApi

    def __init__(self, databricks_config: BuilderDatabricksConfigJob):
        self.config = databricks_config
        self.api_client = self._build_api_client()
        self.jobs_service = JobsService(self.api_client)
        self.jobs_api = JobsApi(self.api_client)

    def build_job(self):
        jobs = self._list_jobs_by_name(self.config.name)

        if len(jobs) > 0:
            job_id = jobs[0]["job_id"]
            response = self.jobs_service.reset_job(job_id, self.config.get_job_config())
        else:
            response = self.jobs_api.create_job(self.config.get_job_config())
            job_id = response['job_id']

        self.jobs_service.run_now(job_id)

    def _list_jobs_by_name(self, name) -> list:
        jobs = self.jobs_service.list_jobs()['jobs']
        return list(filter(lambda job: job['settings']['name'] == name, jobs))

    @staticmethod
    def _build_api_client():
        set_config_provider(EnvironmentVariableConfigProvider())
        config = get_config()
        username = config.username  # $DATABRICKS_USERNAME
        token = config.token  # $DATABRICKS_TOKEN
        host = config.host  # $DATABRICKS_HOST
        return ApiClient(username, token, host, verify=True)
