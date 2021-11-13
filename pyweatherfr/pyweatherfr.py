"""
pyweatherfr use case
"""

import argparse
import sys
import requests
import unidecode
from pyweatherfr.args import compute_args
from columnar import columnar
from termcolor import colored
import json
import urllib.request

incomplete_data = False
SUN = '\U0001F31E'
MI_SUN = '\U0001F324'
MI_CLOUD = '\U0001F325'
CLOUD = '\U00002601'
MI_CLOUD_RAIN = '\U0001F326'
RAIN = '\U0001F327'
SNOW = '\U0001F328'
NIGHT_CLEAR = '\U0001F319'
ORAGE = '\U0001F329'
ORAGE_PLUIE = '\U000026c5' 
FOG = '\U0001F32B'


def emoji(key):
    if compute_args().nocolor:
        return key 
    if key == "Ensoleillé":
        return SUN + " " + key
    if key =="Nuit claire":
        return NIGHT_CLEAR + "  " + key
    if key == "Ciel voilé":
        return MI_SUN + "  " + key
    if key == "Nuit légèrement voilée":
        return MI_SUN + "  " + key
    if key == "Faibles passages nuageux":
        return MI_SUN + "  " + key                
    if key == "Nuit bien dégagée":
        return MI_SUN + "  " + key 
    if key == "Stratus":
        return CLOUD + "  " + key   
    if  key == "Stratus se dissipant":
        return CLOUD + "  " + key
    if key == "Nuit claire et stratus":
        return CLOUD + "  " + key           
    if key == "Eclaircies":
        return MI_SUN + "  " + key
    if key == "Nuit nuageuse":
        return CLOUD + "  " + key   
    if key=="Faiblement nuageux":
        return MI_SUN+ "  " + key
    if key == "Fortement nuageux":
        return CLOUD+ "  " + key
    if key == "Averses de pluie faible":
        return MI_CLOUD_RAIN+ "  " + key
    if key == "Nuit avec averses":
        return MI_CLOUD_RAIN+ "  " + key
    if key == "Averses de pluie modérée":
        return RAIN + "  " + key
    if key == "Averses de pluie forte":
        return RAIN + "  " + key
    if key == "Couvert avec averse":
        return RAIN+ "  " + key
    if key == "Pluie faible":
        return MI_CLOUD_RAIN + "  " + key
    if key == "Pluie forte":
        return RAIN + "  " + key
    if key == "Pluie modérée":
        return RAIN + "  " + key
    if key == "Développement nuageux":
        return CLOUD  + "  " + key
    if key == "Nuit avec développement nuageux":
        return CLOUD     + "  " + key            
    if key == "Faiblement orageux":
        return ORAGE + "  " + key
    if key == "Nuit faiblement orageuse":
        return ORAGE+ "  " + key
    if key == "Orage modéré":
        return ORAGE_PLUIE+ "  " + key
    if key == "Fortement orageux":
        return ORAGE_PLUIE+ "  " + key
    if key == "Nuit avec averses de neige faible":
        return SNOW  + "  " + key
    if key == "Neige faible":
        return SNOW  + "  " + key
    if key == "Neige modérée":
        return SNOW+ "  " + key
    if key == "Neige forte":
        return SNOW+ "  " + key
    if key == "Pluie et neige mélée faible":
        return SNOW  + "  " + key
    if key == "Pluie et neige mélée modérée":
        return SNOW+ "  " + key
    if key == "Pluie et neige mélée forte":
        return SNOW  + "  " + key                    
    return key

