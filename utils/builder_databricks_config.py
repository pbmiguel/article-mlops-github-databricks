class BuilderDatabricksConfigJob():
    def __init__(self,
                 name: str,
                 python_path: str,
                 python_params: str,
                 docker_url: str,
                 docker_username: str,
                 docker_password: str,
                 number_workers=0):
        self.name = name
        self.number_workers = number_workers
        self.python_task_path = python_path
        self.single_node = True if number_workers is 0 else False
        self.docker_url = docker_url
        self.docker_username = docker_username
        self.docker_password = docker_password
        self.python_params = python_params

    def get_job_config(self) -> str:
        config = {
            "name": self.name,
            "num_workers": self.number_workers,
            "new_cluster": {
                "spark_version": "7.3.x-scala2.12",
                "node_type_id": "Standard_DS3_v2",
                "policy_id": None,
                "num_workers": self.number_workers,
                "docker_image": {
                    "url": self.docker_url,
                    "basic_auth": {
                        "username": self.docker_username,
                        "password": self.docker_password
                    }
                },
                "spark_conf": {},
                "init_scripts": [],
                "custom_tags": {},
                "spark_env_vars": {
                    "PYSPARK_PYTHON": "/usr/bin/python"
                }
            },
            "max_concurrent_runs": 60,
            "max_retries:": 0,
            "min_retry_interval_millis": 0,
            "timeout_seconds": "None",
            "spark_env_vars": {
                "PYSPARK_PYTHON": "/usr/bin/python"
            },
            "spark_python_task": {
                "python_file": f"file://{self.python_task_path}",
                "parameters": []
            }
        }

        for param in self.python_params.split("--"):
            if param:
                new_param = f"--{param.strip()}"
                config["spark_python_task"]["parameters"].append(new_param)

        if self.single_node:
            config["num_workers"] = 0
            config["new_cluster"]["spark_conf"]["spark.databricks.cluster.profile"] = "singleNode"
            config["new_cluster"]["spark_conf"]["spark.master"] = "local[*, 4]"
            config["new_cluster"]["custom_tags"]["ResourceClass"] = "SingleNode"

        return config