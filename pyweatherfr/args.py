"""
pygitscrum argparse gestion
"""

import argparse
import sys


# Fonction de validation pour s'assurer que l'argument est un nombre positif
def positive_integer(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s n'est pas un nombre entier strictement positif" % value)
    return ivalue

class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ", ".join(action.option_strings) + " " + args_string

    def _format_args(self, action, default_metavar):
        get_metavar = self._metavar_formatter(action, default_metavar)
        if action.nargs == argparse.ONE_OR_MORE:
            return "%s" % get_metavar(1)
        else:
            return super(CustomHelpFormatter, self)._format_args(
                action, default_metavar
            )

def compute_args():
    """
    check args and return them
    """
    my_parser = argparse.ArgumentParser(
        description="pyweatherfr affiche les données méteo pour les communes françaises et mondiales dans votre terminal.",
        epilog="""
        Full documentation at: <https://github.com/thib1984/pyweatherfr>.
        Report bugs to <https://github.com/thib1984/pyweatherfr/issues>.
        MIT Licence.
        Copyright (c) 2021 thib1984.
        This is free software: you are free to change and redistribute it.
        There is NO WARRANTY, to the extent permitted by law.
        Written by thib1984.""",
        formatter_class=CustomHelpFormatter,
    )
    my_group = my_parser.add_mutually_exclusive_group()
    my_group.add_argument(
        "town",
        metavar="VILLE",
        type=str,
        nargs="?",
        help="affichage des données météo génériques par nom de ville ou code postal (uniquement communes francaises) -si absent, la VILLE est déduite de l'ip-",
    )
    my_2group = my_parser.add_mutually_exclusive_group()
    my_2group.add_argument(
        "-n",
        "--now",
        action="store_true",
        help="affichage des données météo actuelles, plutôt que les données génériques",
    )
    my_2group.add_argument(
        "-j",
        "--jour",
        metavar="JOUR",
        action="store",
        type=int,
        nargs='?',
        const=0,        
        help="affichage des données météo détaillées pour [JOUR] (0 pour le jour actuel, 1 pour le J+1, ..., -1 pour J-1, ...) plutôt que les données génériques",
    )
    my_2group.add_argument(
        "-d",
        "--date",
        metavar="DATE",
        action="store",
        type=str,      
        help="affichage des données météo détaillées pour [DAY] au format yyyy-mm-dd, plutôt que les données génériques",
    )    
    my_2group.add_argument(
        "-p",
        "--past",
        metavar="JOUR PASSE",
        action="store",
        type=positive_integer,
        default=0,
        help="affichage des données météo génériques depuis [JOUR PASSE] (10 pour J-10 à J-1, ...), plutôt que les données génériques",
    )         
    my_group.add_argument(
        "-g",
        "--gps",
        metavar=("LATITUDE", "LONGITUDE"),
        action="store",
        nargs=2,
        type=str,
        help="utilisation des coordonnées GPS à la place d'un nom de ville",
    )      
    my_parser.add_argument(
        "--nocolor",
        action="store_true",
        help="désactiver couleur et emojis en sortie -à utiliser en cas de problème d'affichage-",
    )
    my_parser.add_argument(
        "-w",
        "--world",
        action="store_true",
        help="activer la recherche hors France",
    )
    my_parser.add_argument(
        "-f",
        "--fullwidth",
        action="store_true",
        help="force l'affichage de toutes les données",
    )    
    my_parser.add_argument(
        "-l",
        "--lang",
        action="store_true",
        help="recherche (puis affiche) les villes avec leurs noms locaux",
    )     
    group = my_parser.add_mutually_exclusive_group()
    group.add_argument(
        "--pc",
        action="store_true",
        help="utilise l'heure locale du PC indépendamment de la ville cherchée",
    )
    group.add_argument(
        "--utc",
        action="store_true",
        help="utilise l'heure UTC",
    )          
    my_parser.add_argument(
        "--nocache",
        action="store_true",
        help="supprime le cache de l'api meteo france",
    )    
    my_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="mode verbeux",
    )              
    my_group.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="mise à jour de pyweatherfr",
    )


    args = my_parser.parse_args()
    return args
