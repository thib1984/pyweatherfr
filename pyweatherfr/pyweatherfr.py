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
import os
import tempfile
import time
from pathlib import Path

incomplete_data = False
SUN = '\U0001F31E'
MI_SUN = '\U0001F324'
CLOUD = '\U0001F325'
MI_CLOUD_RAIN = '\U0001F326'
RAIN = '\U0001F327'
SNOW = '\U0001F328'
NIGHT_CLEAR = '\U0001F319'
ORAGE = '\U0001F329'
ORAGE_PLUIE = '\U0001F329' + " " + '\U0001F327' 
FOG = '\U0001F32B'

DROPLET = '\U0001F4A7'
FLOCON = '\U00002744'

WIND = '\U0001F6A9'

COLD = '\U0001F9CA'
WARM = '\U0001F321'

def emoji_rain(key, isSnow):
    return emoji_rain_allign(key, isSnow, True)

def emoji_rain_allign(key, isSnow, allign):
    if allign is not None and allign == True:
        prefixe = "    "
    else:
        prefixe =""    
    if compute_args().nocolor:
        return key + "mm" 
    if key == ".":
        return prefixe + key + "mm "
    if float(key) > 0:
        if isSnow:
            return FLOCON + "  " + key + "mm "
        else:    
            return DROPLET + "  " + key + "mm "
    return prefixe + key + "mm "

def emoji_tmp(key):
    return emoji_tmp_allign(key, True)
    
def emoji_tmp_allign(key, allign):
    if allign is not None and allign == True:
        prefixe = "    "
    else:
        prefixe =""     
    if compute_args().nocolor:
        return key + "°" 
    if key == ".":
        return prefixe + key + "° " 
    if float(key) <= 0:
        return COLD + "  " + key + "° " 
    if float(key) >= 30:
        return WARM + "  " + key + "° "    
    return prefixe + key + "° " 

def emoji_tmp_right(key):
    return emoji_tmp_allign_right(key, True)
    
def emoji_tmp_allign_right(key, allign):
    if allign is not None and allign == True:
        prefixe = "    "
    else:
        prefixe =""     
    if compute_args().nocolor:
        return key + "° " 
    if key == ".":
        return key + "° " + prefixe
    if float(key) <= 0:
        return key + "° "+ "  " + COLD
    if float(key) >= 30:
        return key + "° "+ "  " + WARM    
    return key + "° "+ prefixe

def emoji_wnd(key):
     return emoji_wnd_allign(key, True)

def emoji_wnd_allign(key, allign):    
    if allign is not None and allign == True:
        prefixe = "    "
    else:
        prefixe =""       
    if compute_args().nocolor:
        return key+ "km/h "
    if key == ".":
        return prefixe + key+ "km/h "
    if float(key) >= 30:
        return WIND + "  " + key+ "km/h "
    return prefixe + key+ "km/h " 

def emoji(key):
    return emoji_allign(key,True)

