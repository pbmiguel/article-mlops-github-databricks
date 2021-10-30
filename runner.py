from pyspark.ml.linalg import Vectors
from pyspark.ml.stat import ChiSquareTest
from pyspark.sql import SparkSession
import argparse
from github import Github


class ServiceGithub():
    client: Github

    def __init__(self, token, repo_name, pull_request_id):
        self.client = Github(token)
        self.pull_request_id = pull_request_id
        self.repo = self.client.get_repo(repo_name)

    def publish_comment(self, body):
        body = f'''
        RESULTS:
            {body}
        '''
        pr = self.repo.get_pull(self.pull_request_id)
        pr.create_issue_comment(body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--github_token')
    parser.add_argument('--github_pull_request_id')
    parser.add_argument('--github_repo_name')
    args = parser.parse_args()

    spark = SparkSession.builder.appName("chi_squared_test").getOrCreate()

    data = [(0.0, Vectors.dense(0.5, 10.0)),
            (0.0, Vectors.dense(1.5, 20.0)),
            (0.0, Vectors.dense(3.5, 30.0)),
            (0.0, Vectors.dense(3.5, 40.0)),
            (1.0, Vectors.dense(3.5, 40.0))]

    df = spark.createDataFrame(data, ["label", "features"])

    r = ChiSquareTest.test(df, "features", "label").head()
    print("pValues: " + str(r.pValues))
    print("degreesOfFreedom: " + str(r.degreesOfFreedom))
    print("statistics: " + str(r.statistics))

    service = ServiceGithub()

    service.publish_comment(
        f"""
                pValues {str(r.pValues)}
                degreesOfFreedom {str(r.degreesOfFreedom)}
                statistics {str(r.statistics)}
                """
    )
