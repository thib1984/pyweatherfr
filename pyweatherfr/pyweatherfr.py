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

def find():
    if compute_args().town:
        print_debug("town found from arg -> " + compute_args().town)
        town =compute_args().town
    else:
        with urllib.request.urlopen("https://geolocation-db.com/json") as url:
            print_debug("no town given, search from ip with https://geolocation-db.com/json")
            data = json.loads(url.read().decode())
            print_debug(str(data))                     
            town = data['city']
            print_debug("town found from ip -> " + town)  
    print_debug("search from http://prevision-meteo.ch/services/json/"+town)                   
    r = requests.get("http://prevision-meteo.ch/services/json/"+town)
    if r.json().get("errors"):
        if r.json().get("errors")[0].get("code") == "11":
            print_debug("search town from https://www.prevision-meteo.ch/services/json/list-cities")
            v = requests.get("https://www.prevision-meteo.ch/services/json/list-cities")
            vjson = v.json()
            try:
                matches=[]
                i=0
                while True:
                    if unidecode.unidecode(town.lower()) in unidecode.unidecode(vjson.get(str(i)).get("name").lower()):
                        print(my_colored("for " + vjson.get(str(i)).get("name")+" use parameter : "+vjson.get(str(i)).get("url"),"yellow"))
                        matches.append(vjson.get(str(i)).get("url"))
                    i=i+1
            except Exception:
                if len(matches) == 1:
                    print(my_colored("only one match, we continue...","green"))
                    town = matches[0]
                    print_debug("town found from list-cities -> " + town) 
                    r = requests.get("https://prevision-meteo.ch/services/json/"+town)
                elif len(matches)>1:    
                    print(my_colored("relaunch with correct paramter","yellow"))
                    exit(1)
                else:
                    print(my_colored("error found : ","red"))
                    print(my_colored(r.json().get("errors")[0].get("code"),"red"))
                    print(my_colored(r.json().get("errors")[0].get("text"),"red"))
                    print(my_colored(r.json().get("errors")[0].get("description"),"red"))
                    exit(1)                   
        else: 
            print(my_colored("error found : ","red"))
            print(my_colored(r.json().get("errors")[0].get("code"),"red"))
            print(my_colored(r.json().get("errors")[0].get("text"),"red"))
            print(my_colored(r.json().get("errors")[0].get("description"),"red"))
            exit(1)

    print_debug("search infos from https://www.prevision-meteo.ch/services/json/list-cities")
    v = requests.get("https://www.prevision-meteo.ch/services/json/list-cities")
    vjson = v.json()
    city = r.json().get("city_info").get("name")
    try:
        i=0
        while True:
            if unidecode.unidecode(town.lower()) == unidecode.unidecode(vjson.get(str(i)).get("url").lower()):
                npa = vjson.get(str(i)).get("npa")
                country = vjson.get(str(i)).get("country")
                print_debug("npa found from list-cities -> " + npa) 
                print_debug("country found from list-cities -> " + country) 
                infos = "("+country + " - " + npa+")"
                break
            i=i+1
            infos = ""
    except Exception:
        infos = "not found"        

    if compute_args().day == -1:
        time_now=r.json().get("current_condition").get("date") +" "+r.json().get("current_condition").get("hour")
        condition_now=r.json().get("current_condition").get("condition")
        temp_now=str(r.json().get("current_condition").get("tmp"))+"°"
        humidity_now=str(r.json().get("current_condition").get("humidity"))+"%"
        wind_now=str(r.json().get("current_condition").get("wnd_spd"))+"km/h" + " (" +r.json().get("current_condition").get("wnd_dir") + ")"
        pression_now=str(r.json().get("current_condition").get("pressure"))+"Hp"
        headers = ['day', 'condition', 'T','pluie']
        data=[]        
        for i in [0,1,2,3,4]:
            pluie=0
            day=r.json().get("fcst_day_"+str(i)).get("date") +" ("+r.json().get("fcst_day_"+str(i)).get("day_short") +")"
            condition=r.json().get("fcst_day_"+str(i)).get("condition")
            temp=str(r.json().get("fcst_day_"+str(i)).get("tmin"))+"° - "+str(r.json().get("fcst_day_"+str(i)).get("tmax"))+"°"
            for h in range(0,24):
                hourly_data = r.json().get("fcst_day_"+str(i)).get("hourly_data").get(str(h)+"H00")
                pluie=pluie+hourly_data.get("APCPsfc")
            if pluie > 0:
                pluie=my_colored(str(round(pluie,1))+"mm","yellow")
            else:
                pluie="0mm"
            data.append([day,condition,temp,pluie])
            
        
        if not compute_args().condensate:
            print("")
            print(my_colored("ville       : " +city + " " + infos,"yellow"))
            print("")
            print(my_colored("heure       : " +time_now,"green"))
            print(my_colored("condition   : " +condition_now,"green"))
            print(my_colored("température : " +temp_now ,"green"))   
            print(my_colored("humidité    : " +humidity_now,"green"))
            print(my_colored("vent        : " +wind_now,"green"))
            print(my_colored("pression    : " +pression_now,"green"))
            print("")
            table = columnar(data, headers, no_borders=False)
            print(table)             
        else:
            print(my_colored(time_now + " " + city + " " + infos + " " + condition + " "+ temp + " "+ humidity+ " "+wind+ " "+pression,"green"))
            table = columnar(data, no_borders=True)
            print(table)                         
           

    else:
        #cas day
        json_day = r.json().get("fcst_day_"+str(compute_args().day))
        date_long_format = json_day.get("date") +" ("+json_day.get("day_short") +")"
        temp_delta = str(json_day.get("tmin"))+"° - "+str(json_day.get("tmax"))+"°"
        condition = r.json().get("fcst_day_"+str(compute_args().day)).get("condition")
        total_pluie = 0
        headers = ['hour', 'condition', 'T', 'H', 'P', 'pluie','wind']
        data=[]
        for h in range(0,24):
            hourly_data = json_day.get("hourly_data").get(str(h)+"H00")
            hour=str(h)+"H00"
            cond=hourly_data.get("CONDITION")
            temp=str(hourly_data.get("TMP2m"))+ "°"
            hum=str(hourly_data.get("RH2m"))+ "%"
            pression=str(hourly_data.get("PRMSL"))+"Hp"
            if hourly_data.get("APCPsfc") == 0:
                pluie=str(hourly_data.get("APCPsfc"))+"mm"
            else:
                pluie=my_colored(str(hourly_data.get("APCPsfc"))+"mm","yellow")
                total_pluie=total_pluie+hourly_data.get("APCPsfc")
            wind=str(hourly_data.get("WNDSPD10m"))+ " khm/h " + "("+ str(hourly_data.get("WNDDIRCARD10"))  +")"
            data.append([hour,cond,temp,hum,pression,pluie,wind])
        if total_pluie>0:
            total_pluie=my_colored(str(round(total_pluie,1))+"mm","yellow")
        else:
            total_pluie="0mm"    
        if not compute_args().condensate:
            print("")
            print(my_colored("ville       : " + city + " " + infos,"yellow"))
            print("")
            print(my_colored("date        : " + date_long_format,"green")) 
            print(my_colored("température : " + temp_delta,"green"))
            print(my_colored("pluie       : " + total_pluie,"green"))
            print(my_colored("condition   : " + condition,"green"))   
            print("")
            table = columnar(data, headers, no_borders=False)
            print(table)
        else:
            print(my_colored(date_long_format + " " + city + " " + infos + " " +condition+ " "+ temp_delta+ " "+ total_pluie,"green"))
            table = columnar(data, no_borders=True)
            print(table)   

def my_colored(message, color):
    if compute_args().nocolor:
        return message
    return colored(message,color)      

def print_debug(message):
    if compute_args().verbose:
        print("debug : " + message)