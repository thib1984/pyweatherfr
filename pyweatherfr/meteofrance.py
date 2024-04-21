import pyweatherfr.args
import pyweatherfr.log

import openmeteo_requests
import requests_cache
import retry_requests
import datetime
import pytz
import pathlib
import sys
import os

DOSSIER_CONFIG_PYWEATHER = "pyweatherfr"


def resume(latitude, longitude, tz):
    retry_session = retry_requests.retry(cache_session(), retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = "https://api.open-meteo.com/v1/meteofrance"
    date_debut = (
        datetime.datetime.now(tz=pytz.timezone(tz))
        + datetime.timedelta(days=-1 * pyweatherfr.args.compute_args().past)
    ).strftime("%Y-%m-%d")
    date_fin = (
        datetime.datetime.now(tz=pytz.timezone(tz)) + datetime.timedelta(days=3)
    ).strftime("%Y-%m-%d")
    if pyweatherfr.args.compute_args().past != 0:
        date_fin = (
            datetime.datetime.now(tz=pytz.timezone(tz)) + datetime.timedelta(days=-1)
        ).strftime("%Y-%m-%d")
    params = {
        "timezone": tz,
        "start_date": date_debut,
        "end_date": date_fin,
        "latitude": latitude,
        "longitude": longitude,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "apparent_temperature_max",
            "apparent_temperature_min",
            "precipitation_sum",
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
            "wind_direction_10m_dominant",
            "weather_code",
            "snowfall_sum",
            "precipitation_hours",
            "sunshine_duration",
        ],
    }
    pyweatherfr.log.print_debug(
        "appel api meteo france "
        + url
        + "?"
        + "&".join(
            [
                f'{key}={",".join(value) if isinstance(value, list) else value}'
                for key, value in params.items()
            ]
        )
    )
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    daily_apparent_temperature_max = daily.Variables(2).ValuesAsNumpy()
    daily_apparent_temperature_min = daily.Variables(3).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(4).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(5).ValuesAsNumpy()
    daily_wind_gusts_10m_max = daily.Variables(6).ValuesAsNumpy()
    daily_wind_direction_10m_dominant = daily.Variables(7).ValuesAsNumpy()
    weather_code = daily.Variables(8).ValuesAsNumpy()
    snowfall = daily.Variables(9).ValuesAsNumpy()
    precipitation_hours = daily.Variables(10).ValuesAsNumpy()
    sunshine_duration = daily.Variables(11).ValuesAsNumpy()
    alt = response.Elevation()
    debut = daily.Time()
    fin = daily.TimeEnd()
    return (
        daily_temperature_2m_min,
        daily_temperature_2m_max,
        daily_apparent_temperature_min,
        daily_apparent_temperature_max,
        daily_precipitation_sum,
        daily_wind_speed_10m_max,
        daily_wind_gusts_10m_max,
        daily_wind_direction_10m_dominant,
        weather_code,
        snowfall,
        precipitation_hours,
        sunshine_duration,
        alt,
        debut,
        fin,
    )


def specific_day(latitude, longitude, day, tz):
    retry_session = retry_requests.retry(cache_session(), retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = "https://api.open-meteo.com/v1/meteofrance"
    params = {
        "timezone": tz,
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m",
            "apparent_temperature",
            "precipitation",
            "wind_speed_10m",
            "wind_gusts_10m",
            "wind_direction_10m",
            "pressure_msl",
            "weather_code",
            "snowfall",
            "relative_humidity_2m",
            "sunshine_duration",
            "shortwave_radiation",
            "is_day",
        ],
        "start_date": (
            datetime.datetime.now(tz=pytz.timezone(tz)) + datetime.timedelta(days=day)
        ).strftime("%Y-%m-%d"),
        "end_date": (
            datetime.datetime.now(tz=pytz.timezone(tz))
            + datetime.timedelta(days=day + 1)
        ).strftime("%Y-%m-%d"),
    }
    pyweatherfr.log.print_debug(
        "appel api meteo france "
        + url
        + "?"
        + "&".join(
            [
                f'{key}={",".join(value) if isinstance(value, list) else value}'
                for key, value in params.items()
            ]
        )
    )
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(3).ValuesAsNumpy()
    hourly_wind_gusts_10m = hourly.Variables(4).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(5).ValuesAsNumpy()
    surface_pressure = hourly.Variables(6).ValuesAsNumpy()
    weather_code = hourly.Variables(7).ValuesAsNumpy()
    snowfall = hourly.Variables(8).ValuesAsNumpy()
    relative_humidity_2m = hourly.Variables(9).ValuesAsNumpy()
    sunshine_duration = hourly.Variables(10).ValuesAsNumpy()
    shortwave_radiation = hourly.Variables(11).ValuesAsNumpy()
    alt = response.Elevation()
    isday = hourly.Variables(12).ValuesAsNumpy()
    return (
        hourly_temperature_2m,
        hourly_apparent_temperature,
        hourly_precipitation,
        hourly_wind_speed_10m,
        hourly_wind_gusts_10m,
        hourly_wind_direction_10m,
        surface_pressure,
        weather_code,
        snowfall,
        relative_humidity_2m,
        sunshine_duration,
        shortwave_radiation,
        alt,
        isday,
    )


