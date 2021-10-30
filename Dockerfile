FROM databricksruntime/python:8.x

ENV PATH /databricks/conda/bin:$PATH

RUN apt-get update \
  && apt-get install -y python3-dev g++\
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir --upgrade poetry==1.1.11  \
  && poetry config virtualenvs.create false \
  && poetry install

COPY . /demo-python-docker-img