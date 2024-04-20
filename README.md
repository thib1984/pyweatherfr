# :sunny: :umbrella: :cloud: pyweatherfr

pyweatherfr affiche les prévisions méteo pour les communes françaises (voire mondiales) dans votre terminal. Il utilise l'API de MéteoFrance et d'OpenStreetMap.


# 🚀 Comment utiliser **pyweatherfr**

pyweatherfr \[VILLE\]

exemple : ``pyweatherfr`` affiche les prévisions météo pour la ville trouvée en se basant sur l'ip

exemple : ``pyweatherfr Grenoble`` affiche les prévisions météo pour Grenoble sur 4 jours

exemple : ``pyweatherfr 38700`` affiche les prévisions météo pour le code postal 38700

pyweatherfr -n \[VILLE\]

exemple : ``pyweatherfr -n Grenoble`` affiche les données météo pour Grenoble 

pyweatherfr -g \[COORDONNEES_GPS\]

exemple : `` pyweatherfr -g 45 5`` affiche les prévisions météo pour les coordonnées GPS (latitude : 45 et longitude : 5)

pyweatherfr \[TOWN\] -j [INT]

exemple : ``pyweatherfr Grenoble -j 1`` affiche les prévisions météo détaillées pour Grenoble à J+1

exemple : ``pyweatherfr Grenoble -j -2`` affiche les données météo détaillées pour Grenoble à J-2

attention : le paramètre peut être compris entre - 100 et 3

pyweatherfr \[TOWN\] -p [INT]

exemple : ``pyweatherfr Grenoble -p 10`` affiche les données météo détaillées pour Grenoble de J-10 à J-1

pyweatherfr \[TOWN\] -d [STR]

exemple : ``pyweatherfr Grenoble -d 2024-03-30`` affiche les données météo détaillées pour Grenoble au 30/03/2024


## Autres options

  - ``-w/--world``  recherche la ville en pramètre dans le monde et non seulement en France
  - ``-h/--help``    montrer l'aide
  - ``-u/--update``  update pyweatherfr
  - ``--nocolor``  désactive les couleurs et les emojis en sortie
  - ``-v/--verbose``  mode verbeux
  - ``--nocache``  supprime le cache de l'api meteo france avant l'appel
  - ``--utc``    utilise l'heure utc dans les previsions au lieu de l'heure locale de la ville
  - ``--pc``    utilise l'heure du pc dans les previsions au lieu de l'heure locale de la ville
  - ``-l/--lang`` recherche (puis affiche) les villes avec leurs noms locaux
  - ``-f/--fullwidth`` affiche toutes les données y compris si la largeur du terminal est trop petite  

# Démo

![image](https://github.com/thib1984/pyweatherfr/assets/45128847/9b0c5353-8e1b-4dfa-86b5-e2d5472a6cf2)

![image](https://github.com/thib1984/pyweatherfr/assets/45128847/e92ceca0-e542-4c15-8eea-6a6067d55af8)

![image](https://github/thib1984/pyweatherfr/assets/45128847/2d938bcd-3ee9-432b-a02d-080147ccc974)

![image](https://github.com/thib1984/pyweatherfr/assets/45128847/b75a6a03-74fa-42b4-8cf5-24b15f35fa21)


# ⚙️ Install

See [this page](INSTALL.md)

# :construction_worker: Contribution

See [this page](CONTRIBUTING.md)

# :package: Changelog

See [this page](CHANGELOG.md)


# License

MIT License

Copyright (c) 2021 [thib1984](https://github.com/thib1984)

See [this page](LICENSE.txt) for details
