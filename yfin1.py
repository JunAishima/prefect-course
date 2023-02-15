import datetime
from prefect import task, flow
from prefect.tasks import task_input_hash
import yfinance

@task(cache_key_fn=task_input_hash, retries=3)
def get_yfin_info(name):
    df = yfinance.download(name)
    return df

@flow #subflow?
def extract_field(name, field):
    return get_yfin_info(name)[field]

@flow
def assemble_report(name):
    open = extract_field(name, 'Open')
    close = extract_field(name, 'Close')
    volume = extract_field(name, 'Volume')
    print(f"Last open: {open[-1]} last close: {close[-1]} volume: {volume[-1]}")
    print(f"Averages: open: {open.mean()} close: {close.mean()} volume: {volume.mean()}")

@flow(log_prints=True)
def multiple_reports(names):
    for name in names:
        print(f"assembling report for {name}")
        assemble_report(name)
    print("all done")

if __name__ == "__main__":
    names = ["GM", "TSLA"]
    multiple_reports(names)