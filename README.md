# MLOPs Project Teamplate - Integrating Github Actions With Databricks
- for each pull-request to Github, the pipeline builds a new image, then creates a Databricks job, and finally sends the job results to Github
- this is for projects with high computational needs, such as training machine learning models or performing distributed tasks (Spark).

# How To Run
- Setup Github Secret Variables - you have to specify 6 action secret
  - DATABRICKS_HOST, DATABRIKCS_TOKEN, DATABRICKS_USERNAME, DOCKER_TOKEN, DOCKER_USERNAME, TOKEN_GITHUB
- Setup Github Action Environment Variables
  - REGISTRY, USERNAME_GITHUB, IMAGE_NAME

# Next Steps
To adapt the project to your needs start by editing the `runner.py` - which is the project entrypoint

More Info Here