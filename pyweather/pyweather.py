"""
pyweather use case
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
    print(r.json().get("city_info").get("name"))
    print(r.json().get("current_condition").get("date"))
    print(r.json().get("current_condition").get("condition"))   

