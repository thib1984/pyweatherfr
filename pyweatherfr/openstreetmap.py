import certifi
import ssl
import geopy
import unicodedata
import json
import urllib.request

import pyweatherfr.args
import pyweatherfr.log


def findcitybyopenstreetmap(town, others):
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    geolocator = geopy.geocoders.Nominatim(user_agent="my_geocoder")
    if pyweatherfr.args.compute_args().lang:
        locations = geolocator.geocode(
            town + "," + others, exactly_one=False, addressdetails=True, limit=9999
        )
    else:
        locations = geolocator.geocode(
            town + "," + others,
            exactly_one=False,
            addressdetails=True,
            language="fr",
            limit=9999,
        )
    choix = []
    if locations is None:
        print(pyweatherfr.log.my_colored("erreur : aucune ville trouvée", "red"))
        exit(1)
    world = False
    pyweatherfr.log.print_debug(str(len(locations)) + " villes trouvées")
    for location in locations:
        pyweatherfr.log.print_debug(
            json.dumps(location.raw, indent=4, ensure_ascii=False)
        )
        if (
            (
                location.raw.get("addresstype") == "postcode"
                and location.raw.get("address").get("country") == "France"
            )
            or (
                location.raw.get("addresstype") == "hamlet"
                and location.raw.get("address").get("country") != "France"
            )
            or location.raw.get("addresstype") == "town"
            or location.raw.get("addresstype") == "city"
            or location.raw.get("addresstype") == "municipality"
            or location.raw.get("addresstype") == "village"
            or (
                location.raw.get("addresstype") == "province"
                and location.raw.get("address").get("country_code") == "jp"
            )
        ):
            ville = None
            if ville is None and (
                location.raw.get("address").get("province") is not None
                and (
                    clean_string(location.raw.get("address").get("province").lower())
                    == clean_string(town.lower())
                )
            ):
                ville = location.raw.get("address").get("province")
            if ville is None and (
                location.raw.get("address").get("city") is not None
                and (
                    clean_string(location.raw.get("address").get("city").lower())
                    == clean_string(town.lower())
                )
            ):
                ville = location.raw.get("address").get("city")
            if ville is None and (
                location.raw.get("address").get("town") is not None
                and (
                    clean_string(location.raw.get("address").get("town").lower())
                    == clean_string(town.lower())
                )
            ):
                ville = location.raw.get("address").get("town")
            if ville is None and (
                location.raw.get("address").get("municipality") is not None
                and (
                    clean_string(
                        location.raw.get("address").get("municipality").lower()
                    )
                    == clean_string(town.lower())
                )
            ):
                ville = location.raw.get("address").get("municipality")
            if ville is None and (
                location.raw.get("address").get("village") is not None
                and (
                    clean_string(location.raw.get("address").get("village").lower())
                    == clean_string(town.lower())
                )
            ):
                ville = location.raw.get("address").get("village")
            if ville is None and (
                location.raw.get("address").get("hamlet") is not None
                and (
                    clean_string(location.raw.get("address").get("hamlet").lower())
                    == clean_string(town.lower())
                )
            ):
                ville = location.raw.get("address").get("hamlet")

            dpt = ""
            if location.raw.get("address").get("county") is not None:
                dpt = location.raw.get("address").get("county")
            if location.raw.get("address").get("state") is not None:
                if dpt == "":
                    dpt = location.raw.get("address").get("state")
                else:
                    dpt = dpt + ", " + location.raw.get("address").get("state")
            if pyweatherfr.args.compute_args().world:
                if dpt == "":
                    dpt = location.raw.get("address").get("country")
                else:
                    dpt = dpt + ", " + location.raw.get("address").get("country")

            country = location.raw.get("address").get("country")
            if country == "France" and location.raw.get("addresstype") == "postcode":
                cp = location.raw.get("address").get("postcode")
                if ville is None and (
                    location.raw.get("address").get("village") is not None
                ):
                    ville = location.raw.get("address").get("village")
                if ville is None and (
                    location.raw.get("address").get("municipality") is not None
                ):
                    ville = location.raw.get("address").get("municipality")
                if ville is None and (
                    location.raw.get("address").get("town") is not None
                ):
                    ville = location.raw.get("address").get("town")
                if ville is None and (
                    location.raw.get("address").get("city") is not None
                ):
                    ville = location.raw.get("address").get("city")
            else:
                cp = ""
            lat = location.raw.get("lat")
            long = location.raw.get("lon")
            if location.raw.get("address").get("country") == "France" and (
                (
                    location.raw.get("address").get("municipality") is not None
                    and location.raw.get("address").get("village") is not None
                    and location.raw.get("address").get("city") is not None
                )
                or (
                    location.raw.get("address").get("municipality") is not None
                    and location.raw.get("address").get("town") is not None
                    and location.raw.get("address").get("city") is not None
                )
            ):
                ville = None
            if ville is not None:
                pyweatherfr.log.print_debug(
                    ville + "-" + dpt + "-" + lat + "-" + long + "-" + country
                )
                if (
                    clean_string(ville.lower()) == clean_string(town.lower())
                    or cp.lower() == town.lower()
                ):
                    if ville + "-" + dpt not in [item[0] for item in choix]:
                        if country == "France":
                            choix.append(
                                [ville + "-" + dpt, ville, dpt, country, lat, long]
                            )
                        else:
                            if pyweatherfr.args.compute_args().world:
                                choix.append(
                                    [ville + "-" + dpt, ville, dpt, country, lat, long]
                                )
                            else:
                                world = True
    return choix, world