def emoji_allign(key, allign):
    if allign is not None and allign == True:
        prefixe = "    "
    else:
        prefixe =""     
    if compute_args().nocolor:
        return key 
    if key == "Ensoleillé":
        return SUN + " " + key + " "
    if key =="Nuit claire":
        return NIGHT_CLEAR + "  " + key + " "
    if key == "Ciel voilé":
        return MI_SUN + "  " + key + " "
    if key == "Nuit légèrement voilée":
        return MI_SUN + "  " + key + " "
    if key == "Faibles passages nuageux":
        return MI_SUN + "  " + key + " "               
    if key == "Nuit bien dégagée":
        return MI_SUN + "  " + key + " "
    if key == "Stratus":
        return CLOUD + "  " + key + " "  
    if  key == "Stratus se dissipant":
        return CLOUD + "  " + key + " "
    if key == "Nuit claire et stratus":
        return CLOUD + "  " + key + " "          
    if key == "Eclaircies":
        return MI_SUN + "  " + key+ " "
    if key == "Nuit nuageuse":
        return CLOUD + "  " + key   + " "
    if key=="Faiblement nuageux":
        return MI_SUN+ "  " + key+ " "
    if key == "Fortement nuageux":
        return CLOUD+ "  " + key+ " "
    if key == "Averses de pluie faible":
        return MI_CLOUD_RAIN+ "  " + key+ " "
    if key == "Nuit avec averses":
        return MI_CLOUD_RAIN+ "  " + key+ " "
    if key == "Averses de pluie modérée":
        return RAIN + "  " + key+ " "
    if key == "Averses de pluie forte":
        return RAIN + "  " + key+ " "
    if key == "Couvert avec averses":
        return RAIN+ "  " + key+ " "
    if key == "Pluie faible":
        return MI_CLOUD_RAIN + "  " + key+ " "
    if key == "Pluie forte":
        return RAIN + "  " + key+ " "
    if key == "Pluie modérée":
        return RAIN + "  " + key+ " "
    if key == "Développement nuageux":
        return CLOUD  + "  " + key+ " "
    if key == "Nuit avec développement nuageux":
        return CLOUD     + "  " + key  + " "          
    if key == "Faiblement orageux":
        return ORAGE + "  " + key+ " "
    if key == "Nuit faiblement orageuse":
        return ORAGE+ "  " + key+ " "
    if key == "Orage modéré":
        return ORAGE_PLUIE+ "  " + key+ " "
    if key == "Fortement orageux":
        return ORAGE_PLUIE+ "  " + key+ " "
    if key == "Nuit avec averses de neige faible":
        return SNOW  + "  " + key+ " "
    if key == "Averses de neige faible":
        return SNOW  + "  " + key+ " "        
    if key == "Neige faible":
        return SNOW  + "  " + key+ " "
    if key == "Neige modérée":
        return SNOW+ "  " + key+ " "
    if key == "Neige forte":
        return SNOW+ "  " + key+ " "
    if key == "Pluie et neige mêlée faible":
        return SNOW  + "  " + key+ " "
    if key == "Pluie et neige mêlée modérée":
        return SNOW+ "  " + key+ " "
    if key == "Pluie et neige mêlée forte":
        return SNOW  + "  " + key  + " "                  
    return prefixe + key


def get_user_config_directory():
    """Returns a platform-specific root directory for user config settings."""
    if os.name == "nt":
        appdata = os.getenv("LOCALAPPDATA")
        if appdata:
            ze_path = os.path.join(appdata,"pyweatherfr")
            Path(ze_path).mkdir(parents=True, exist_ok=True)
            return ze_path
        appdata = os.getenv("APPDATA")
        if appdata:
            ze_path = os.path.join(appdata,"pyweatherfr")
            Path(ze_path).mkdir(parents=True, exist_ok=True)
            return ze_path            
        print(my_colored("erreur : impossible de créer le dossier de config","red"))
        sys.exit(1)
    # On non-windows, use XDG_CONFIG_HOME if set, else default to ~/.config.
    xdg_config_home = os.getenv("XDG_CONFIG_HOME")
    if xdg_config_home:
        ze_path = os.path.join(xdg_config_home,"")
        Path(ze_path).mkdir(parents=True, exist_ok=True)
        return ze_path
    ze_path = os.path.join(os.path.expanduser("~"), ".config","pyweatherfr","") 
    Path(ze_path).mkdir(parents=True, exist_ok=True)
    return ze_path 

