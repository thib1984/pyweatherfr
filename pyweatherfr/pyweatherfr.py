"""
pyweatherfr use case
"""

import argparse
import sys
import requests

def find(town):
    r = requests.get("https://prevision-meteo.ch/services/json/"+town)
    if r.json().get("errors"):
        print("error found : ")
        print(r.json().get("errors")[0].get("code"))
        print(r.json().get("errors")[0].get("text"))
        print(r.json().get("errors")[0].get("description"))
        exit(1)
    print("ville       : " +r.json().get("city_info").get("name"))
    print("heure       : " +r.json().get("current_condition").get("date") +" "+r.json().get("current_condition").get("hour"))
    print("========================")
    print("condition    : " +r.json().get("current_condition").get("condition"))
    print("température  : " +str(r.json().get("current_condition").get("tmp"))+"°")    
    print("humidité     : " +str(r.json().get("current_condition").get("humidity"))+"%")
    print("vent         : " +str(r.json().get("current_condition").get("wnd_spd"))+"km/h" + " (" +r.json().get("current_condition").get("wnd_dir") + ")")
    print("pression     : " +str(r.json().get("current_condition").get("pressure"))+"Hp")
    print("========================")
    for i in [0,1,2,3,4]:
        print("date        : " +r.json().get("fcst_day_"+str(i)).get("date") +" ("+r.json().get("fcst_day_"+str(i)).get("day_short") +")")  
        print("température : " +str(r.json().get("fcst_day_"+str(i)).get("tmin"))+"° - "+str(r.json().get("fcst_day_"+str(i)).get("tmax"))+"°") 
        print("condition   : " +r.json().get("fcst_day_"+str(i)).get("condition"))
        print("========================")