def obtaingpsfromstreetmap():
    geolocator = geopy.geocoders.Nominatim(user_agent="my_geocoder")
    if pyweatherfr.args.compute_args().lang:
        location = geolocator.reverse(
            pyweatherfr.args.compute_args().gps[0]
            + ", "
            + pyweatherfr.args.compute_args().gps[1],
            addressdetails=True,
        )
    else:
        location = geolocator.reverse(
            pyweatherfr.args.compute_args().gps[0]
            + ", "
            + pyweatherfr.args.compute_args().gps[1],
            addressdetails=True,
            language="fr",
        )
    if location is None:
        print(pyweatherfr.logmy_colored("erreur : aucune ville trouvée.", "red"))
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
        dpt = location.raw.get("address").get("state")
    if dpt is None:
        dpt = location.raw.get("address").get("postcode")
    if dpt is None or location.raw.get("address").get("country") != "France":
        dpt = location.raw.get("address").get("country")
    cp = location.raw.get("address").get("postcode")
    country = location.raw.get("address").get("country")
    if cp is None:
        cp = ""
    lat = location.raw.get("lat")
    long = location.raw.get("lon")
    pyweatherfr.log.print_debug(
        ville + "-" + dpt + "-" + lat + "-" + long + "-" + country
    )

    return ville, dpt, lat, long, country


def clean_string(mystring):
    if mystring is None:
        return None
    retour = ""
    nfkd_form = unicodedata.normalize("NFKD", mystring)
    retour = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    retour = retour.replace(" ", "-").replace("'", "-").replace('"', "-")
    # if mystring!=retour:
    #    pyweatherfr.log.print_debug(mystring + " modifié en " + retour)
    return retour


def obtainfromip(url):
    resultat = url.read().decode()
    pyweatherfr.log.print_debug(resultat)
    data = json.loads(resultat)
    pyweatherfr.log.print_debug(str(json.dumps(data, indent=4, ensure_ascii=False)))
    ville = data["city"]
    if ville is None:
        ville = ""
    lat = str(data["latitude"])
    long = str(data["longitude"])
    dpt = data["state"]
    if dpt is None:
        dpt = ""
    country = str(data["country_name"])
    if country is None:
        country = ""
    return ville, dpt, lat, long, country


def obtain_city_data_from_ip():

    with urllib.request.urlopen("https://geolocation-db.com/json") as url:
        pyweatherfr.log.print_debug(
            "recherche de la localisation depuis https://geolocation-db.com/json"
        )
        return pyweatherfr.openstreetmap.obtainfromip(url)
