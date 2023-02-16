from prefect import flow

@flow
def flow(abc):
    print(f"abc: {abc}")
