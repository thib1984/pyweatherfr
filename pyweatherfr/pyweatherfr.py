"""
pyweatherfr use case
"""

from pyweatherfr.args import compute_args


import datetime
import sys
import requests
import unidecode
import json
import urllib.request
import os
import time
import re
import openmeteo_requests
import requests_cache

import pandas as pd

from columnar import columnar
from termcolor import colored
from pathlib import Path
from retry_requests import retry

incomplete_data = False

DOSSIER_CONFIG_PYWEATHER = "pyweatherfr"

SUN = "\U0001F31E"
MI_SUN = "\U0001F324"
CLOUD = "\U0001F325"
MI_CLOUD_RAIN = "\U0001F326"
RAIN = "\U0001F327"
SNOW = "\U0001F328"
NIGHT_CLEAR = "\U0001F319"
ORAGE = "\U0001F329"
ORAGE_PLUIE = "\U0001F329" + " " + "\U0001F327"
FOG = "\U0001F32B"
DROPLET = "\U0001F4A7"
FLOCON = "\U00002744"
WIND = "\U0001F6A9"
COLD = "\U0001F9CA"
WARM = "\U0001F321"
HOME = "\U0001F3E0"
BOUSSOLE = "\U0001F9ED"
CLOCK = "\U000023F0"
THERMO = "\U0001F321"
HUMIDITE = "\U0001F4A7"
PLUIE = "\U0001F327"
FLECHE_N = "\U0000FE0F"
FLECHE_NW = "\U0000FE0F"
FLECHE_W = "\U0000FE0F"
FLECHE_SW = "\U0000FE0F"
FLECHE_S = "\U0000FE0F"
FLECHE_SE = "\U0000FE0F"
FLECHE_E = "\U0000FE0F"
FLECHE_NE = "\U0000FE0F"
ELEPHANT = "\U0001F418"
PLUME = "\U0001FAB6"
WARNING_WARM=30
WARNING_FROID=0
WARNING_SNOW=0.1
WARNING_RAIN=0.1
WARNING_WIND=30
WARNING_WIND_GUST=50
WARNING_HP=1030
WARNING_BP=990
WARNING_HUMIDITY=90

def get_user_config_directory_pyweather():
    if os.name == "nt":
        appdata = os.getenv("LOCALAPPDATA")
        if appdata:
            ze_path = os.path.join(appdata, DOSSIER_CONFIG_PYWEATHER, "")
            Path(ze_path).mkdir(parents=True, exist_ok=True)
            return ze_path
        appdata = os.getenv("APPDATA")
        if appdata:
            ze_path = os.path.join(appdata, DOSSIER_CONFIG_PYWEATHER, "")
            Path(ze_path).mkdir(parents=True, exist_ok=True)
            return ze_path
        print(my_colored("erreur : impossible de créer le dossier de config", "red"))
        sys.exit(1)
    xdg_config_home = os.getenv("XDG_CONFIG_HOME")
    if xdg_config_home:
        ze_path = os.path.join(xdg_config_home, "")
        Path(ze_path).mkdir(parents=True, exist_ok=True)
        return ze_path
    ze_path = os.path.join(
        os.path.expanduser("~"), ".config", DOSSIER_CONFIG_PYWEATHER, ""
    )
    Path(ze_path).mkdir(parents=True, exist_ok=True)
    return ze_path


def find():

    global incomplete_data
    global is_gps
    incomplete_data = False
    is_gps = False
    doublon_cp = False

    vjson = recuperation_data_villes()

    if compute_args().search:
        search_town(vjson)
    elif compute_args().town:
        url = obtain_url_and_town()
    elif compute_args().post:
        url, doublon_cp = obtain_url_and_town_from_cp(vjson)
    elif compute_args().gps:
        is_gps = True
        url = obtain_url_and_town_from_gps()
    else:
        url = obtain_url_and_town_from_ip()

    print_debug(
        "recherche prévision depuis http://prevision-meteo.ch/services/json/" + url
    )
    r = requests.get("http://prevision-meteo.ch/services/json/" + url)
    if r.json().get("errors"):
        display_error(r)
    if is_gps:
        infos = "(" + url + ")"
        city = "."
    else:
        infos = obtain_info_town(vjson, url, r)
        city = r.json().get("city_info").get("name")
    if compute_args().now:
        previsions_courantes(r, infos, city)
    elif compute_args().jour == -1:
        previsions_generiques(r, infos, city)
    else:
        previsions_detaillees(r, infos, city)
    if incomplete_data == True:
        print(
            my_colored(
                "attention : données incomplètes, vous pouvez essayer une autre ville pour plus de précision",
                "yellow",
            )
        )
    if doublon_cp:
        print(
            my_colored(
                'attention : il existe plusieurs villes associées au code postal. Si besoin, jouez "pyweather -s '
                + compute_args().post
                + '"'
                + " pour trouver la ville souhaitée ",
                "yellow",
            )
        )


