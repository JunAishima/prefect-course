from prefect import task, flow
import httpx

@task(log_prints=True, retries=3, retry_delay_seconds=0.1)
def get_meteo(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    return most_recent_temp

@flow(log_prints=True)
def get_weather(location):
    print(f"location: {location}")
    print(f"Temperature is {get_meteo(location[0], location[1])}")

@task(log_prints=True)
def get_locations():
    to_return = []
    with open('locations.txt', 'r') as locations:
        f=locations.readline().split()
        while f:
            to_return.append((f[0], f[1]))
            f= locations.readline().split()
    return to_return

@flow(log_prints=True)
def get_all():
    locations = get_locations()
    for index, location in enumerate(locations):
        get_weather(location)

get_all()