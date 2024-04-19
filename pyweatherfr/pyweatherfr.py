"""
pyweatherfr use case
"""


from pyweatherfr.args import compute_args

import unicodedata
import geopy
import certifi
import ssl
import datetime
import sys
import json
import urllib.request
import os
import openmeteo_requests
import requests_cache
import columnar
import termcolor
import pathlib
import retry_requests
import geopy
import timezonefinder
import pytz
import tzlocal
import numpy


DOSSIER_CONFIG_PYWEATHER = "pyweatherfr"

SUN = "\U0001F31E"
MI_SUN = "\U0001F324"
CLOUD = "\U0001F325"
NIGHT_CLOUD = "\U0001f319"
MI_CLOUD_RAIN = "\U0001F326"
RAIN = "\U0001F327"
SNOW = "\U0001F328"
NIGHT_CLEAR = "\U0001f319"
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

FLECHE_N = "\U00002193"
FLECHE_NO = "\U00002198"
FLECHE_O = "\U00002192"
FLECHE_SO = "\U00002197"
FLECHE_S = "\U00002191"
FLECHE_SE = "\U00002196"
FLECHE_E = "\U00002190"
FLECHE_NE = "\U00002199"

ELEPHANT = "\U0001F418"
PLUME = "\U0001FAB6"
PC ="\U0001f4bb"
LUNETTES= "\U0001F60E"
WARNING_WARM=30
WARNING_FROID=0
WARNING_SNOW=0.1
WARNING_RAIN=0.1
WARNING_WIND=30
WARNING_WIND_GUST=50
WARNING_HP=1030
WARNING_BP=995
WARNING_HUMIDITY=90

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


def diff_jour(long,lat):
    tz=timezonefinder.TimezoneFinder().timezone_at(lng=float(long), lat=float(lat))
    if not compute_args().date is None:
        if not est_format_date(compute_args().date):
            print(my_colored("erreur : format date invalide, format attendu yyyy-mm-dd", "red"))
            exit(1)
        diff = (pytz.timezone(tz).localize(datetime.datetime.strptime(compute_args().date, "%Y-%m-%d")) - datetime.datetime.now(tz=pytz.timezone(tz))).days +1
        print_debug(str(diff) + " jours")
        if diff>=15:
            print(my_colored("erreur : date invalide (limitée à +14 jour de la date actuelle)", "red"))
            exit(1)
        return diff
    if compute_args().jour>=15:
        print(my_colored("erreur : date invalide (limitée à +14 jour de la date actuelle)", "red"))
        exit(1)                 
    return compute_args().jour