def previsions_detaillees(r, infos, city):
    gps, elevation, sunrise, sunset = obtain_data(r)
    print_generic_data_town(infos, city, gps, elevation)
    # Utilisation d'une expression régulière pour extraire les nombres
    matches = re.findall(r"[-+]?\d*\.\d+|\d+", gps)

    # Récupération des deux nombres extraits
    latitude = float(matches[0])
    longitude = float(matches[1])
    (
        hourly_temperature_2m,
        hourly_apparent_temperature,
        hourly_precipitation,
        hourly_wind_speed_10m,
        hourly_wind_gusts_10m,
        hourly_wind_direction_10m,
        surface_pressure,
        current_weather_code,
        snowfall,
        relative_humidity_2m,
        sunshine_duration,
        cloud_cover       
    ) = specific_day(latitude, longitude, compute_args().jour)
    data = []
    for h in range(0, 24):
        warning = ""
        if (
            compute_args().jour == 0
            and 0 < h - int(datetime.datetime.now().strftime("%H")) <= 1
        ):
            warning = warning + " " + CLOCK
        temp = (
            f"{hourly_temperature_2m[h]:.1f}° ({hourly_apparent_temperature[h]:.1f}°)"
        )
        if hourly_temperature_2m[h] <= WARNING_FROID or hourly_apparent_temperature[h] <= WARNING_FROID:
            warning = warning + " " + COLD
        if hourly_temperature_2m[h] >= WARNING_WARM or hourly_apparent_temperature[h] >= WARNING_WARM:
            warning = warning + " " + WARM
        pluie = f"{hourly_precipitation[h]:.1f}mm"
        if snowfall[h] >= WARNING_SNOW:
            warning = warning + " " + SNOW
        elif hourly_precipitation[h] >= WARNING_RAIN:
            warning = warning + " " + RAIN

        vent = (
            f"{hourly_wind_speed_10m[h]:.1f}km/h ({hourly_wind_gusts_10m[h]:.1f}km/h)"
        )
        direction = calculer_direction(hourly_wind_direction_10m[h])

        vent = vent
        if hourly_wind_speed_10m[h] >= WARNING_WIND or hourly_wind_gusts_10m[h] >= WARNING_WIND_GUST:
            warning = warning + " " + WIND

        pression = f"{surface_pressure[h]:.1f}Hpa"
        if surface_pressure[h] >= WARNING_HP:
            warning = warning + " " + ELEPHANT
        if surface_pressure[h] <= WARNING_BP:
            warning = warning + " " + PLUME
        weather, emojiweather = traduction(current_weather_code[h])
        humidity = f"{relative_humidity_2m[h]:.0f}%"
        soleil_nuage = f"{sunshine_duration[h]/60:.0f}% / {cloud_cover[h]:.0f}%"
        if compute_args().nocolor:
            data.append(
                [
                    datetime.datetime.strftime(
                        datetime.datetime.now().replace(
                            hour=0, minute=0, second=0, microsecond=0
                        )
                        + datetime.timedelta(days=compute_args().jour)
                        + datetime.timedelta(hours=h),
                        "%Y-%m-%d %H:%M",
                    ),
                    weather,
                    temp,
                    pluie,
                    vent,
                    direction,
                    pression,
                    humidity,
                    soleil_nuage,
                ]
            )
        else:
            data.append(
                [
                    datetime.datetime.strftime(
                        datetime.datetime.now().replace(
                            hour=0, minute=0, second=0, microsecond=0
                        )
                        + datetime.timedelta(days=compute_args().jour)
                        + datetime.timedelta(hours=h),
                        "%Y-%m-%d %H:%M",
                    ),
                    emojiweather + " " + weather,
                    temp,
                    pluie,
                    vent,
                    direction,
                    pression,
                    humidity,
                    soleil_nuage,
                    warning,
                ]
            )

    if compute_args().nocolor:
        headers = [
            "date",
            "temps",
            "température (ressenties)",
            "précipitations",
            "vent (rafales)",
            "direction",
            "pression",
            "humidité",
            "soleil / nuage"
        ]
    else:
        headers = [
            "date",
            "temps",
            "température (ressenties)",
            "précipitations",
            "vent (rafales)",
            "direction",
            "pression",
            "humidité",
            "soleil / nuage",            
            "warnings",
        ]

    if data != []:
        if compute_args().condensate:
            table = columnar(data, no_borders=True, wrap_max=0)
        else:
            print("")
            table = columnar(data, headers, no_borders=False, wrap_max=0)
        print(table)

