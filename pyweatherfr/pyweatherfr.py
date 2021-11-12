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

def find():
    global incomplete_data
    incomplete_data = False
    if compute_args().search:
        search = compute_args().search
        print_debug("search town from https://www.prevision-meteo.ch/services/json/list-cities")
        v = requests.get("https://www.prevision-meteo.ch/services/json/list-cities")
        vjson = v.json()
        i=0
        try:
            while True:
                if vjson.get(str(i)).get("country") is not None and vjson.get(str(i)).get("country") == 'FRA':
                    name = vjson.get(str(i)).get("name")
                    npa = vjson.get(str(i)).get("npa")
                    url = vjson.get(str(i)).get("url")
                    if str(search) == vjson.get(str(i)).get("npa"):
                        print("for " + name +", use \"pyweatherfr '" + url + "'\" or \"pyweatherfr -p " + npa+"\"")
                    if unidecode.unidecode(search.lower()).replace(" ","-") in unidecode.unidecode(vjson.get(str(i)).get("name").lower()).replace(" ","-") or unidecode.unidecode(vjson.get(str(i)).get("name").lower().replace(" ","-")) in unidecode.unidecode(search.lower().replace(" ","-")):
                        print("for " + name +", use '" + url + "' or '-p " + npa+"'")
                i=i+1    
        except Exception:
            sys.exit(1)
        town =compute_args().town
    elif compute_args().town:
        print_debug("town found from arg -> " + unidecode.unidecode(compute_args().town.lower()).replace(" ","-"))
        town =unidecode.unidecode(compute_args().town.lower()).replace(" ","-")
    elif compute_args().post:
        print_debug("postal code found from arg -> " + str(compute_args().post))
        post =compute_args().post        
        print_debug("search town from https://www.prevision-meteo.ch/services/json/list-cities")
        v = requests.get("https://www.prevision-meteo.ch/services/json/list-cities")
        vjson = v.json()
        i=0
        try:
            while True:
                if vjson.get(str(i)).get("country") is not None and vjson.get(str(i)).get("country") == 'FRA':
                    if str(post) == vjson.get(str(i)).get("npa"):
                        town = vjson.get(str(i)).get("url")
                        break
                i=i+1    
        except Exception:
            print(my_colored("no town found with postal code " + str(post)+", try with other code or the main code of your twon?","red"))
            sys.exit(1)
    elif compute_args().gps:
        print_debug("gps found from arg -> " + str(compute_args().gps))
        town="lat="+compute_args().gps[0]+"lng="+compute_args().gps[1]
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
        print(my_colored("error found : ","red"))
        print(my_colored(r.json().get("errors")[0].get("code"),"red"))
        print(my_colored(r.json().get("errors")[0].get("text"),"red"))
        print(my_colored(r.json().get("errors")[0].get("description"),"red"))
        print("")
        print(my_colored("try to found correct parameter with pyweatherfr -s '"+compute_args().town+"'" ,"yellow"))        
        exit(1)                   


    print_debug("search infos from https://www.prevision-meteo.ch/services/json/list-cities")
    v = requests.get("https://www.prevision-meteo.ch/services/json/list-cities")
    vjson = v.json()
    city = r.json().get("city_info").get("name")
    try:
        i=0
        while True:
            if vjson.get(str(i)).get("country") is not None and vjson.get(str(i)).get("country") == 'FRA':            
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
        print(my_colored("town is not found in France","red"))
        sys.exit(1)

    if compute_args().day == -1:
        date = valueorNA(r.json().get("current_condition").get("date"))
        hour = valueorNA(r.json().get("current_condition").get("hour"))       
        time_now=date +" "+hour
        condition_now=valueorNA(r.json().get("current_condition").get("condition"))         
        temp_now=str(valueorNA(r.json().get("current_condition").get("tmp")))+"°"           
        humidity_now=str(valueorNA(r.json().get("current_condition").get("humidity")))+"%"     
        wnd_spd = str(valueorNA(r.json().get("current_condition").get("wnd_spd")))
        wnd_dir = valueorNA(r.json().get("current_condition").get("wnd_dir"))  
        wind_now=wnd_spd +" km/h" + " (" +wnd_dir + ")"
        pression_now = str(valueorNA(r.json().get("current_condition").get("pressure")))+" Hp"
        headers = ['day', 'condition', 'T','pluie']
        data=[]        
        for i in [0,1,2,3,4]:
            pluie="."
            date_i = valueorNA(r.json().get("fcst_day_"+str(i)).get("date"))
            day_short_i = valueorNA(r.json().get("fcst_day_"+str(i)).get("day_short"))                          
            day=date_i +" ("+day_short_i +")"
            condition=valueorNA(r.json().get("fcst_day_"+str(i)).get("condition"))
            temp=str(valueorNA(r.json().get("fcst_day_"+str(i))).get("tmin"))+"° - "+str(valueorNA(r.json().get("fcst_day_"+str(i)).get("tmax")))+"°"
            for h in range(0,24):
                hourly_pluie = valueorNA(r.json().get("fcst_day_"+str(i)).get("hourly_data").get(str(h)+"H00").get("APCPsfc"))
                if hourly_pluie != ".":
                    if pluie == ".":
                        pluie=0
                    pluie=pluie+hourly_pluie
            if pluie == ".":
                pluie=". mm"
            elif pluie > 0:   
                pluie=my_colored(str(round(pluie,1))+" mm","yellow")
            else:
                pluie="0 mm"
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
            print(my_colored(time_now + " " + city + " " + infos + " " + condition + " "+ temp_now + " "+ humidity_now+ " "+wind_now+ " "+pression_now,"green"))
            table = columnar(data, no_borders=True)
            print(table)                         
           
        if incomplete_data == True:
            print(my_colored("incomplete data, you can try an other town","red"))

    else:
        #cas day
        json_day = r.json().get("fcst_day_"+str(compute_args().day))
        date_long_format = valueorNA(json_day.get("date")) +" ("+valueorNA(json_day.get("day_short")) +")"
        temp_delta = str(valueorNA(json_day.get("tmin")))+"° - "+str(valueorNA(json_day.get("tmax")))+"°"
        condition = valueorNA(r.json().get("fcst_day_"+str(compute_args().day)).get("condition"))
        total_pluie = "."
        headers = ['hour', 'condition', 'T', 'H', 'P', 'pluie','wind']
        data=[]
        for h in range(0,24):
            hourly_data = json_day.get("hourly_data").get(str(h)+"H00")
            hour=str(h)+"H00"
            cond=valueorNA(hourly_data.get("CONDITION"))
            temp=str(valueorNA(hourly_data.get("TMP2m")))+ "°"
            hum=str(valueorNA(hourly_data.get("RH2m")))+ "%"
            pression=str(valueorNA(hourly_data.get("PRMSL")))+"Hp"
            if hourly_data.get("APCPsfc") is None:
                pluie=". mm"
            elif hourly_data.get("APCPsfc") == 0:
                pluie=str(hourly_data.get("APCPsfc"))+" mm"
                if total_pluie == ".":
                    total_pluie =0
            else:
                pluie=my_colored(str(hourly_data.get("APCPsfc"))+" mm","yellow")
                if total_pluie == ".":
                    total_pluie =0                
                total_pluie=total_pluie+hourly_data.get("APCPsfc")
            wind=str(valueorNA(hourly_data.get("WNDSPD10m")))+ " khm/h " + "("+ str(valueorNA(hourly_data.get("WNDDIRCARD10")))  +")"
            data.append([hour,cond,temp,hum,pression,pluie,wind])
        if total_pluie == ".":
            total_pluie == ". mm"
        elif total_pluie>0:
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
        if incomplete_data == True:
            print(my_colored("incomplete data, you can try an other town","red"))

    #print_debug("search town from https://www.prevision-meteo.ch/services/json/list-cities")
    #v = requests.get("https://www.prevision-meteo.ch/services/json/list-cities")
    #vjson = v.json()
    #try:
    #    matches=[]
    #    i=0
    #    while True:
    #        if unidecode.unidecode(town.lower()) == unidecode.unidecode(vjson.get(str(i)).get("name").lower()) or unidecode.unidecode(vjson.get(str(i)).get("name").lower()) in unidecode.unidecode(town.lower()):
    #            print(my_colored("for " + vjson.get(str(i)).get("name")+" use parameter : "+vjson.get(str(i)).get("url"),"yellow"))
    #            matches.append(vjson.get(str(i)).get("url"))
    #        i=i+1
    #except Exception:
    #    print("")

def my_colored(message, color):
    if compute_args().nocolor:
        return message
    return colored(message,color)      

def print_debug(message):
    if compute_args().verbose:
        print("debug : " + message)
        
def valueorNA(my_string):
    global incomplete_data
    if my_string is None:
        incomplete_data = True
        return "."
    return my_string     