def est_format_date(chaine):
    try:
        datetime.datetime.strptime(chaine, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def find():
    if compute_args().town:
        ville, dpt, lat, long,country = obtain_city_data()
    elif compute_args().gps:
        ville, dpt, lat, long,country = obtain_city_data_from_gps()
    else:
        ville, dpt, lat, long,country = obtain_city_data_from_ip()
    tz=timezonefinder.TimezoneFinder().timezone_at(lng=float(long), lat=float(lat))
    if compute_args().pc:
        tz=str(tzlocal.get_localzone())
    if compute_args().utc:
        tz=str(pytz.utc)              
    print_debug(tz)
    if compute_args().now:
        previsions_courantes(ville, dpt, lat, long,tz)
    elif not compute_args().date is None:
        previsions_detaillees(ville, dpt, lat, long,tz)        
    elif compute_args().jour is None:
        previsions_generiques(ville, dpt, lat, long,tz)
    else:
        previsions_detaillees(ville, dpt, lat, long,tz)
    if not compute_args().town and not compute_args().gps:   
        print(my_colored("warning : si vous utilisez un proxy ou un VPN, la localisation peut être incorrecte", "yellow"))
    if country is None:
        print(my_colored("warning : ville potentiellement hors de France, les prévisions et données peuvent être moins précises", "yellow"))
    elif  country!="France":
        print(my_colored("warning : ville hors de France, les prévisions et données peuvent être moins précises", "yellow"))


def previsions_detaillees(ville, dpt, lat, long, tz):


    
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
        shortwave_radiation,
        alt,
        isday   
    ) = specific_day(lat, long, diff_jour(long,lat), tz)
    recap ="Prévisions détaillées pour le " + (datetime.datetime.now(tz=pytz.timezone(tz)) + datetime.timedelta(days=diff_jour(long,lat))).strftime(
            "%Y-%m-%d")
    if compute_args().pc:
        recap = recap + " (pc)"
    elif compute_args().utc:
        recap = recap + " (utc.)"        
    else:
        recap = recap + " (loc.)"    
    if diff_jour(long,lat)<0:
        recap ="Données détaillées pour le " + (datetime.datetime.now(tz=pytz.timezone(tz)) + datetime.timedelta(days=diff_jour(long,lat))).strftime(
                "%Y-%m-%d")        
    print_generic_data_town(ville, dpt, lat, long, alt, recap)
    data = []
    new_var = diff_jour(long,lat)
    for h in range(0, 24):
        if numpy.isnan(hourly_temperature_2m[h]):
            print(my_colored("warning : pas de données pour ce jour", "yellow"))
            exit(1)
        warning = ""
        if (
            (datetime.datetime.now(tz=pytz.timezone(tz)) + datetime.timedelta(days=new_var)).strftime(
            "%Y-%m-%d") == datetime.datetime.now(tz=pytz.timezone(tz)).strftime("%Y-%m-%d")
            and 0 < h - int(datetime.datetime.now(tz=pytz.timezone(tz)).strftime("%H")) <= 1
        ):
            warning = warning + " " + CLOCK
        temp = (
            f"{hourly_temperature_2m[h]:.1f}°C ({hourly_apparent_temperature[h]:.1f}°C)"
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
        weather, emojiweather = traduction(current_weather_code[h],isday[h])
        humidity = f"{relative_humidity_2m[h]:.0f}%"
        duree_soleil = f"{sunshine_duration[h]/60:.0f}'"
        rayonnement = f" {shortwave_radiation[h]:.0f}W/m\u00B2" 
        if shortwave_radiation[h]>1000:
            warning = warning + " " + LUNETTES   
        if compute_args().nocolor:
            data.append(
                [
                    datetime.datetime.strftime(
                        datetime.datetime.now(tz=pytz.timezone(tz)).replace(
                            hour=0, minute=0, second=0, microsecond=0
                        )
                        + datetime.timedelta(days=new_var)
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
                    rayonnement,
                ]
            )
        else:
            data.append(
                [
                    datetime.datetime.strftime(
                        datetime.datetime.now(tz=pytz.timezone(tz)).replace(
                            hour=0, minute=0, second=0, microsecond=0
                        )
                        + datetime.timedelta(days=new_var)
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
                    rayonnement,
                    warning,
                ]
            )

    if compute_args().nocolor:
        headers = [
            "date",
            "temps",
            "température (ressentie)",
            "pluie",
            "vent (rafales)",
            "dir.",
            "pression",
            "humidité",
            "rayonnement"            
        ]
    else:
        headers = [
            "date",
            "temps",
            "température (ressentie)",
            "pluie",
            "vent (rafales)",
            "dir.",
            "pression",
            "humidité",
            "rayonnement",            
            "warnings",
        ]

    if data != []:
        print("")
        table = columnar.columnar(data, headers, no_borders=False, wrap_max=0)
        print(table)

def calculer_direction(direction_vent_degres):
    if (
            direction_vent_degres <= 22.5
            or direction_vent_degres >= 360 - 22.5
        ):
        direction = "N  "
        if not compute_args().nocolor:
            direction=direction+FLECHE_N        
    if (
            direction_vent_degres <= 360 - 22.5
            and direction_vent_degres > 360 - 22.5 - 45
        ):
        direction = "NO "
        if not compute_args().nocolor:
            direction=direction+FLECHE_NO        
    if (
            direction_vent_degres <= 360 - 22.5 - 45
            and direction_vent_degres > 360 - 22.5 - 90
        ):
        direction = "O  "
        if not compute_args().nocolor:
            direction=direction+FLECHE_O        
    if (
            direction_vent_degres <= 360 - 22.5 - 90
            and direction_vent_degres > 360 - 22.5 - 135
        ):
        direction = "SO "
        if not compute_args().nocolor:
            direction=direction+FLECHE_SO        
    if (
            direction_vent_degres <= 360 - 22.5 - 135
            and direction_vent_degres > 360 - 22.5 - 180
        ):
        direction = "S  "
        if not compute_args().nocolor:
            direction=direction+FLECHE_S        
    if (
            direction_vent_degres <= 360 - 22.5 - 180
            and direction_vent_degres > 360 - 22.5 - 225
        ):
        direction = "SE "
        if not compute_args().nocolor:
            direction=direction+FLECHE_SE        
    if (
            direction_vent_degres <= 360 - 22.5 - 225
            and direction_vent_degres > 360 - 22.5 - 270
        ):
        direction = "E  "
        if not compute_args().nocolor:
            direction=direction+FLECHE_E        
    if (
            direction_vent_degres <= 360 - 22.5 - 270
            and direction_vent_degres > 360 - 22.5 - 315
        ):
        direction = "NE "
        if not compute_args().nocolor:
            direction=direction+FLECHE_NE
    return direction


def traduction(current_weather_code,jour):
    if (
        current_weather_code == 0
        or current_weather_code == 1
        or current_weather_code == 2
    ):
        if jour==0:
            return ["nuit claire ", NIGHT_CLEAR]
        return ["ciel clair ", SUN]
    if current_weather_code >= 3 and current_weather_code <= 12:
        if jour==0:
            return ["nuageux ", NIGHT_CLOUD]        
        return ["nuageux", CLOUD]
    if current_weather_code >= 13 and current_weather_code <= 19:
        return ["pluie proche", RAIN]
    if current_weather_code >= 20 and current_weather_code <= 29:
        return ["fin de pluie", RAIN]
    if current_weather_code >= 30 and current_weather_code <= 39:
        return ["tempete", FOG]
    if current_weather_code >= 40 and current_weather_code <= 49:
        return ["brouillard", FOG]
    if current_weather_code >= 50 and current_weather_code <= 59:
        return ["bruine", RAIN]
    if current_weather_code >= 60 and current_weather_code <= 69:
        return ["pluie", RAIN]
    if current_weather_code >= 70 and current_weather_code <= 79:
        return ["neige", SNOW]
    if current_weather_code >= 80 and current_weather_code <= 99:
        return ["averse-orage", ORAGE_PLUIE]
    return ["", ""]

def previsions_courantes(ville, dpt, lat, long, tz):
    

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
        snowfall,
        alt,
        time,
        isday,
        w_soleil

    ) = current(lat, long, tz)
    recap = "Données courantes mesurées à " + datetime.datetime.fromtimestamp(time,tz=pytz.timezone(tz)).strftime('%Y-%m-%d %H:%M') 
    if compute_args().pc:
        recap = recap + " (pc)"
    elif compute_args().utc:
        recap = recap + " (utc.)"        
    else:
        recap = recap + " (loc.)"
    print_generic_data_town(ville, dpt, lat, long, alt, recap)
    current_weather, emojiweather = traduction(current_weather_code,isday)
    data = []
    direction = calculer_direction(current_wind_direction_10m)

    if compute_args().nocolor:
        data.append(
            [
                "température (ressentie)",
                f"{current_temperature_2m:.1f}°C ({current_apparent_temperature:.1f}°C)",
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
        data.append(["rayonnement", f"{w_soleil:.0f}W/m\u00B2"])
        data.append(["temps", current_weather])

    else:
        if current_temperature_2m >= WARNING_WARM or current_apparent_temperature >= WARNING_WARM:
            data.append(
                [
                    "température (ressentie)",
                    f"{current_temperature_2m:.1f}°C ({current_apparent_temperature:.1f}°C)",
                    WARM,
                ]
            )
        else:
            data.append(
                [
                    "température",
                    f"{current_temperature_2m:.1f}°C ({current_apparent_temperature:.1f}°C)",
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
            data.append(["precipitation", f"{current_precipitation:.1f}mm", ""])
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
        if w_soleil>1000:
            data.append(["rayonnement", f"{w_soleil:.0f}W/m\u00B2",LUNETTES]) 
        else:      
            data.append(["rayonnement", f"{w_soleil:.0f}W/m\u00B2",""]) 
        data.append(["temps", emojiweather + " " + current_weather, ""])
    print("")
    table = columnar.columnar(data, no_borders=False, wrap_max=0)
    print(table)


def previsions_generiques(ville, dpt, lat, long, tz):

    
    (
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
        fin
    ) = resume(lat, long, tz)
    datetime.datetime.fromtimestamp(debut,tz=pytz.timezone(tz)).strftime('%Y-%m-%d')
    recap = "Prévisions génériques du " + datetime.datetime.fromtimestamp(debut,tz=pytz.timezone(tz)).strftime('%Y-%m-%d') + " au " + (datetime.datetime.fromtimestamp(fin,tz=pytz.timezone(tz))+ datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
    if compute_args().past!=0:
        recap = "Données génériques du " + datetime.datetime.fromtimestamp(debut,tz=pytz.timezone(tz)).strftime('%Y-%m-%d') + " au " + (datetime.datetime.fromtimestamp(fin,tz=pytz.timezone(tz))+ datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
    if compute_args().pc:
        recap = recap + " (pc)"
    elif compute_args().utc:
        recap = recap + " (utc.)"        
    else:
        recap = recap + " (loc.)"  
    print_generic_data_town(ville, dpt, lat, long, alt, recap)
    data = []
    fin = 3
    if compute_args().past!=0:
        fin=-1
    tronque=False    
    for i in range(0,len(daily_precipitation_sum)):
        if not numpy.isnan(daily_precipitation_sum[i]):
            warning = ""
            pluie = f"{daily_precipitation_sum[i]:.1f}mm"
            if snowfall[i] >= WARNING_SNOW:
                warning = warning + " " + SNOW
            elif daily_precipitation_sum[i] >= WARNING_RAIN:
                warning = warning + " " + RAIN
            if os.get_terminal_size().columns > 140:    
                temp = f"{daily_temperature_2m_min[i]:.1f}°C ({daily_apparent_temperature_min[i]:.1f}°C) -> {daily_temperature_2m_max[i]:.1f}°C ({daily_apparent_temperature_max[i]:.1f}°C)"
            else:
                temp = f"{daily_temperature_2m_min[i]:.0f}°C -> {daily_temperature_2m_max[i]:.0f}°C"
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
            weather, emojiweather = traduction(weather_code[i],1)

            vent = f"{daily_wind_speed_10m_max[i]:.0f}km/h ({daily_wind_gusts_10m_max[i]:.0f}km/h)"
            direction=calculer_direction(daily_wind_direction_10m_dominant[i])


            vent = vent
            if daily_wind_speed_10m_max[i] >= WARNING_WIND or daily_wind_gusts_10m_max[i] >= WARNING_WIND_GUST:
                warning = warning + " " + WIND
            duree_pluie = f"{precipitation_hours[i]:.0f}h"
            duree_soleil = f"{sunshine_duration[i]/3600:.1f}h"
            if compute_args().nocolor:
                if os.get_terminal_size().columns > 140:
                    data.append(
                        [
                            datetime.datetime.strftime(
                                datetime.datetime.now(tz=pytz.timezone(tz)).replace(
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
                            duree_pluie,
                            duree_soleil
                        ]
                    )
                else:
                    data.append(
                        [
                            datetime.datetime.strftime(
                                datetime.datetime.now(tz=pytz.timezone(tz)).replace(
                                    hour=0, minute=0, second=0, microsecond=0
                                )
                                + datetime.timedelta(hours=24 * i),
                                "%y-%m-%d",
                            ),
                            weather,
                            temp,
                            pluie,
                            vent,
                            direction
                        ]
                    )
            else:
                if os.get_terminal_size().columns > 140:

                    data.append(
                        [
                            datetime.datetime.strftime(
                                datetime.datetime.now(tz=pytz.timezone(tz)).replace(
                                    hour=0, minute=0, second=0, microsecond=0
                                )
                                + datetime.timedelta(hours=24 * i)
                                + datetime.timedelta(days=-1*compute_args().past),
                                "%Y-%m-%d",
                            ),
                            emojiweather + " " + weather,
                            temp,
                            pluie,
                            vent,
                            direction,
                            duree_pluie,
                            duree_soleil,
                            warning,
                        ]
                    )
                else:
                    data.append(
                        [
                            datetime.datetime.strftime(
                                datetime.datetime.now(tz=pytz.timezone(tz)).replace(
                                    hour=0, minute=0, second=0, microsecond=0
                                )
                                + datetime.timedelta(hours=24 * i)
                                + datetime.timedelta(days=-1*compute_args().past),
                                "%y-%m-%d",
                            ),
                            emojiweather + " " + weather,
                            temp,
                            pluie,
                            vent,
                            direction,
                            warning,
                        ]
                    )
        else:
            tronque=True
    if data != []:
        if compute_args().nocolor:
            if os.get_terminal_size().columns > 140:
            
                headers = [
                    "date",
                    "temps",
                    "température (ressentie)",
                    "pluie",
                    "vent (rafales)",
                    "direction",
                    "tps pluie",
                    "tps soleil"
                ]
            else:
                headers = [
                    "date",
                    "temps",
                    "température",
                    "pluie",
                    "vent (rafales)",
                    "direction"
                ]                
        else:
            if os.get_terminal_size().columns > 140:

                headers = [
                    "date",
                    "temps",
                    "température (ressentie)",
                    "pluie",
                    "vent (rafales)",
                    "dir.",
                    "tps pluie",
                    "tps soleil",
                    "",
                ]
            else:
                                headers = [
                    "date",
                    "temps",
                    "température",
                    "pluie",
                    "vent (rafales)",
                    "dir.",
                    "",
                ]


        print("")
        table = columnar.columnar(data, headers, no_borders=False, wrap_max=0)
        print(table)
        if not os.get_terminal_size().columns > 140:
            print(my_colored("warning : pour + d'affichage, élargissez votre terminal", "yellow"))

    if tronque:
        print(my_colored("warning : données tronquées", "yellow"))

def print_generic_data_town(ville, dpt, lat, long, alt, recap):
    print("")

    data = []
    if compute_args().nocolor:
        if (ville is None or ville == "") and (dpt is None or dpt == ""):
            print_debug("pas de data pour ville/dpt/cp")
        elif dpt is None or dpt == "":
            data.append([ville])
        else:    
            data.append([ville + " (" + dpt + ")"])
        data.append([f"lat.:  {float(lat):.4f}° / long.: {float(long):.4f}° / alt.: {float(alt):.0f}m "])
        data.append([recap])
    else:
        if (ville is None or ville == "") and (dpt is None or dpt == ""):
            print_debug("pas de data pour ville/dpt/cp")
        elif dpt is None or dpt == "":
            data.append([HOME, ville])
        else:    
            data.append([HOME, ville + " (" + dpt + ")"])
        data.append([BOUSSOLE, f"lat.:  {float(lat):.4f}°  / long.: {float(long):.4f}° / alt.: {float(alt):.0f}m "])
        data.append([PC,recap])


    table = columnar.columnar(data, no_borders=False, wrap_max=0)

    print(table)


def display_error(r):
    print(my_colored("erreur : pas de données trouvées", "red"))
    print_debug(r.json().get("errors")[0].get("code"))
    print_debug(r.json().get("errors")[0].get("text"))
    print_debug(r.json().get("errors")[0].get("description"))
    if compute_args().town:
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


def obtain_city_data_from_ip():

    with urllib.request.urlopen("https://geolocation-db.com/json") as url:
        print_debug(
            "recherche de la localisation depuis https://geolocation-db.com/json"
        )
        resultat= url.read().decode()
        print_debug(resultat)
        data = json.loads(resultat)
        print_debug(str(json.dumps(data, indent=4,ensure_ascii=False)))
        ville = data["city"]
        if ville is None:
            ville=""
        lat = str(data["latitude"])
        long = str(data["longitude"])
        dpt = data["state"]
        if dpt is None:
            dpt=""
        country = str(data["country_name"])
        if country is None:
            country=""        
        return ville, dpt, lat, long, country




def obtain_city_data_from_gps():
    print_debug(
        "COORDONNEES_GPS :"
        + "latitude="
        + str(compute_args().gps[0])
        + " longitude="
        + str(compute_args().gps[1])
    )
    geolocator = geopy.geocoders.Nominatim(user_agent="my_geocoder")
    if compute_args().lang:
        location = geolocator.reverse(compute_args().gps[0] +", " + compute_args().gps[1],addressdetails=True)
    else:        
        location = geolocator.reverse(compute_args().gps[0] +", " + compute_args().gps[1],addressdetails=True,language="fr")
    if location is None:
        print(my_colored("erreur : aucune ville trouvée.", "red"))
        exit(1)
    ville = None
    if ville is None or (location.raw.get("address").get("village") is not None):
        ville = location.raw.get("address").get("village")
    if ville is None or (location.raw.get("address").get("municipality") is not None):
        ville = location.raw.get("address").get("municipality")
    if ville is None or (location.raw.get("address").get("town") is not None):
        ville = location.raw.get("address").get("town")               
    if ville is None or (location.raw.get("address").get("city") is not None):
        ville = location.raw.get("address").get("city")        
    dpt = location.raw.get("address").get("county")
    if dpt is None:
        dpt=location.raw.get("address").get("state")
    if dpt is None:
        dpt= location.raw.get("address").get("postcode") 
    if dpt is None or location.raw.get("address").get("country")!="France":
        dpt= location.raw.get("address").get("country")              
    cp = location.raw.get("address").get("postcode")
    country=location.raw.get("address").get("country") 
    if cp is None:
        cp = ""
    lat = location.raw.get("lat")
    long = location.raw.get("lon")
    print_debug(ville+"-"+dpt+"-"+lat+"-"+long+"-"+country)


    return ville, dpt, lat, long, country


def obtain_city_data():
    parties = compute_args().town.split(',')
    if len(parties)>2:
        print(my_colored("erreur : format incorrect : attendu 'ville, pays' ou 'ville'","red"))
        exit(1)
    if len(parties)==1 and compute_args().world==True:
        print(my_colored("warning : si la ville souhaitée ne s'affiche pas vous pouvez utiliser le format 'ville, pays' pour la recherche","yellow"))       
    town = parties[0]
    others = ','.join(parties[1:])
    print_debug(town)
    print_debug(others)
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    geolocator = geopy.geocoders.Nominatim(user_agent="my_geocoder")
    if compute_args().lang:
        locations = geolocator.geocode(town+","+others,exactly_one=False,addressdetails=True,limit=9999)
    else:
        locations = geolocator.geocode(town+","+others,exactly_one=False,addressdetails=True,language="fr",limit=9999)    
    choix = []
    if locations is None:
        print(my_colored("erreur : aucune ville trouvée", "red"))
        exit(1)  
    world=False
    print_debug(str(len(locations)) +" villes trouvées")    
    for location in locations:
        print_debug(json.dumps(location.raw, indent=4,ensure_ascii=False))
        if ((location.raw.get("addresstype")=="postcode" and location.raw.get("address").get("country")=="France") or (location.raw.get("addresstype")=="hamlet" and location.raw.get("address").get("country")!="France") or location.raw.get("addresstype")=="town" or location.raw.get("addresstype")=="city" or location.raw.get("addresstype")=="municipality" or location.raw.get("addresstype")=="village" or (location.raw.get("addresstype")=="province" and location.raw.get("address").get("country_code")=="jp")):   
            ville = None
            if ville is None and (location.raw.get("address").get("province") is not None and (clean_string(location.raw.get("address").get("province").lower())==clean_string(town.lower()))):
                ville = location.raw.get("address").get("province")                 
            if ville is None and (location.raw.get("address").get("city") is not None and (clean_string(location.raw.get("address").get("city").lower())==clean_string(town.lower()))):
                ville = location.raw.get("address").get("city") 
            if ville is None and (location.raw.get("address").get("town") is not None and (clean_string(location.raw.get("address").get("town").lower())==clean_string(town.lower()))):
                ville = location.raw.get("address").get("town")               
            if ville is None and (location.raw.get("address").get("municipality") is not None and (clean_string(location.raw.get("address").get("municipality").lower())==clean_string(town.lower()))):
                ville = location.raw.get("address").get("municipality")
            if ville is None and (location.raw.get("address").get("village") is not None and (clean_string(location.raw.get("address").get("village").lower())==clean_string(town.lower()))):
                ville = location.raw.get("address").get("village")
            if ville is None and (location.raw.get("address").get("hamlet") is not None and (clean_string(location.raw.get("address").get("hamlet").lower())==clean_string(town.lower()))):
                ville = location.raw.get("address").get("hamlet")

            dpt = ""
            if location.raw.get("address").get("county") is not None:        
                dpt = location.raw.get("address").get("county")
            if location.raw.get("address").get("state") is not None:
                if dpt =="":
                    dpt = location.raw.get("address").get("state")  
                else:
                    dpt = dpt + ", "+ location.raw.get("address").get("state") 
            if compute_args().world:
                if dpt =="":                       
                    dpt= location.raw.get("address").get("country")
                else:
                    dpt= dpt + ", "+location.raw.get("address").get("country")

            country = location.raw.get("address").get("country")
            if country == "France" and location.raw.get("addresstype")=="postcode":
                cp = location.raw.get("address").get("postcode")
                if ville is None and (location.raw.get("address").get("village") is not None):
                    ville = location.raw.get("address").get("village")              
                if ville is None and (location.raw.get("address").get("municipality") is not None):
                    ville = location.raw.get("address").get("municipality")
                if ville is None and (location.raw.get("address").get("town") is not None):
                    ville = location.raw.get("address").get("town")               
                if ville is None and (location.raw.get("address").get("city") is not None):
                    ville = location.raw.get("address").get("city")                 
            else:
                cp = ""
            lat = location.raw.get("lat")
            long = location.raw.get("lon")
            if location.raw.get("address").get("country")=="France" and ((location.raw.get("address").get("municipality") is not None and location.raw.get("address").get("village") is not None and location.raw.get("address").get("city") is not None) or (location.raw.get("address").get("municipality") is not None and location.raw.get("address").get("town") is not None and location.raw.get("address").get("city") is not None)):
                ville=None
            if ville is not None:
                print_debug(ville+"-"+dpt+"-"+lat+"-"+long+"-"+country)
                if (clean_string(ville.lower()) == clean_string(town.lower()) or cp.lower() == town.lower()):
                    if ville+"-"+dpt not in [item[0] for item in choix]:  
                        if country=="France":
                            choix.append([ville+"-"+dpt, ville, dpt, country,lat, long])
                        else:
                            if compute_args().world:
                                choix.append([ville+"-"+dpt, ville, dpt, country,lat, long])
                            else:
                                world=True    
    if not compute_args().world and world:
        print("")
        print(my_colored("warning : il existe des villes hors France disponibles pour wotre recherche. Relancez la avec -w pour y acceder", "yellow"))
    if len(choix)==1:
        choice = choix[0]
        ville = choice[1]
        dpt = choice[2]
        country = choice[3]
        lat = choice[4]
        long = choice[5]
        return ville, dpt, lat, long, country    
    elif len(choix)==0:
        print(my_colored("erreur : aucune ville trouvée", "red"))
        exit(1)
    else:
        while True:    
            i=0    
            for choice in choix:
                i=i+1
                print("["+str(i)+"] " + choice[1] + " (" + choice[2]+ ")")
            toto = input("Quelle ville? ")
            if toto.isnumeric() and 1 <= int(toto) <= len(choix):
                break
            print(my_colored("erreur : choix incorrect", "red"))       
        choice = choix[int(toto)-1]
        ville = choice[1]
        dpt = choice[2]
        country = choice[3]
        lat = choice[4]
        long = choice[5]
    return ville, dpt, lat, long, country


def my_colored(message, color):
    if compute_args().nocolor:
        return message
    return termcolor.colored(message, color)


def print_debug(message):
    if compute_args().verbose:
        print("debug : " + message)




def resume(latitude, longitude, tz):
    retry_session = retry_requests.retry(cache_session(), retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = "https://api.open-meteo.com/v1/meteofrance"
    date_debut = (datetime.datetime.now(tz=pytz.timezone(tz)) + datetime.timedelta(days=-1*compute_args().past)).strftime("%Y-%m-%d")
    date_fin = (datetime.datetime.now(tz=pytz.timezone(tz)) + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
    if compute_args().past!=0:
        date_fin = (datetime.datetime.now(tz=pytz.timezone(tz)) + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")    
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
            "sunshine_duration"
        ],
    }
    print_debug("appel api meteo france "+url+"?"+'&'.join([f'{key}={",".join(value) if isinstance(value, list) else value}' for key, value in params.items()]))
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
    precipitation_hours= daily.Variables(10).ValuesAsNumpy()
    sunshine_duration= daily.Variables(11).ValuesAsNumpy()
    alt= response.Elevation()
    debut=daily.Time()
    fin=(daily.TimeEnd())
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
        fin
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
            "is_day"
        ],
        "start_date": (datetime.datetime.now(tz=pytz.timezone(tz)) + datetime.timedelta(days=day)).strftime(
            "%Y-%m-%d"
        ),
        "end_date": (
            datetime.datetime.now(tz=pytz.timezone(tz)) + datetime.timedelta(days=day + 1)
        ).strftime("%Y-%m-%d"),
    }
    print_debug("appel api meteo france "+url+"?"+'&'.join([f'{key}={",".join(value) if isinstance(value, list) else value}' for key, value in params.items()]))
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
    alt= response.Elevation()
    isday= hourly.Variables(12).ValuesAsNumpy()
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
        isday
                )

def cache_session():
    if compute_args().nocache:
        directory = get_user_config_directory_pyweather()
        file_path = os.path.join(directory, ".cache.sqlite")
        if os.path.exists(file_path):
            os.remove(file_path)
            print_debug("Le cache a été supprimé avec succès.")
        else:
            print_debug("Le cache n'existe pas.")
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
            "shortwave_radiation"
        ],
    }
    print_debug("appel api meteo france "+url+"?"+'&'.join([f'{key}={",".join(value) if isinstance(value, list) else value}' for key, value in params.items()]))
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
    isday= current.Variables(11).Value()
    altitude=response.Elevation()
    time=int(response.Current().Time())
    shortwave_radiation=current.Variables(12).Value()

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
        shortwave_radiation
    )

def clean_string(mystring):
    if mystring is None:
        return None
    retour =""
    nfkd_form = unicodedata.normalize('NFKD', mystring)
    retour = ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    retour = retour.replace(' ', '-').replace("'", '-').replace('"', '-')
    #if mystring!=retour:
    #    print_debug(mystring + " modifié en " + retour)
    return retour