def calculer_direction(direction_vent_degres):
    if (
            direction_vent_degres <= 22.5
            or direction_vent_degres >= 360 - 22.5
        ):
        direction = "N"
    if (
            direction_vent_degres <= 360 - 22.5
            and direction_vent_degres > 360 - 22.5 - 45
        ):
        direction = "NO"
    if (
            direction_vent_degres <= 360 - 22.5 - 45
            and direction_vent_degres > 360 - 22.5 - 90
        ):
        direction = "O"
    if (
            direction_vent_degres <= 360 - 22.5 - 90
            and direction_vent_degres > 360 - 22.5 - 135
        ):
        direction = "SO"
    if (
            direction_vent_degres <= 360 - 22.5 - 135
            and direction_vent_degres > 360 - 22.5 - 180
        ):
        direction = "S"
    if (
            direction_vent_degres <= 360 - 22.5 - 180
            and direction_vent_degres > 360 - 22.5 - 225
        ):
        direction = "SE"
    if (
            direction_vent_degres <= 360 - 22.5 - 225
            and direction_vent_degres > 360 - 22.5 - 270
        ):
        direction = "E"
    if (
            direction_vent_degres <= 360 - 22.5 - 270
            and direction_vent_degres > 360 - 22.5 - 315
        ):
        direction = "NE"
    return direction


def traduction(current_weather_code):
    if (
        current_weather_code == 0
        or current_weather_code == 1
        or current_weather_code == 2
    ):
        return ["ciel clair", SUN]
    if current_weather_code >= 3 and current_weather_code <= 12:
        return ["nuageux", CLOUD]
    if current_weather_code >= 13 and current_weather_code <= 19:
        return ["pluie proche", RAIN]
    if current_weather_code >= 20 and current_weather_code <= 29:
        return ["fin de pluie", RAIN]
    if current_weather_code >= 30 and current_weather_code <= 39:
        return ["tempete de poussière, sable ou neige", FOG]
    if current_weather_code >= 40 and current_weather_code <= 49:
        return ["brouillard", FOG]
    if current_weather_code >= 50 and current_weather_code <= 59:
        return ["bruine", RAIN]
    if current_weather_code >= 60 and current_weather_code <= 69:
        return ["pluie", RAIN]
    if current_weather_code >= 70 and current_weather_code <= 79:
        return ["neige", SNOW]
    if current_weather_code >= 80 and current_weather_code <= 99:
        return ["averse / orage", ORAGE_PLUIE]