def cache_session():
    if pyweatherfr.args.compute_args().nocache:
        directory = get_user_config_directory_pyweather()
        file_path = os.path.join(directory, ".cache.sqlite")
        if os.path.exists(file_path):
            os.remove(file_path)
            pyweatherfr.log.print_debug("Le cache a été supprimé avec succès.")
        else:
            pyweatherfr.log.print_debug("Le cache n'existe pas.")
    return requests_cache.CachedSession(
        get_user_config_directory_pyweather() + ".cache", expire_after=3600
    )


def current(latitude, longitude, tz):
    retry_session = retry_requests.retry(cache_session(), retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/meteofrance"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": tz,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "rain",
            "snowfall",
            "weather_code",
            "pressure_msl",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
            "is_day",
            "shortwave_radiation",
        ],
    }
    pyweatherfr.log.print_debug(
        "appel api meteo france "
        + url
        + "?"
        + "&".join(
            [
                f'{key}={",".join(value) if isinstance(value, list) else value}'
                for key, value in params.items()
            ]
        )
    )
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_apparent_temperature = current.Variables(2).Value()
    current_precipitation = current.Variables(4).Value()
    snowfall = current.Variables(5).Value()
    current_weather_code = current.Variables(6).Value()
    current_surface_pressure = current.Variables(7).Value()
    current_wind_speed_10m = current.Variables(8).Value()
    current_wind_direction_10m = current.Variables(9).Value()
    current_wind_gusts_10m = current.Variables(10).Value()
    isday = current.Variables(11).Value()
    altitude = response.Elevation()
    time = int(response.Current().Time())
    shortwave_radiation = current.Variables(12).Value()

    return (
        current_temperature_2m,
        current_apparent_temperature,
        current_relative_humidity_2m,
        current_precipitation,
        current_surface_pressure,
        current_wind_speed_10m,
        current_wind_gusts_10m,
        current_wind_direction_10m,
        current_weather_code,
        snowfall,
        altitude,
        time,
        isday,
        shortwave_radiation,
    )


def get_user_config_directory_pyweather():
    if os.name == "nt":
        appdata = os.getenv("LOCALAPPDATA")
        if appdata:
            ze_path = os.path.join(appdata, DOSSIER_CONFIG_PYWEATHER, "")
            pathlib.Path(ze_path).mkdir(parents=True, exist_ok=True)
            return ze_path
        appdata = os.getenv("APPDATA")
        if appdata:
            ze_path = os.path.join(appdata, DOSSIER_CONFIG_PYWEATHER, "")
            pathlib.Path(ze_path).mkdir(parents=True, exist_ok=True)
            return ze_path
        print(my_colored("erreur : impossible de créer le dossier de config", "red"))
        sys.exit(1)
    xdg_config_home = os.getenv("XDG_CONFIG_HOME")
    if xdg_config_home:
        ze_path = os.path.join(xdg_config_home, "")
        pathlib.Path(ze_path).mkdir(parents=True, exist_ok=True)
        return ze_path
    ze_path = os.path.join(
        os.path.expanduser("~"), ".config", DOSSIER_CONFIG_PYWEATHER, ""
    )
    pathlib.Path(ze_path).mkdir(parents=True, exist_ok=True)
    return ze_path
