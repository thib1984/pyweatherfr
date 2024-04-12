# A VENIR

- [ ] améliorer infos villes si ville ou dpt non renseignés
- [ ] securiser la saisie du choix de ville
- [ ] mode full pour humidité/pression/soleil etc
- [ ] mode minimal pour temps / pluie uniquement (uniquement emoji si non nocolor)
- [ ] previsions -n ajouter data comme -j 
- [ ] gestion des emojis aux largeurs fantaisistes
- [ ] emoji nuit claire, nuit nuageuse
- [ ] recherche par date précise pour -j
- [ ] -j donnerait le jour actuel
- [ ] recap de la recherche dans le bloc ville
- [ ] clean code
- [ ] test install cicd

# 4.0.1

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