def previsions_courantes(r, infos, city):
    gps, elevation, sunrise, sunset = obtain_data(r)
    print_generic_data_town(infos, city, gps, elevation)

    matches = re.findall(r"[-+]?\d*\.\d+|\d+", gps)
    latitude = float(matches[0])
    longitude = float(matches[1])

    (
        current_temperature_2m,
        current_apparent_temperature,
        current_relative_humidity_2m,
        current_precipitation,
        current_surface_pressure,
        current_wind_speed_10m,
        current_wind_gusts_10m,
        current_wind_direction_10m,
        current_weather_code,
        snowfall

    ) = current(latitude, longitude)
    current_weather, emojiweather = traduction(current_weather_code)
    data = []
    direction = calculer_direction(current_wind_direction_10m)

    if compute_args().nocolor:
        data.append(
            [
                "température",
                f"{current_temperature_2m:.1f}° ({current_apparent_temperature:.1f}°)",
            ]
        )
        data.append(["humidité", f"{current_relative_humidity_2m:.1f}%"])
        data.append(["precipitation", f"{current_precipitation:.1f}mm"])
        data.append(["pression", f"{current_surface_pressure:.1f}Hp"])
        data.append(
            [
                "vent",
                f"{current_wind_speed_10m:.1f}km/h ({current_wind_gusts_10m:.1f}km/h) - "
                + direction,
            ]
        )
        data.append(["temps", current_weather])

    else:
        if current_temperature_2m >= WARNING_WARM or current_apparent_temperature >= WARNING_WARM:
            data.append(
                [
                    "température",
                    f"{current_temperature_2m:.1f}° ({current_apparent_temperature:.1f}°)",
                    WARM,
                ]
            )
        else:
            data.append(
                [
                    "température",
                    f"{current_temperature_2m:.1f}° ({current_apparent_temperature:.1f}°)",
                    "",
                ]
            )
        if current_relative_humidity_2m >= WARNING_HUMIDITY:
            data.append(["humidité", f"{current_relative_humidity_2m:.1f}%", DROPLET])
        else:
            data.append(["humidité", f"{current_relative_humidity_2m:.1f}%", ""])
        if snowfall >= WARNING_SNOW:
            data.append(["precipitation", f"{current_precipitation:.1f}mm", SNOW])
        elif current_precipitation>=WARNING_RAIN:
            data.append(["precipitation", f"{current_precipitation:.1f}mm", RAIN])
        else:
            data.append(["precipitation", f"{current_precipitation:.1f}mm", RAIN])
        if current_surface_pressure >= WARNING_HP:
            data.append(["pression", f"{current_surface_pressure:.1f}Hp", ELEPHANT])
        elif current_surface_pressure <= WARNING_BP:
            data.append(["pression", f"{current_surface_pressure:.1f}Hp", PLUME])
        else:
            data.append(["pression", f"{current_surface_pressure:.1f}Hp", ""])
        if current_wind_speed_10m >= WARNING_WIND or current_wind_gusts_10m >= WARNING_WIND_GUST:
            data.append(
                [
                    "vent",
                    f"{current_wind_speed_10m:.1f}km/h ({current_wind_gusts_10m:.1f}km/h) - "
                    + direction,
                    WIND,
                ]
            )
        else:
            data.append(
                [
                    "vent",
                    f"{current_wind_speed_10m:.1f}km/h ({current_wind_gusts_10m:.1f}km/h) - "
                    + direction,
                    "",
                ]
            )
        data.append(["temps", emojiweather + " " + current_weather, ""])
    if compute_args().condensate:
        table = columnar(data, no_borders=True, wrap_max=0)
    else:
        print("")
        table = columnar(data, no_borders=False, wrap_max=0)
    print(table)


