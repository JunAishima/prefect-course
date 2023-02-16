from prefect.orion.schemas.schedules import CronSchedule
from prefect.deployments import Deployment
from blocks_alphavantage1 import get_info
from prefect.filesystems import S3, GitHub

github_block = GitHub.load("prefect-course")

s3_block = S3.load("prefect-test")

cron_deploy = Deployment.build_from_flow(
    get_info,
    "info_cron_github",
    schedule=CronSchedule(cron="0 0 * * *", timezone="America/New_York"),
    parameters={"name":"GOOG"},
    storage=github_block
)

if __name__=="__main__":
    cron_deploy.apply()