def find():

    
    global incomplete_data
    incomplete_data = False
    vjson = requests.get(
        "https://www.prevision-meteo.ch/services/json/list-cities").json()
    if compute_args().search:
        search = compute_args().search
        print_debug(
            "recherche de la ville depuis https://www.prevision-meteo.ch/services/json/list-cities")
        trouve = False
        i = 0
        try:
            while True:
                if vjson.get(str(i)).get("country") is not None and vjson.get(str(i)).get("country") == 'FRA':
                    name = vjson.get(str(i)).get("name")
                    npa = vjson.get(str(i)).get("npa")
                    url = vjson.get(str(i)).get("url")
                    if (str(search) == vjson.get(str(i)).get("npa")) or unidecode.unidecode(search.lower()).replace(" ", "-") in unidecode.unidecode(vjson.get(str(i)).get("name").lower()).replace(" ", "-") or unidecode.unidecode(vjson.get(str(i)).get("name").lower().replace(" ", "-")) in unidecode.unidecode(search.lower().replace(" ", "-")):
                        trouve = True
                        print(my_colored("pour " + name + " ("+npa+"), exécutez 'pyweatherfr " +
                              url + "' or 'pyweatherfr -p " + npa+"'","yellow"))
                i = i+1
        except Exception:
            if not trouve:
                print(my_colored("erreur : pas de ville trouvée", "red"))
            sys.exit(1)
    elif compute_args().town:
        town = unidecode.unidecode(
            compute_args().town.lower()).replace(" ", "-")
        print_debug("VILLE : " +
                    unidecode.unidecode(compute_args().town.lower()).replace(" ", "-"))
        url = town
        print_debug("URL : " +
                    unidecode.unidecode(compute_args().town.lower()).replace(" ", "-"))
    elif compute_args().post:
        post = compute_args().post.zfill(5)
        print_debug("CODE_POSTAL : " + str(post))
        print_debug(
            "recherche de la VILLE et de l'URL depuis https://www.prevision-meteo.ch/services/json/list-cities")
        i = 0
        try:
            while True:
                if vjson.get(str(i)).get("country") is not None and vjson.get(str(i)).get("country") == 'FRA':
                    if str(post) == vjson.get(str(i)).get("npa"):
                        town = vjson.get(str(i)).get("name")
                        print_debug("VILLE : " + town)
                        url = vjson.get(str(i)).get("url")
                        print_debug("URL : " + town)
                        break
                i = i+1
        except Exception:
            print(my_colored(
                "erreur : pas de ville trouvée avec le code postal " + str(post), "red"))
            print(my_colored(
                "essayez avec un autre code postal, ou avec le code postal principal de la ville", "yellow"))
            sys.exit(1)
    elif compute_args().gps:
        print_debug("COORDONNEES_GPS :" + "latitude=" +
                    str(compute_args().gps[0])+" longitude="+str(compute_args().gps[1]))
        url = "lat="+compute_args().gps[0]+"lng="+compute_args().gps[1]
        print_debug("URL : " + url)
        town = None
    else:
        with urllib.request.urlopen("https://geolocation-db.com/json") as url:
            print_debug(
                "recherche de la localisation depuis https://geolocation-db.com/json")
            data = json.loads(url.read().decode())
            print_debug(str(data))
            town = data['city']
            if town is None:
                print(my_colored(
                    "attention : pas de ville trouvée avec l'ip, utilisation des coordonnées GPS...", "yellow"))
                print_debug("COORDONNEES_GPS :" + "latitude=" +
                            str(data['latitude'])+" longitude="+str(data['longitude']))
                url = "lat="+str(data['latitude']) + \
                    "lng="+str(data['longitude'])
                print_debug("URL : " + url)
            else:
                print_debug("VILLE : " + town)
                url = town
                print_debug("URL : " + url)
    print_debug(
        "recherche prévision depuis http://prevision-meteo.ch/services/json/"+url)
    r = requests.get("http://prevision-meteo.ch/services/json/"+url)
    if r.json().get("errors"):
        print(my_colored("erreur : pas de données trouvées", "red"))
        print_debug(r.json().get("errors")[0].get("code"))
        print_debug(r.json().get("errors")[0].get("text"))
        print_debug(r.json().get("errors")[0].get("description"))
        if compute_args().town or compute_args().post:
            print(my_colored("essayez de trouver un paramètre correct avec \"pyweatherfr -s '" +
                  compute_args().town+"'\"", "yellow"))
        else:
            print(my_colored(
                "essayez avec le lancement classique \"pyweatherfr [VILLE]\"", "yellow"))
        exit(1)

    if town is not None:
        print_debug(
            "recherche informations de la VILLE depuis https://www.prevision-meteo.ch/services/json/list-cities")
        city = r.json().get("city_info").get("name")
        try:
            i = 0
            while True:
                if vjson.get(str(i)).get("country") is not None and vjson.get(str(i)).get("country") == 'FRA':
                    if unidecode.unidecode(town.lower()) == unidecode.unidecode(vjson.get(str(i)).get("url").lower()):
                        npa = vjson.get(str(i)).get("npa")
                        country = vjson.get(str(i)).get("country")
                        print_debug("CODE_POSTAL : " + npa)
                        print_debug("COUNTRY : " + country)
                        infos = "("+country + " - " + npa+")"
                        break
                i = i+1
                infos = ""
        except Exception:
            print(my_colored("erreur : la VILLE n'est pas en France", "red"))
            print(my_colored("essayez de trouver un paramètre correct avec \"pyweatherfr -s '" +
                  compute_args().town+"'\"", "yellow"))
            sys.exit(1)
    else:
        city = "."
        infos = "("+url+")"
    if compute_args().day == -1:
        elevation = valueorNA(r.json().get("city_info").get("elevation"))+"m"
        sunrise = valueorNA(r.json().get("city_info").get("sunrise"))
        sunset = valueorNA(r.json().get("city_info").get("sunset"))
        date = valueorNA(r.json().get("current_condition").get("date"))
        hour = valueorNA(r.json().get("current_condition").get("hour"))
        time_now = date + " "+hour
        condition_now = emoji(valueorNA(r.json().get(
            "current_condition").get("condition")))
        temp_now = str(valueorNA(r.json().get(
            "current_condition").get("tmp")))+"°"
        humidity_now = str(valueorNA(r.json().get(
            "current_condition").get("humidity")))+"%"
        wnd_spd = str(valueorNA(r.json().get(
            "current_condition").get("wnd_spd")))
        wnd_dir = valueorNA(r.json().get("current_condition").get("wnd_dir"))
        wind_now = wnd_spd + " km/h" + " (" + wnd_dir + ")"
        pression_now = str(valueorNA(r.json().get(
            "current_condition").get("pressure")))+" Hp"
        headers = ['day', 'condition', 'T', 'pluie']
        data = []
        for i in [0, 1, 2, 3, 4]:
            pluie = "."
            date_i = valueorNA(r.json().get("fcst_day_"+str(i)).get("date"))
            day_short_i = valueorNA(r.json().get(
                "fcst_day_"+str(i)).get("day_short"))
            day = date_i + " ("+day_short_i + ")"
            condition = emoji(valueorNA(r.json().get(
                "fcst_day_"+str(i)).get("condition")))
            temp = str(valueorNA(r.json().get("fcst_day_"+str(i))).get("tmin")) + \
                "° - " + \
                str(valueorNA(r.json().get("fcst_day_"+str(i)).get("tmax")))+"°"
            for h in range(0, 24):
                hourly_pluie = valueorNA(r.json().get(
                    "fcst_day_"+str(i)).get("hourly_data").get(str(h)+"H00").get("APCPsfc"))
                if hourly_pluie != ".":
                    if pluie == ".":
                        pluie = 0
                    pluie = pluie+hourly_pluie
            if pluie == ".":
                pluie = ". mm"
            elif pluie > 0:
                pluie = my_colored(str(round(pluie, 1))+"mm", "yellow")
            else:
                pluie = "0 mm"
            data.append([day, condition, temp, pluie])

        if not compute_args().condensate:
            print("")
            print(my_colored("ville       : " + city + " " + infos, "yellow"))
            print(my_colored("altitude    : " + elevation, "yellow"))
            print("")
            print(my_colored("heure       : " + time_now, "green"))
            print(my_colored("condition   : " + condition_now, "green"))
            print(my_colored("température : " + temp_now, "green"))
            print(my_colored("humidité    : " + humidity_now, "green"))
            print(my_colored("vent        : " + wind_now, "green"))
            print(my_colored("pression    : " + pression_now, "green"))
            print(my_colored("soleil      : " + sunrise+" - "+sunset, "green"))
            print("")
            table = columnar(data, headers, no_borders=False)
            print(table)
        else:
            print(my_colored(time_now + " " + city + " " + infos + " " + elevation + " " + sunrise + "-" + sunset +
                  " " + condition + " " + temp_now + " " + humidity_now + " "+wind_now + " "+pression_now, "green"))
            table = columnar(data, no_borders=True)
            print(table)

        if incomplete_data == True:
            print(my_colored(
                "attention : données incomplètes, vous pouvez essayer une autre ville pour plus de précision", "yellow"))

    else:
        # cas day
        elevation = valueorNA(r.json().get("city_info").get("elevation"))+"m"
        sunrise = valueorNA(r.json().get("city_info").get("sunrise"))
        sunset = valueorNA(r.json().get("city_info").get("sunset"))
        json_day = r.json().get("fcst_day_"+str(compute_args().day))
        date_long_format = valueorNA(json_day.get(
            "date")) + " ("+valueorNA(json_day.get("day_short")) + ")"
        temp_delta = str(valueorNA(json_day.get("tmin"))) + \
            "° - "+str(valueorNA(json_day.get("tmax")))+"°"
        condition = emoji(valueorNA(r.json().get(
            "fcst_day_"+str(compute_args().day)).get("condition")))
        total_pluie = "."
        headers = ['hour', 'condition', 'T', 'H', 'P', 'pluie', 'wind']
        data = []
        for h in range(0, 24):
            hourly_data = json_day.get("hourly_data").get(str(h)+"H00")
            hour = str(h)+"H00"
            cond = emoji(valueorNA(hourly_data.get("CONDITION")))
            temp = str(valueorNA(hourly_data.get("TMP2m"))) + "°"
            hum = str(valueorNA(hourly_data.get("RH2m"))) + "%"
            pression = str(valueorNA(hourly_data.get("PRMSL")))+"Hp"
            if hourly_data.get("APCPsfc") is None:
                pluie = ". mm"
            elif hourly_data.get("APCPsfc") == 0:
                pluie = str(hourly_data.get("APCPsfc"))+"mm"
                if total_pluie == ".":
                    total_pluie = 0
            else:
                pluie = my_colored(
                    str(hourly_data.get("APCPsfc"))+"mm", "yellow")
                if total_pluie == ".":
                    total_pluie = 0
                total_pluie = total_pluie+hourly_data.get("APCPsfc")
            wind = str(valueorNA(hourly_data.get("WNDSPD10m"))) + "khm/h " + \
                "(" + str(valueorNA(hourly_data.get("WNDDIRCARD10"))) + ")"
            data.append([hour, cond, temp, hum, pression, pluie, wind])
        if total_pluie == ".":
            total_pluie == ". mm"
        elif total_pluie > 0:
            total_pluie = my_colored(str(round(total_pluie, 1))+"mm", "yellow")
        else:
            total_pluie = "0mm"
        if not compute_args().condensate:
            print("")
            print(my_colored("ville       : " + city + " " + infos, "yellow"))
            print(my_colored("altitude    : " + elevation, "yellow"))
            print("")
            print(my_colored("date        : " + date_long_format, "green"))
            print(my_colored("température : " + temp_delta, "green"))
            print(my_colored("pluie       : " + total_pluie, "green"))
            print(my_colored("condition   : " + condition, "green"))
            if compute_args().day == 0:
                print(my_colored("soleil      : " + sunrise+" - "+sunset, "green"))
            print("")
            table = columnar(data, headers, no_borders=False)
            print(table)
        else:
            if compute_args().day == 0:
                print(my_colored(date_long_format + " " + city + " " + infos + " " + elevation + " " + sunrise +
                      "-" + sunset + " "  + condition + "  " + temp_delta + " " + total_pluie, "green"))
            else:
                print(my_colored(date_long_format + " " + city + " " + infos + " " +
                      elevation + " " + condition + " " + temp_delta + " " + total_pluie, "green"))
            table = columnar(data, no_borders=True)
            print(table)
            
        if incomplete_data == True:
            print(my_colored(
                "attention : données incomplètes, vous pouvez essayer une autre ville pour plus de précision", "yellow"))


def my_colored(message, color):
    if compute_args().nocolor:
        return message
    return colored(message, color)


def print_debug(message):
    if compute_args().verbose:
        print("debug : " + message)


def valueorNA(my_string):
    global incomplete_data
    if my_string is None:
        incomplete_data = True
        return "."
    return my_string
