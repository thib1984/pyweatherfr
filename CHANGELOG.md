# A VENIR 5.3.0


- [x] supprimer --condensate
- [x] mode responsive / -f / / retrait -c

- [ ] emojis compatibles windows et linux
- [ ] ajouter cas d'erreurs dans les tests
- [ ] maj captures ecrans


- [ ] marqué en rouge les records de chaque zone
- [ ] integrer test sur heure soleil si ==3 si lumineux et ou petite pluie
- [ ] comparer boundingbox openstreetmap pour doublons
- [ ] clean code
- [ ] ajouter log version and co pour issue : https://github.com/thib1984/ytdlmusic/blob/main/ytdlmusic/print.py
- [ ] json formater pour le log/debug : https://www.freecodecamp.org/news/how-to-pretty-print-json-in-python/
- [ ] fichier log dans le dossier config pour completer le mode debug avec dates and co

# 5.2.5

- [x] limite les recherche par -j à 14j

# 5.2.4

- [x] restreint la province au japon
- [x] ajouter cas d'erreurs dans les tests
- [x] 5 sprigfiled en Jamaique mais 10 beaulieu en france. si munic/village/city/france on ne remonte pas

# 5.2.3
width
- [x] ip et remontée du state corrigé si non trouvé

# 5.2.2

- [x] completer flags courts et arguments courts
- [x] tokyo province japon
- [x] ne remonte que les city (ancenis ne doit pas remonter + beaulieu, il en faut 10 en France)

# 5.2.1

- [x] gère mieux les doublons de villes (meme ville, meme pays)
- [x] ajoute une options par pays pour affiner la recherche
- [x] remonte les hamlets


# 5.2.0

- [x] optimise les headers
- [x] --world + warning si ville world atteignable

# 5.1.3

- [x] correction is None
- [x] correction vent

# 5.1.2

- [x] W/m -> W/m2
- [x] changement warning pression basse 990 à 995
- [x] ajout lunettes
- [x] warning recherche par ip si vpn proxy
- [x] tronquer les données en -p les chercher en détaillés plutot que de mettre une limite haute ou basse
- [x] seule limite +15 jours (cf api meteo france)
- [x] limite le --past a un nb strcitement positif

# 5.1.1

- [x] retire le doublon d'appel pour la recherche par ip
- [x] gère l'absence de ville/dpt pour la recherche par ip
- [x] KeyboardInterrupt à mieux gérer
- [x] ajouter fleche vent

# 5.1.0


- [x] supprimer --world
- [x] correction erreur incorrecte pour rechercher gps et ip si or de France
- [x] bug code postal si non francais pyweatherfr 44000
- [x] maj pyweatherfr --help
- [x] pyweatherfr pekin --world -v ajouter au ci/cd
- [x] option multilang pour les villes


# 5.0.2

- [x] pyweatherfr pekin --world corriger
- [x] pyweatherfr -g 89 2.15 --world corriger


# 5.0.1

- [x] affiche un warning si ville hors france
- [x] précise l'erreur si ville non trouvée sans --world
- [x] remonte les villes en francais

# 5.0.0

- [x] headers meme si compact
- [x] recherche world

# 4.2.0

- [x] previsions -n ajouter data comme -j 
- [x] radiation plutot que couverture nuageuse

# 4.1.2

- [x] correction tz

# 4.1.1

- [x] -d ne fonctionne pas!


# 4.1.0

- [x] bug basse-terre
- [x] securiser la saisie du choix de ville : https://github.com/thib1984/ytdlmusic/blob/main/ytdlmusic/choice.py
- [x] gérer fuseau horaire en fonction de la ville (ex Nouméa): https://www.geeksforgeeks.org/get-time-zone-of-a-given-location-using-python/
- [x] bug --nocolor sur données ville
- [x] emoji pluie sur données courantes si ==0
- [x] corrige la possibilite de -p / -j / -n en //
- [x] test format et range si --date

- [x] changer cp to state pour la recherche par ip
- [x] améliorer unités from apimeteofrance
- [x] ameliorer affichage dpt from openstreetmap basse-terre
- [x] recap de la recherche dans le bloc ville
- [x] emoji nuit claire, nuit nuageuse
- [x] gestion des emojis aux largeurs fantaisistes