def previsions_generiques(r, infos, city):
    gps, elevation, sunrise, sunset = obtain_data(r)

    print_generic_data_town(infos, city, gps, elevation)

    matches = re.findall(r"[-+]?\d*\.\d+|\d+", gps)
    latitude = float(matches[0])
    longitude = float(matches[1])

    (
        date_debut,
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
    ) = resume(latitude, longitude)
    data2 = []
    for i in [0, 1, 2, 3]:
        warning = ""
        pluie = f"{daily_precipitation_sum[i]:.1f}mm"
        if snowfall[i] >= WARNING_SNOW:
            warning = warning + " " + SNOW
        elif daily_precipitation_sum[i] >= WARNING_RAIN:
            warning = warning + " " + RAIN
        temp = f"{daily_temperature_2m_min[i]:.1f}° ({daily_apparent_temperature_min[i]:.1f}°) -> {daily_temperature_2m_max[i]:.1f}° ({daily_apparent_temperature_max[i]:.1f}°)"
        if (
            daily_temperature_2m_min[i] <= WARNING_FROID
            or daily_apparent_temperature_min[i] <= WARNING_FROID
            or daily_temperature_2m_max[i] <= WARNING_FROID
            or daily_apparent_temperature_max[i] <= WARNING_FROID
        ):
            warning = warning + " " + COLD
        if (
            daily_temperature_2m_min[i] >= WARNING_WARM
            or daily_apparent_temperature_min[i] >= WARNING_WARM
            or daily_temperature_2m_max[i] >= WARNING_WARM
            or daily_apparent_temperature_max[i] >= WARNING_WARM
        ):
            warning = warning + " " + WARM
        weather, emojiweather = traduction(weather_code[i])

        vent = f"{daily_wind_speed_10m_max[i]:.1f}km/h ({daily_wind_gusts_10m_max[i]:.1f}km/h)"
        direction=calculer_direction(daily_wind_direction_10m_dominant[i])


        vent = vent
        if daily_wind_speed_10m_max[i] >= WARNING_WIND or daily_wind_gusts_10m_max[i] >= WARNING_WIND_GUST:
            warning = warning + " " + WIND
        duree = f"{precipitation_hours[i]:.0f}h / {sunshine_duration[i]/3600:.0f}h"
        if compute_args().nocolor:
            data2.append(
                [
                    datetime.datetime.strftime(
                        datetime.datetime.now().replace(
                            hour=0, minute=0, second=0, microsecond=0
                        )
                        + datetime.timedelta(hours=24 * i),
                        "%Y-%m-%d",
                    ),
                    weather,
                    temp,
                    pluie,
                    vent,
                    direction,
                    duree
                ]
            )
            headers = [
                "date",
                "temps",
                "température",
                "précipitations",
                "vent (rafales)",
                "direction",
                "pluie/soleil"
            ]
        else:
            data2.append(
                [
                    datetime.datetime.strftime(
                        datetime.datetime.now().replace(
                            hour=0, minute=0, second=0, microsecond=0
                        )
                        + datetime.timedelta(hours=24 * i),
                        "%Y-%m-%d",
                    ),
                    emojiweather + " " + weather,
                    temp,
                    pluie,
                    vent,
                    direction,
                    duree,
                    warning,
                ]
            )
            headers = [
                "date",
                "temps",
                "température",
                "précipitations",
                "vent (rafales)",
                "direction",
                "pluie/soleil",
                "warning",
            ]

    if data2 != []:
        if compute_args().condensate:
            table = columnar(data2, no_borders=True, wrap_max=0)
        else:
            print("")
            table = columnar(data2, headers, no_borders=False, wrap_max=0)
        print(table)


