from prefect.orion.schemas.schedules import CronSchedule, IntervalSchedule
from prefect.deployments import Deployment
from blocks_alphavantage1 import get_info

cron_deploy = Deployment.build_from_flow(
    get_info,
    "info_cron",
    schedule=CronSchedule(cron="0 0 * * *", timezone="America/New_York"),
    parameters={"name":"GOOG"}
)

interval_deploy = Deployment.build_from_flow(
    get_info,
    "info_interval",
    schedule=IntervalSchedule(interval=600, timezone="America/New_York"),
    parameters={"name":"GM"}
)

if __name__=="__main__":
    cron_deploy.apply()
    interval_deploy.apply()