- [x] altitude from apimeteofrance
- [x] -utc ou -local pour la tz
- [x] -j sans param donnerait le jour actuel
- [x] recherche par date précise pour -j

## technic

- [x] test install cicd


# 4.0.1

- [x] améliorer infos villes si ville ou dpt non renseignés
- [x] limite le nb de decimales au GPS
- [x] maj --cache pour cache session en nocache
- [x] librairie manquante Numpy
- [x] bug ancenis
- [x] bug saint-etienne choix
- [x] bug saint-étienne/etienne
- [x] passer à 100j et non 99


# 4.0.0 

- [x] vérifier durée soleil hourly/daily
- [x] séparer durée soleil / couverture nuage
- [x] mode passé pour le générique
- [x] intégration geopy
- [x] retry sur erreur 502 de l'ancienne api

# 3.0.0 

- [x] mode passé pour récuperer les données de la veille avant veille
- [x] corrections libellés colonnes
- [x] mode debug sur l'api meteo france
- [x] supprimer -p et rechercher par code postal comme par ville
- [x] capture et rejeu de l'erreur a a l appel url
- [x] adaptation pring debug sur ancienne api

# 2.0.4

- [x] add nuage/soleil %

# 2.0.3

- [x] add hours of precipitations
- [x] clean code
- [x] refacto emoji

# 2.0.2

- [x] add some data and snow

# 2.0.1

- [x] add some data

# 2.0.0
- [x] switch to api meteo france

# 1.4.4

- [x] Allign sun
- [x] Delete pression
- [x] 0H00 -> 0H ?
# 1.4.2

- [x] Refacto and deduplicate code
- [x] date format "Lun. 15/11/2020"
- [x] arrondi affichage coordonnees GPS
- [x] pyweatherfr -s "La Rochelle" fix
- [x] Fix if no data (ex : Étival-lès-le-Mans) (bis)
- [x] pyweatherfr -p 29217 ? duplicate?
- [x] rework -c option
# 1.4.1

- [x] requests import
- [x] retrait altitude prévision (donnée incorrecte?)

# 1.4.0

- [x] fix emoji : Averses de neige faible
- [x] afficher altitude prévision
- [x] snow or rain for precipitations

# 1.3.1

- [x] Clean/reorder help message
- [x] bug duplicate postal : pyweatherfr -vp 29217

# 1.3.0

- [x] Fix emoji "Couvert avec averses"
- [x] Change -d to -j 
- [x] Clean/reorder help message

# 1.2.0

- [x] Add emoji rain (>0mm), wind(>30km.h), cold(<0), and warm(>30)
- [x] Fix emoji (ter)
- [x] Change "-" to "->" for temperature
- [x] Fix wrap and troncate columnar
- [x] Francisation (bis)
- [x] Allignement emoji not emoji

# 1.1.3

- [x] Fix emoji (bis)

# 1.1.2

- [x] Add white space with emoji
- [x] Fix emoji

# 1.1.1

- [x] Explain disable emoji -n
- [x] keep condition even if emoji

# 1.1.0

- [x] Add white space in -s option results
- [x] Emoji
- [x] Import unidecode
- [x] Add white space in -d -c option results

# 1.0.0

- [x] Search by longitude/latitude (-g/--gps)
- [x] Search by code postal (-p/--postal)
- [x] search town 
- [x] replace space with tiret
- [x] Fix if not a town at ip with no parameter
- [x] post in string
- [x] display sunrise + lat/long #"elevation":"480","sunrise":"07:31","sunset":"17:11"
- [x] francisation

# 0.0.8

- [x] Fix if no data (ex : Étival-lès-le-Mans)

# 0.0.7

- [x] Fix bug current conditions
- [x] Default search by ip information
- [x] Verbose mode

# 0.0.6

- [x] Clean color in compact mode
- [x] Fix colorama
- [x] Fix impports termcolor


# 0.0.5

- [x] Compact mode
- [x] One day mode (hour by hour)
- [x] Add color
- [x] Add rain

# 0.0.4

- [x] Unicode for matching names + city informations

# 0.0.3

- [x] Add test for matching names if param is not correct

# 0.0.2

- [x] Add basic forecast weather for next days

# 0.0.1

- [x] Initial feature with basic summary for a given town
