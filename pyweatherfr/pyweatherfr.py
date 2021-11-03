"""
pyweatherfr use case
"""

import argparse
import sys
import requests
import unidecode

def find(town):
    r = requests.get("https://prevision-meteo.ch/services/json/"+town)
    if r.json().get("errors"):
        if r.json().get("errors")[0].get("code") == "11":
            v = requests.get("https://www.prevision-meteo.ch/services/json/list-cities")
            vjson = v.json()
            try:
                matches=[]
                i=0
                while True:
                    if unidecode.unidecode(town.lower()) in unidecode.unidecode(vjson.get(str(i)).get("name").lower()):
                        print("for " + vjson.get(str(i)).get("name")+" use parameter : "+vjson.get(str(i)).get("url"))
                        matches.append(vjson.get(str(i)).get("url"))
                    i=i+1
            except Exception:
                if len(matches) == 1:
                    print("only one match, we continue...")
                    town = matches[0]
                    r = requests.get("https://prevision-meteo.ch/services/json/"+town)
                elif len(matches)>1:    
                    print("relaunch with correct paramter")
                    exit(1)
                else:
                    print("error found : ")
                    print(r.json().get("errors")[0].get("code"))
                    print(r.json().get("errors")[0].get("text"))
                    print(r.json().get("errors")[0].get("description"))
                    exit(1)                    
        else: 
            print("error found : ")
            print(r.json().get("errors")[0].get("code"))
            print(r.json().get("errors")[0].get("text"))
            print(r.json().get("errors")[0].get("description"))
            exit(1)


    v = requests.get("https://www.prevision-meteo.ch/services/json/list-cities")
    vjson = v.json()
    try:
        i=0
        while True:
            if unidecode.unidecode(town.lower()) == unidecode.unidecode(vjson.get(str(i)).get("url").lower()):
                npa = vjson.get(str(i)).get("npa")
                country = vjson.get(str(i)).get("country")
                infos = "("+country + " - " + npa+")"
                break
            i=i+1
            infos = ""
    except Exception:
        region = "not found"        
    print("ville       : " +r.json().get("city_info").get("name") + " " + infos)
    print("heure       : " +r.json().get("current_condition").get("date") +" "+r.json().get("current_condition").get("hour"))
    print("========================")
    print("condition   : " +r.json().get("current_condition").get("condition"))
    print("température : " +str(r.json().get("current_condition").get("tmp"))+"°")    
    print("humidité    : " +str(r.json().get("current_condition").get("humidity"))+"%")
    print("vent        : " +str(r.json().get("current_condition").get("wnd_spd"))+"km/h" + " (" +r.json().get("current_condition").get("wnd_dir") + ")")
    print("pression    : " +str(r.json().get("current_condition").get("pressure"))+"Hp")
    print("========================")
    for i in [0,1,2,3,4]:
        print("date        : " +r.json().get("fcst_day_"+str(i)).get("date") +" ("+r.json().get("fcst_day_"+str(i)).get("day_short") +")")  
        print("température : " +str(r.json().get("fcst_day_"+str(i)).get("tmin"))+"° - "+str(r.json().get("fcst_day_"+str(i)).get("tmax"))+"°") 
        print("condition   : " +r.json().get("fcst_day_"+str(i)).get("condition"))
        print("========================")