def print_generic_data_town(infos, city, gps, elevation):
    print("")

    data = []
    if compute_args().nocolor:
        data.append([re.sub(" \([0-9]+\)", "", city) + " " + infos])
        data.append([gps + " / alt. " + elevation])
        data.append([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    else:
        data.append([HOME, re.sub(" \([0-9]+\)", "", city) + " " + infos])
        data.append([BOUSSOLE, gps + " / alt. " + elevation])
        data.append([CLOCK, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    if compute_args().condensate:
        table = columnar(data, no_borders=True, wrap_max=0)
    else:
        table = columnar(data, no_borders=False, wrap_max=0)

    print(table)


def obtain_data(r):
    gps = (
        "lat. "
        + str(round(float(r.json().get("city_info").get("latitude")), 5))
        + " / long. "
        + str(round(float(r.json().get("city_info").get("longitude")), 5))
    )
    if not is_gps:
        elevation = valueorNA(r.json().get("city_info").get("elevation")) + "m"
    else:
        elevation = valueorNA(r.json().get("forecast_info").get("elevation")) + "m"
    sunrise = valueorNA(r.json().get("city_info").get("sunrise"))
    sunset = valueorNA(r.json().get("city_info").get("sunset"))
    return gps, elevation, sunrise, sunset


def obtain_info_town(vjson, url, r):
    print_debug(
        "recherche informations de la VILLE depuis https://www.prevision-meteo.ch/services/json/list-cities"
    )
    try:
        i = 0
        while True:
            if (
                vjson.get(str(i)).get("country") is not None
                and vjson.get(str(i)).get("country") == "FRA"
            ):
                if unidecode.unidecode(url.lower()) == unidecode.unidecode(
                    vjson.get(str(i)).get("url").lower()
                ):
                    npa = vjson.get(str(i)).get("npa")
                    print_debug("CODE_POSTAL : " + npa)
                    infos = "(" + npa + ")"
                    break
            i = i + 1
            infos = ""
        return infos
    except Exception:
        print(my_colored("erreur : la VILLE n'est pas en France", "red"))
        print(
            my_colored(
                "essayez de trouver un paramètre correct avec \"pyweatherfr -s '"
                + compute_args().town
                + "'\"",
                "yellow",
            )
        )
        sys.exit(1)


def display_error(r):
    print(my_colored("erreur : pas de données trouvées", "red"))
    print_debug(r.json().get("errors")[0].get("code"))
    print_debug(r.json().get("errors")[0].get("text"))
    print_debug(r.json().get("errors")[0].get("description"))
    if compute_args().town or compute_args().post:
        print(
            my_colored(
                "essayez de trouver un paramètre correct avec \"pyweatherfr -s '"
                + compute_args().town
                + "'\"",
                "yellow",
            )
        )
    else:
        print(
            my_colored(
                'essayez avec le lancement classique "pyweatherfr [VILLE]"',
                "yellow",
            )
        )
    exit(1)


def obtain_url_and_town_from_ip():
    global is_gps
    with urllib.request.urlopen("https://geolocation-db.com/json") as url:
        print_debug(
            "recherche de la localisation depuis https://geolocation-db.com/json"
        )
        data = json.loads(url.read().decode())
        print_debug(str(data))
        town = data["city"]
        if town is None:
            print(
                my_colored(
                    "attention : pas de ville trouvée avec l'ip, utilisation des coordonnées GPS...",
                    "yellow",
                )
            )
            print_debug(
                "COORDONNEES_GPS :"
                + "latitude="
                + str(data["latitude"])
                + " longitude="
                + str(data["longitude"])
            )
            is_gps = True
            url = "lat=" + str(data["latitude"]) + "lng=" + str(data["longitude"])
            print_debug("URL : " + url)
        else:
            url = town
            print_debug("URL : " + url)
    return url


def obtain_url_and_town_from_gps():
    print_debug(
        "COORDONNEES_GPS :"
        + "latitude="
        + str(compute_args().gps[0])
        + " longitude="
        + str(compute_args().gps[1])
    )
    url = "lat=" + compute_args().gps[0] + "lng=" + compute_args().gps[1]
    print_debug("URL : " + url)
    return url


def obtain_url_and_town_from_cp(vjson):
    post = compute_args().post.zfill(5)
    print_debug("CODE_POSTAL : " + str(post))
    print_debug(
        "recherche de la VILLE et de l'URL depuis https://www.prevision-meteo.ch/services/json/list-cities"
    )
    i = 0
    try:
        trouve = False
        doublon = False
        while True:
            if (
                vjson.get(str(i)).get("country") is not None
                and vjson.get(str(i)).get("country") == "FRA"
            ):
                if str(post) == vjson.get(str(i)).get("npa"):
                    if not trouve:
                        url = vjson.get(str(i)).get("url")
                        print_debug("URL : " + url)
                    if trouve:
                        doublon = True
                    trouve = True
            i = i + 1
    except Exception:
        if not trouve:
            print(
                my_colored(
                    "erreur : pas de ville trouvée avec le code postal " + str(post),
                    "red",
                )
            )
            print(
                my_colored(
                    "essayez avec un autre code postal, ou avec le code postal principal de la ville",
                    "yellow",
                )
            )
            sys.exit(1)
    return url, doublon


def obtain_url_and_town():
    url = unidecode.unidecode(compute_args().town.lower()).replace(" ", "-")
    print_debug("URL : " + url)
    return url


def search_town(vjson):
    search = compute_args().search
    print_debug(
        "recherche de la ville depuis https://www.prevision-meteo.ch/services/json/list-cities"
    )
    trouve = False
    i = 0
    try:
        while True:
            if (
                vjson.get(str(i)).get("country") is not None
                and vjson.get(str(i)).get("country") == "FRA"
            ):
                name = re.sub(" \([0-9]+\)", "", vjson.get(str(i)).get("name")).replace(
                    " ", "-"
                )
                npa = vjson.get(str(i)).get("npa")
                url = vjson.get(str(i)).get("url")
                if (
                    str(search) == npa
                    or unidecode.unidecode(search.lower()).replace(" ", "-")
                    in unidecode.unidecode(name.lower().replace(" ", "-"))
                    or unidecode.unidecode(name.lower().replace(" ", "-"))
                    in unidecode.unidecode(search.lower().replace(" ", "-"))
                ):
                    trouve = True
                    print(
                        my_colored(
                            "pour "
                            + name
                            + " ("
                            + npa
                            + "), exécutez 'pyweatherfr "
                            + url
                            + "' or 'pyweatherfr -p "
                            + npa
                            + "'",
                            "yellow",
                        )
                    )
            i = i + 1
    except Exception:
        if not trouve:
            print(my_colored("erreur : pas de ville trouvée", "red"))
        sys.exit(1)


def recuperation_data_villes():
    tmp_json = "villes.json"
    if (
        compute_args().cache
        or not os.path.exists(get_user_config_directory_pyweather() + tmp_json)
        or (
            time.time()
            - os.stat(get_user_config_directory_pyweather() + tmp_json).st_mtime
            > 86400 * 30
        )
    ):
        print(
            my_colored(
                "cache des villes absent, expiré ou reset, en cours de téléchargement...",
                "yellow",
            )
        )
        vjson = requests.get(
            "https://www.prevision-meteo.ch/services/json/list-cities"
        ).json()
        print_debug(
            "enregistrement du cache dans "
            + get_user_config_directory_pyweather()
            + tmp_json
        )
        with open(get_user_config_directory_pyweather() + tmp_json, "w") as f:
            json.dump(vjson, f)
    else:
        print_debug(
            "recupération du cache depuis "
            + get_user_config_directory_pyweather()
            + tmp_json
        )
        with open(get_user_config_directory_pyweather() + tmp_json, "r") as f:
            vjson = json.load(f)
    return vjson


def my_colored(message, color):
    if compute_args().nocolor:
        return message
    return colored(message, color)


def print_debug(message):
    if compute_args().verbose:
        print("debug : " + message)


def valueorNA(my_string):
    global incomplete_data
    if my_string is None or my_string == "NA":
        incomplete_data = True
        return "."
    return my_string


def resume(latitude, longitude):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(
        get_user_config_directory_pyweather() + ".cache", expire_after=3600
    )
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/meteofrance"
    params = {
        "timezone": "Europe/Paris",
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
            "sunshine_duration"
        ],
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process daily data. The order of variables needs to be the same as requested.
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
    precipitation_hours= daily.Variables(10).ValuesAsNumpy()
    sunshine_duration= daily.Variables(11).ValuesAsNumpy()
    date_debut = pd.to_datetime(daily.Time(), unit="s", utc=True)
    return (
        date_debut,
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
        sunshine_duration
    )


def specific_day(latitude, longitude, day):
    cache_session = requests_cache.CachedSession(
        get_user_config_directory_pyweather() + ".cache", expire_after=3600
    )
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = "https://api.open-meteo.com/v1/meteofrance"
    params = {
        "timezone": "Europe/Paris",
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
            "cloud_cover" 
        ],
        "start_date": (datetime.datetime.now() + datetime.timedelta(days=day)).strftime(
            "%Y-%m-%d"
        ),
        "end_date": (
            datetime.datetime.now() + datetime.timedelta(days=day + 1)
        ).strftime("%Y-%m-%d"),
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process daily data. The order of variables needs to be the same as requested.
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
    cloud_cover = hourly.Variables(11).ValuesAsNumpy()
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
        cloud_cover
                )


def current(latitude, longitude):
    cache_session = requests_cache.CachedSession(
        get_user_config_directory_pyweather() + ".cache", expire_after=3600
    )
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/meteofrance"
    params = {
        "latitude": latitude,
        "longitude": longitude,
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
        ],
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_apparent_temperature = current.Variables(2).Value()
    current_precipitation = current.Variables(4).Value()
    snowfall=current.Variables(5).Value()
    current_weather_code = current.Variables(6).Value()
    current_surface_pressure = current.Variables(7).Value()
    current_wind_speed_10m = current.Variables(8).Value()
    current_wind_direction_10m = current.Variables(9).Value()
    current_wind_gusts_10m = current.Variables(10).Value()

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
        snowfall
    )