def find():

    global incomplete_data
    incomplete_data = False

    tmp_json = "villes.json"
    if compute_args().cache or not os.path.exists(get_user_config_directory()+tmp_json) or (
        time.time() - os.stat(get_user_config_directory()+tmp_json).st_mtime > 86400*30
    ):
        print(my_colored("cache des villes absent, expiré ou reset, en cours de téléchargement...","yellow"))
        vjson = requests.get(
        "https://www.prevision-meteo.ch/services/json/list-cities").json()
        print_debug("enregistrement du cache dans " + get_user_config_directory()+tmp_json)
        with open(get_user_config_directory()+tmp_json, 'w') as f:
            json.dump(vjson, f)
    else:
        print_debug("recupération du cache depuis " + get_user_config_directory()+tmp_json)
        with open(get_user_config_directory()+tmp_json, 'r') as f:
            vjson =  json.load(f)

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
                    if unidecode.unidecode(town.lower()) == unidecode.unidecode(vjson.get(str(i)).get("name").lower()):
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
    if compute_args().jour == -1:
        elevation = valueorNA(r.json().get("city_info").get("elevation"))+"m"
        sunrise = valueorNA(r.json().get("city_info").get("sunrise"))
        sunset = valueorNA(r.json().get("city_info").get("sunset"))
        date = valueorNA(r.json().get("current_condition").get("date"))
        hour = valueorNA(r.json().get("current_condition").get("hour"))
        altprev = valueorNA(r.json().get("forecast_info").get("elevation"))+"m"
        time_now = date + " "+hour
        condition_now = emoji_allign(valueorNA(r.json().get(
            "current_condition").get("condition")),False)
        temp_now = emoji_tmp_allign(str(valueorNA(r.json().get(
            "current_condition").get("tmp"))),False)
        humidity_now = str(valueorNA(r.json().get(
            "current_condition").get("humidity")))+"%"
        wnd_spd = emoji_wnd_allign(str(valueorNA(r.json().get(
            "current_condition").get("wnd_spd"))),False)
        wnd_dir = valueorNA(r.json().get("current_condition").get("wnd_dir"))
        wind_now = wnd_spd + "(" + wnd_dir + ")"
        pression_now = str(valueorNA(r.json().get(
            "current_condition").get("pressure")))+" Hp"
        headers = ['date', 'condition', 'température', 'précipitations']
        data = []
        for i in [0, 1, 2, 3, 4]:
            pluie = "."
            date_i = valueorNA(r.json().get("fcst_day_"+str(i)).get("date"))
            day_short_i = valueorNA(r.json().get(
                "fcst_day_"+str(i)).get("day_short"))
            day = date_i + " ("+day_short_i + ")"
            condition = emoji(valueorNA(r.json().get(
                "fcst_day_"+str(i)).get("condition")))
            temp = emoji_tmp(str(valueorNA(r.json().get("fcst_day_"+str(i))).get("tmin"))) + \
                "-> " + \
                emoji_tmp_right(str(valueorNA(r.json().get("fcst_day_"+str(i)).get("tmax"))))
            is_snow_day = False
            for h in range(0, 24):
                hourly_pluie = valueorNA(r.json().get(
                    "fcst_day_"+str(i)).get("hourly_data").get(str(h)+"H00").get("APCPsfc"))
                if hourly_pluie != ".":
                    if pluie == ".":
                        pluie = 0
                    if hourly_pluie != 0 and r.json().get("fcst_day_"+str(i)).get("hourly_data").get(str(h)+"H00").get("ISSNOW")>0:
                        is_snow_day = True                        
                    pluie = pluie+hourly_pluie
            if pluie == ".":
                pluie = emoji_rain(str("."),False)
            elif pluie > 0:
                pluie = emoji_rain(str(round(pluie, 1)),is_snow_day)
            else:
                 pluie = emoji_rain(str("0"),False)
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
            table = columnar(data, headers, no_borders=False,wrap_max=0)
            print(table)
        else:
            print(my_colored(time_now + " " + city + " " + infos + " " + elevation+ " " + sunrise + "-" + sunset, "green"))
            print(my_colored(condition + " " + temp_now + " " + humidity_now + " "+wind_now + " "+pression_now+ " (" + altprev + ") ", "green"))
            table = columnar(data, no_borders=True,wrap_max=0)
            print(table)

        if incomplete_data == True:
            print(my_colored(
                "attention : données incomplètes, vous pouvez essayer une autre ville pour plus de précision", "yellow"))

    else:
        # cas day
        elevation = valueorNA(r.json().get("city_info").get("elevation"))+"m"
        altprev = valueorNA(r.json().get("forecast_info").get("elevation"))+"m"
        sunrise = valueorNA(r.json().get("city_info").get("sunrise"))
        sunset = valueorNA(r.json().get("city_info").get("sunset"))
        json_day = r.json().get("fcst_day_"+str(compute_args().jour))
        date_long_format = valueorNA(json_day.get(
            "date")) + " ("+valueorNA(json_day.get("day_short")) + ")"
        temp_delta = emoji_tmp_allign(str(valueorNA(json_day.get("tmin"))),False) + \
            "-> "+emoji_tmp_allign_right(str(valueorNA(json_day.get("tmax"))),False)
        condition = emoji_allign(valueorNA(r.json().get(
            "fcst_day_"+str(compute_args().jour)).get("condition")),False)
        total_pluie = "."
        headers = ['heure', 'condition', 'température', 'humidité', 'pression', 'précipitations', 'vent']
        data = []
        is_snow_day = False
        for h in range(0, 24):
            hourly_data = json_day.get("hourly_data").get(str(h)+"H00")
            hour = str(h)+"H00"
            cond = emoji(valueorNA(hourly_data.get("CONDITION")))
            temp = emoji_tmp(str(valueorNA(hourly_data.get("TMP2m"))))
            hum = str(valueorNA(hourly_data.get("RH2m"))) + "%"
            pression = str(valueorNA(hourly_data.get("PRMSL")))+"Hp"
            if hourly_data.get("APCPsfc") is None:
                pluie = emoji_rain(str("."),False)
            elif hourly_data.get("APCPsfc") == 0:
                pluie = emoji_rain(str("0"),False)
                if total_pluie == ".":
                    total_pluie = 0
            else:
                pluie = emoji_rain(
                    str(hourly_data.get("APCPsfc")),hourly_data.get("ISSNOW")>=1)
                if total_pluie == ".":
                    total_pluie = 0
                if hourly_data.get("ISSNOW")>0:
                    is_snow_day = True    
                total_pluie = total_pluie+hourly_data.get("APCPsfc")
            wind = emoji_wnd(str(valueorNA(hourly_data.get("WNDSPD10m")))) + \
                "(" + str(valueorNA(hourly_data.get("WNDDIRCARD10"))) + ") "
            data.append([hour, cond, temp, hum, pression, pluie, wind])
        if total_pluie == ".":
            total_pluie == emoji_rain_allign(str("."),False,False)
        elif total_pluie > 0:
            total_pluie = emoji_rain_allign(str(round(total_pluie, 1)),is_snow_day,False)
        else:
            total_pluie = emoji_rain_allign(str("0"),False,False)
        if not compute_args().condensate:
            print("")
            print(my_colored("ville       : " + city + " " + infos, "yellow"))
            print(my_colored("altitude    : " + elevation, "yellow"))
            print("")
            print(my_colored("date        : " + date_long_format, "green"))
            print(my_colored("température : " + temp_delta, "green"))
            print(my_colored("précip.     : " + total_pluie, "green"))
            print(my_colored("condition   : " + condition, "green"))
            if compute_args().jour == 0:
                print(my_colored("soleil      : " + sunrise+" - "+sunset, "green"))
            print("")
            table = columnar(data, headers, no_borders=False,wrap_max=0)
            print(table)
        else:
            if compute_args().jour == 0:
                print(my_colored(date_long_format + " " + city + " " + infos + " " + elevation + " " + sunrise +
                      "-" + sunset, "green"))
                print(my_colored(condition + "  " + temp_delta + " " + total_pluie+ " (" + altprev + ") ", "green"))                      
            else:
                print(my_colored(date_long_format + " " + city + " " + infos + " " + elevation, "green"))
                print(my_colored(condition + "  " + temp_delta + " " + total_pluie+ " (" + altprev + ") ", "green"))                      

            table = columnar(data, no_borders=True,wrap_max=0)
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
