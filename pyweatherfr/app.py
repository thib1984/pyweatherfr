"""
pyweatherfr use case
"""

import pyweatherfr.openstreetmap
import pyweatherfr.args
import pyweatherfr.log
import pyweatherfr.meteofrance
import datetime

import os
import columnar
import timezonefinder
import pytz
import tzlocal
import numpy


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
LUNETTES = "\U0001F60E"
WIND = "\U0001F6A9"
COLD = "\U0001F9CA"
WARM = "\U0001F321"

HOME = "\U0001F3E0"
BOUSSOLE = "\U0001F9ED"
CLOCK = "\U000023F0"
PC = "\U0001f4bb"


WARNING_WARM = 30
WARNING_FROID = 0
WARNING_SNOW = 0.1
WARNING_RAIN = 0.1
WARNING_WIND = 30
WARNING_WIND_GUST = 50
WARNING_HP = 1030
WARNING_BP = 995
WARNING_HUMIDITY = 90


def find():
    if pyweatherfr.args.compute_args().town:
        ville, dpt, lat, long, country = obtain_city_data()
    elif pyweatherfr.args.compute_args().gps:
        ville, dpt, lat, long, country = obtain_city_data_from_gps()
    else:
        ville, dpt, lat, long, country = (
            pyweatherfr.openstreetmap.obtain_city_data_from_ip()
        )
    tz = timezonefinder.TimezoneFinder().timezone_at(lng=float(long), lat=float(lat))
    if pyweatherfr.args.compute_args().pc:
        tz = str(tzlocal.get_localzone())
    if pyweatherfr.args.compute_args().utc:
        tz = str(pytz.utc)
    pyweatherfr.log.print_debug(tz)
    if pyweatherfr.args.compute_args().now:
        previsions_courantes(ville, dpt, lat, long, tz)
    elif not pyweatherfr.args.compute_args().date is None:
        previsions_detaillees(ville, dpt, lat, long, tz)
    elif pyweatherfr.args.compute_args().jour is None:
        previsions_generiques(ville, dpt, lat, long, tz)
    else:
        previsions_detaillees(ville, dpt, lat, long, tz)
    if (
        not pyweatherfr.args.compute_args().town
        and not pyweatherfr.args.compute_args().gps
    ):
        print(
            pyweatherfr.log.my_colored(
                "warning : si vous utilisez un proxy ou un VPN, la localisation peut être incorrecte",
                "yellow",
            )
        )
    if country is None:
        print(
            pyweatherfr.log.my_colored(
                "warning : ville potentiellement hors de France, les prévisions et données peuvent être moins précises",
                "yellow",
            )
        )
    elif country != "France":
        print(
            pyweatherfr.log.my_colored(
                "warning : ville hors de France, les prévisions et données peuvent être moins précises",
                "yellow",
            )
        )


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
        isday,
    ) = pyweatherfr.meteofrance.specific_day(lat, long, diff_jour(long, lat), tz)
    recap = "Prévisions détaillées pour le " + (
        datetime.datetime.now(tz=pytz.timezone(tz))
        + datetime.timedelta(days=diff_jour(long, lat))
    ).strftime("%Y-%m-%d")
    if pyweatherfr.args.compute_args().pc:
        recap = recap + " (pc)"
    elif pyweatherfr.args.compute_args().utc:
        recap = recap + " (utc.)"
    else:
        recap = recap + " (loc.)"
    if diff_jour(long, lat) < 0:
        recap = "Données détaillées pour le " + (
            datetime.datetime.now(tz=pytz.timezone(tz))
            + datetime.timedelta(days=diff_jour(long, lat))
        ).strftime("%Y-%m-%d")
    print_generic_data_town(ville, dpt, lat, long, alt, recap)
    data = []
    new_var = diff_jour(long, lat)
    for h in range(0, 24):
        if numpy.isnan(hourly_temperature_2m[h]):
            print(
                pyweatherfr.log.my_colored(
                    "warning : pas de données pour ce jour", "yellow"
                )
            )
            exit(1)
        warning = ""
        if (
            datetime.datetime.now(tz=pytz.timezone(tz))
            + datetime.timedelta(days=new_var)
        ).strftime("%Y-%m-%d") == datetime.datetime.now(tz=pytz.timezone(tz)).strftime(
            "%Y-%m-%d"
        ) and 0 < h - int(
            datetime.datetime.now(tz=pytz.timezone(tz)).strftime("%H")
        ) <= 1:
            warning = warning + " " + CLOCK
        if isFullWidth():
            temp = f"{hourly_temperature_2m[h]:.1f}°C ({hourly_apparent_temperature[h]:.1f}°C)"
        else:
            temp = f"{hourly_temperature_2m[h]:.0f}°C"
        if (
            hourly_temperature_2m[h] <= WARNING_FROID
            or hourly_apparent_temperature[h] <= WARNING_FROID
        ):
            warning = warning + " " + COLD
        if (
            hourly_temperature_2m[h] >= WARNING_WARM
            or hourly_apparent_temperature[h] >= WARNING_WARM
        ):
            warning = warning + " " + WARM
        pluie = f"{hourly_precipitation[h]:.1f}mm"
        if snowfall[h] >= WARNING_SNOW:
            warning = warning + " " + SNOW
        elif hourly_precipitation[h] >= WARNING_RAIN:
            warning = warning + " " + RAIN

        vent = (
            f"{hourly_wind_speed_10m[h]:.0f}km/h ({hourly_wind_gusts_10m[h]:.0f}km/h)"
        )
        direction = calculer_direction(hourly_wind_direction_10m[h])

        vent = vent
        if (
            hourly_wind_speed_10m[h] >= WARNING_WIND
            or hourly_wind_gusts_10m[h] >= WARNING_WIND_GUST
        ):
            warning = warning + " " + WIND

        pression = f"{surface_pressure[h]:.0f}Hpa"
        if surface_pressure[h] >= WARNING_HP:
            warning = warning + " " + ELEPHANT
        if surface_pressure[h] <= WARNING_BP:
            warning = warning + " " + PLUME
        weather, emojiweather = traduction(current_weather_code[h], isday[h])
        humidity = f"{relative_humidity_2m[h]:.0f}%"
        duree_soleil = f"{sunshine_duration[h]/60:.0f}'"
        rayonnement = f" {shortwave_radiation[h]:.0f}W/m\u00B2"
        if shortwave_radiation[h] > 1000:
            warning = warning + " " + LUNETTES
        if pyweatherfr.args.compute_args().nocolor:
            if isFullWidth():
                data.append(
                    [
                        datetime.datetime.strftime(
                            datetime.datetime.now(tz=pytz.timezone(tz)).replace(
                                hour=0, minute=0, second=0, microsecond=0
                            )
                            + datetime.timedelta(days=new_var)
                            + datetime.timedelta(hours=h),
                            "%H:%M",
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
                            "%H:%M",
                        ),
                        weather,
                        temp,
                        pluie,
                        vent,
                        direction,
                    ]
                )
        else:
            if isFullWidth():
                data.append(
                    [
                        datetime.datetime.strftime(
                            datetime.datetime.now(tz=pytz.timezone(tz)).replace(
                                hour=0, minute=0, second=0, microsecond=0
                            )
                            + datetime.timedelta(days=new_var)
                            + datetime.timedelta(hours=h),
                            "%H:%M",
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
            else:
                data.append(
                    [
                        datetime.datetime.strftime(
                            datetime.datetime.now(tz=pytz.timezone(tz)).replace(
                                hour=0, minute=0, second=0, microsecond=0
                            )
                            + datetime.timedelta(days=new_var)
                            + datetime.timedelta(hours=h),
                            "%H:%M",
                        ),
                        emojiweather + " " + weather,
                        temp,
                        pluie,
                        vent,
                        direction,
                        warning,
                    ]
                )

    if pyweatherfr.args.compute_args().nocolor:
        if isFullWidth():
            headers = [
                "heure",
                "temps",
                "température (ressentie)",
                "pluie",
                "vent (rafales)",
                "dir.",
                "pression",
                "humidité",
                "rayonnement",
            ]
        else:
            headers = [
                "heure",
                "temps",
                "température",
                "pluie",
                "vent (rafales)",
                "dir.",
            ]
    else:
        if isFullWidth():
            headers = [
                "heure",
                "temps",
                "température (ressentie)",
                "pluie",
                "vent (rafales)",
                "dir.",
                "pression",
                "humidité",
                "rayonnement",
                "/!\\",
            ]
        else:
            headers = [
                "heure",
                "temps",
                "température",
                "pluie",
                "vent (rafales)",
                "dir.",
                "/!\\",
            ]
    if data != []:
        print("")
        table = columnar.columnar(data, headers, no_borders=False, wrap_max=0)
        print(table)
        if not isFullWidth():
            print(
                pyweatherfr.log.my_colored(
                    "warning : pour + d'affichage, élargissez votre terminal", "yellow"
                )
            )


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
        w_soleil,
    ) = pyweatherfr.meteofrance.current(lat, long, tz)
    recap = "Données courantes mesurées à " + datetime.datetime.fromtimestamp(
        time, tz=pytz.timezone(tz)
    ).strftime("%Y-%m-%d %H:%M")
    if pyweatherfr.args.compute_args().pc:
        recap = recap + " (pc)"
    elif pyweatherfr.args.compute_args().utc:
        recap = recap + " (utc.)"
    else:
        recap = recap + " (loc.)"
    print_generic_data_town(ville, dpt, lat, long, alt, recap)
    current_weather, emojiweather = traduction(current_weather_code, isday)
    data = []
    direction = calculer_direction(current_wind_direction_10m)

    if pyweatherfr.args.compute_args().nocolor:
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
        if (
            current_temperature_2m >= WARNING_WARM
            or current_apparent_temperature >= WARNING_WARM
        ):
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
        elif current_precipitation >= WARNING_RAIN:
            data.append(["precipitation", f"{current_precipitation:.1f}mm", RAIN])
        else:
            data.append(["precipitation", f"{current_precipitation:.1f}mm", ""])
        if current_surface_pressure >= WARNING_HP:
            data.append(["pression", f"{current_surface_pressure:.1f}Hp", ELEPHANT])
        elif current_surface_pressure <= WARNING_BP:
            data.append(["pression", f"{current_surface_pressure:.1f}Hp", PLUME])
        else:
            data.append(["pression", f"{current_surface_pressure:.1f}Hp", ""])
        if (
            current_wind_speed_10m >= WARNING_WIND
            or current_wind_gusts_10m >= WARNING_WIND_GUST
        ):
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
        if w_soleil > 1000:
            data.append(["rayonnement", f"{w_soleil:.0f}W/m\u00B2", LUNETTES])
        else:
            data.append(["rayonnement", f"{w_soleil:.0f}W/m\u00B2", ""])
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
        fin,
    ) = pyweatherfr.meteofrance.resume(lat, long, tz)
    datetime.datetime.fromtimestamp(debut, tz=pytz.timezone(tz)).strftime("%Y-%m-%d")
    recap = (
        "Prévisions génériques du "
        + datetime.datetime.fromtimestamp(debut, tz=pytz.timezone(tz)).strftime(
            "%Y-%m-%d"
        )
        + " au "
        + (
            datetime.datetime.fromtimestamp(fin, tz=pytz.timezone(tz))
            + datetime.timedelta(days=-1)
        ).strftime("%Y-%m-%d")
    )
    if pyweatherfr.args.compute_args().past != 0:
        recap = (
            "Données génériques du "
            + datetime.datetime.fromtimestamp(debut, tz=pytz.timezone(tz)).strftime(
                "%Y-%m-%d"
            )
            + " au "
            + (
                datetime.datetime.fromtimestamp(fin, tz=pytz.timezone(tz))
                + datetime.timedelta(days=-1)
            ).strftime("%Y-%m-%d")
        )
    if pyweatherfr.args.compute_args().pc:
        recap = recap + " (pc)"
    elif pyweatherfr.args.compute_args().utc:
        recap = recap + " (utc.)"
    else:
        recap = recap + " (loc.)"
    print_generic_data_town(ville, dpt, lat, long, alt, recap)
    data = []
    fin = 3
    if pyweatherfr.args.compute_args().past != 0:
        fin = -1
    tronque = False
    for i in range(0, len(daily_precipitation_sum)):
        if not numpy.isnan(daily_precipitation_sum[i]):
            warning = ""
            pluie = f"{daily_precipitation_sum[i]:.1f}mm"
            if snowfall[i] >= WARNING_SNOW:
                warning = warning + " " + SNOW
            elif daily_precipitation_sum[i] >= WARNING_RAIN:
                warning = warning + " " + RAIN
            if isFullWidth():
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
            weather, emojiweather = traduction(weather_code[i], 1)

            vent = f"{daily_wind_speed_10m_max[i]:.0f}km/h ({daily_wind_gusts_10m_max[i]:.0f}km/h)"
            direction = calculer_direction(daily_wind_direction_10m_dominant[i])

            vent = vent
            if (
                daily_wind_speed_10m_max[i] >= WARNING_WIND
                or daily_wind_gusts_10m_max[i] >= WARNING_WIND_GUST
            ):
                warning = warning + " " + WIND
            duree_pluie = f"{precipitation_hours[i]:.0f}h"
            duree_soleil = f"{sunshine_duration[i]/3600:.0f}h"
            if pyweatherfr.args.compute_args().nocolor:
                if isFullWidth():
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
                            duree_soleil,
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
                            direction,
                        ]
                    )
            else:
                if isFullWidth():

                    data.append(
                        [
                            datetime.datetime.strftime(
                                datetime.datetime.now(tz=pytz.timezone(tz)).replace(
                                    hour=0, minute=0, second=0, microsecond=0
                                )
                                + datetime.timedelta(hours=24 * i)
                                + datetime.timedelta(
                                    days=-1 * pyweatherfr.args.compute_args().past
                                ),
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
                                + datetime.timedelta(
                                    days=-1 * pyweatherfr.args.compute_args().past
                                ),
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
            tronque = True
    if data != []:
        if pyweatherfr.args.compute_args().nocolor:
            if isFullWidth():

                headers = [
                    "date",
                    "temps",
                    "température (ressentie)",
                    "pluie",
                    "vent (rafales)",
                    "direction",
                    "tps pluie",
                    "tps soleil",
                ]
            else:
                headers = [
                    "date",
                    "temps",
                    "température",
                    "pluie",
                    "vent (rafales)",
                    "direction",
                ]
        else:
            if isFullWidth():

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
        if not isFullWidth():
            print(
                pyweatherfr.log.my_colored(
                    "warning : pour + d'affichage, élargissez votre terminal", "yellow"
                )
            )

    if tronque:
        print(pyweatherfr.log.my_colored("warning : données tronquées", "yellow"))


def print_generic_data_town(ville, dpt, lat, long, alt, recap):
    print("")
    data = []
    if pyweatherfr.args.compute_args().nocolor:
        if (ville is None or ville == "") and (dpt is None or dpt == ""):
            pyweatherfr.log.print_debug("pas de data pour ville/dpt/cp")
        elif dpt is None or dpt == "":
            data.append([ville])
        else:
            data.append([ville + " (" + dpt + ")"])
        data.append(
            [
                f"lat.:  {float(lat):.4f}° / long.: {float(long):.4f}° / alt.: {float(alt):.0f}m "
            ]
        )
        data.append([recap])
    else:
        if (ville is None or ville == "") and (dpt is None or dpt == ""):
            pyweatherfr.log.print_debug("pas de data pour ville/dpt/cp")
        elif dpt is None or dpt == "":
            data.append([HOME, ville])
        else:
            data.append([HOME, ville + " (" + dpt + ")"])
        data.append(
            [
                BOUSSOLE,
                f"lat.:  {float(lat):.4f}°  / long.: {float(long):.4f}° / alt.: {float(alt):.0f}m ",
            ]
        )
        data.append([PC, recap])

    table = columnar.columnar(data, no_borders=False, wrap_max=0)

    print(table)
    if ville=="Springfield" and "Oregon" in dpt:
        art_ascii = "\
            |\/\/\/|\n\
            |      |\n\
            |      |\n\
            | (o)(o)\n\
            C      _)\n\
            | ,___|\n\
            |   /\n\
            /____\n\
            /    \  \n\
        "

        print(art_ascii)


def obtain_city_data_from_gps():
    pyweatherfr.log.print_debug(
        "COORDONNEES_GPS :"
        + "latitude="
        + str(pyweatherfr.args.compute_args().gps[0])
        + " longitude="
        + str(pyweatherfr.args.compute_args().gps[1])
    )
    return pyweatherfr.openstreetmap.obtaingpsfromstreetmap()


def obtain_city_data():
    parties = pyweatherfr.args.compute_args().town.split(",")
    if len(parties) > 2:
        print(
            pyweatherfr.log.my_colored(
                "erreur : format incorrect : attendu 'ville, pays' ou 'ville'", "red"
            )
        )
        exit(1)
    if len(parties) == 1 and pyweatherfr.args.compute_args().world == True:
        print(
            pyweatherfr.log.my_colored(
                "warning : si la ville souhaitée ne s'affiche pas vous pouvez utiliser le format 'ville, pays' pour la recherche",
                "yellow",
            )
        )
    town = parties[0]
    others = ",".join(parties[1:])
    pyweatherfr.log.print_debug(town)
    pyweatherfr.log.print_debug(others)
    choix, world = pyweatherfr.openstreetmap.findcitybyopenstreetmap(town, others)
    if not pyweatherfr.args.compute_args().world and world:
        print("")
        print(
            pyweatherfr.log.my_colored(
                "warning : il existe des villes hors France disponibles pour wotre recherche. Relancez la avec -w pour y acceder",
                "yellow",
            )
        )
    if len(choix) == 1:
        choice = choix[0]
        ville = choice[1]
        dpt = choice[2]
        country = choice[3]
        lat = choice[4]
        long = choice[5]
        return ville, dpt, lat, long, country
    elif len(choix) == 0:
        print(pyweatherfr.log.my_colored("erreur : aucune ville trouvée", "red"))
        exit(1)
    else:
        while True:
            i = 0
            for choice in choix:
                i = i + 1
                print("[" + str(i) + "] " + choice[1] + " (" + choice[2] + ")")
            print("[0] pour quitter")
            answer = input("Quelle ville? ")
            if answer.isnumeric() and int(answer) == 0:
                exit(0)
            if answer.isnumeric() and 1 <= int(answer) <= len(choix):
                break
            print(pyweatherfr.log.my_colored("erreur : choix incorrect", "red"))
        choice = choix[int(answer) - 1]
        ville = choice[1]
        dpt = choice[2]
        country = choice[3]
        lat = choice[4]
        long = choice[5]
    return ville, dpt, lat, long, country


def diff_jour(long, lat):
    tz = timezonefinder.TimezoneFinder().timezone_at(lng=float(long), lat=float(lat))
    if not pyweatherfr.args.compute_args().date is None:
        if not est_format_date(pyweatherfr.args.compute_args().date):
            print(
                pyweatherfr.log.my_colored(
                    "erreur : format date invalide, format attendu yyyy-mm-dd", "red"
                )
            )
            exit(1)
        diff = (
            pytz.timezone(tz).localize(
                datetime.datetime.strptime(
                    pyweatherfr.args.compute_args().date, "%Y-%m-%d"
                )
            )
            - datetime.datetime.now(tz=pytz.timezone(tz))
        ).days + 1
        pyweatherfr.log.print_debug(str(diff) + " jours")
        if diff >= 15:
            print(
                pyweatherfr.log.my_colored(
                    "erreur : date invalide (limitée à +14 jour de la date actuelle)",
                    "red",
                )
            )
            exit(1)
        return diff
    if pyweatherfr.args.compute_args().jour >= 15:
        print(
            pyweatherfr.log.my_colored(
                "erreur : date invalide (limitée à +14 jour de la date actuelle)", "red"
            )
        )
        exit(1)
    return pyweatherfr.args.compute_args().jour


def est_format_date(chaine):
    try:
        datetime.datetime.strptime(chaine, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def isFullWidth():
    try:
        return (
            os.get_terminal_size().columns > 140
            or pyweatherfr.args.compute_args().fullwidth
        )
    except Exception:
        pyweatherfr.log.print_debug("détection impossible de la largeur du terminal")
        return True


def calculer_direction(direction_vent_degres):
    if direction_vent_degres <= 22.5 or direction_vent_degres >= 360 - 22.5:
        direction = "N  "
        if not pyweatherfr.args.compute_args().nocolor:
            direction = direction + FLECHE_N
    if direction_vent_degres <= 360 - 22.5 and direction_vent_degres > 360 - 22.5 - 45:
        direction = "NO "
        if not pyweatherfr.args.compute_args().nocolor:
            direction = direction + FLECHE_NO
    if (
        direction_vent_degres <= 360 - 22.5 - 45
        and direction_vent_degres > 360 - 22.5 - 90
    ):
        direction = "O  "
        if not pyweatherfr.args.compute_args().nocolor:
            direction = direction + FLECHE_O
    if (
        direction_vent_degres <= 360 - 22.5 - 90
        and direction_vent_degres > 360 - 22.5 - 135
    ):
        direction = "SO "
        if not pyweatherfr.args.compute_args().nocolor:
            direction = direction + FLECHE_SO
    if (
        direction_vent_degres <= 360 - 22.5 - 135
        and direction_vent_degres > 360 - 22.5 - 180
    ):
        direction = "S  "
        if not pyweatherfr.args.compute_args().nocolor:
            direction = direction + FLECHE_S
    if (
        direction_vent_degres <= 360 - 22.5 - 180
        and direction_vent_degres > 360 - 22.5 - 225
    ):
        direction = "SE "
        if not pyweatherfr.args.compute_args().nocolor:
            direction = direction + FLECHE_SE
    if (
        direction_vent_degres <= 360 - 22.5 - 225
        and direction_vent_degres > 360 - 22.5 - 270
    ):
        direction = "E  "
        if not pyweatherfr.args.compute_args().nocolor:
            direction = direction + FLECHE_E
    if (
        direction_vent_degres <= 360 - 22.5 - 270
        and direction_vent_degres > 360 - 22.5 - 315
    ):
        direction = "NE "
        if not pyweatherfr.args.compute_args().nocolor:
            direction = direction + FLECHE_NE
    return direction


def traduction(current_weather_code, jour):
    if (
        current_weather_code == 0
        or current_weather_code == 1
        or current_weather_code == 2
    ):
        if jour == 0:
            return ["nuit claire ", NIGHT_CLEAR]
        return ["ciel clair ", SUN]
    if current_weather_code >= 3 and current_weather_code <= 12:
        if jour == 0:
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
