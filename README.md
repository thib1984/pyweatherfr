# :sunny: :umbrella: :cloud: pyweatherfr

pyweatherfr affiche les prévisions méteo pour les communes françaises dans votre terminal. Il utilise l'API de MéteoFrance


# 🚀 Comment utiliser **pyweatherfr**

pyweatherfr affiche les prévisions météo sur 4 jours en se basant sur l'ip

pyweatherfr \[VILLE\]

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



## Autres options

  - ``-h/--help``    montrer l'aide
  - ``-u/--update``  update pyweatherfr
  - ``-c/--condensate``  condense la sortie
  - ``--nocolor``  désactive les couleurs et les emojis en sortie
  - ``-v/--verbose``  mode verbeux
  - ``--nocache``  supprime le cache de l'api meteo france avant l'appel
  
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
