# :sunny: :umbrella: :cloud: pyweatherfr

pyweatherfr affiche les prévisions méteo pour les communes françaises dans votre terminal. Il utilise les API de méteoFrance, https://www.prevision-meteo.ch et https://geolocation-db.com/json.


# 🚀 Comment utiliser **pyweatherfr**

pyweatherfr \[VILLE\]

exemple : ``pyweatherfr Grenoble`` affiche les prévisions météo pour Grenoble sur 4 jours

pyweatherfr -n \[VILLE\]

exemple : ``pyweatherfr -n Grenoble`` affiche les données météo pour Grenoble 

pyweatherfr \[TOWN\] -j [INT(0-3)]

exemple : ``pyweatherfr Grenoble -j 1`` affiche les prévisions météo détaillées pour Grenoble à J+1

pyweatherfr -p \[CODE_POSTAL\]

exemple : ``pyweatherfr -p  38700`` affiche les prévisions météo pour le code postal 38700

pyweatherfr -g \[COORDONNEES_GPS\]

exemple : `` pyweatherfr -g 45 5`` affiche les prévisions météo pour les coordonnées GPS (latitude : 45 et longitude : 5)


## Autres options

  - ``-h/--help``    montrer l'aide
  - ``-u/--update``  update pyweatherfr
  - ``-c/--condensate``  condense la sortie
  - ``--nocolor``  désactive les couleurs et les emojis en sortie
  - ``-v/--verbose``  mode verbeux
  - ``-C/--cache``  met à jour le cache du nom des villes (cache par défaut 30j)
  
# Démo

![image](./demo_01.png)

![image](./demo_02.png)

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
