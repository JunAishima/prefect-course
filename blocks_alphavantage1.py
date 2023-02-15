from prefect import task, flow
from prefect.blocks.system import Secret
import httpx

@task
def get_alphavantage(function, name, key, interval="5min"):
    return httpx.get(f"https://www.alphavantage.co/query?function={function}&symbol={name}&interval={interval}&apikey={key}")

@task
def get_secret_block(name):
    secret_block = Secret.load(name)# Access the stored secretsecret_block.get()
    return secret_block

@flow
def get_info(name, secret_name):
    result = get_alphavantage("TIME_SERIES_INTRADAY", "IBM", get_secret_block(secret_name).get())
    #print(result.json())
    #print(result.json().keys())
    price = result.json()["Time Series (5min)"]["2023-02-14 19:55:00"]["1. open"]
    return price

@flow
def get_info_multiple():
    price = get_info("IBM", "alphavantage-1")
    return price


if __name__ == "__main__":
    price = get_info_multiple()
    print(f"price is {price}")