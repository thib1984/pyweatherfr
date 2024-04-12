"""
pygitscrum argparse gestion
"""

import argparse
import sys


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
        description="pyweatherfr affiche les prévisions méteo pour les communes françaises dans votre terminal.",
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
        help="affichage des données météo par nom de ville ou code postal -si absent, la VILLE est déduite de l'ip-",
    )
    my_parser.add_argument(
        "-n",
        "--now",
        action="store_true",
        help="affichage des données météo détaillées actuelles",
    )
    my_parser.add_argument(
        "-j",
        "--jour",
        metavar="JOUR",
        action="store",
        type=int,
        default=1000,
        choices=range(-101, 4),
        help="affichage des données météo détaillées pour [JOUR] (0 pour le jour actuel, 1 pour le J+1, ..., -1 pour J-1, ...)",
    )
    my_parser.add_argument(
        "-p",
        "--past",
        metavar="JOUR PASSE",
        action="store",
        type=int,
        default=0,
        choices=range(1, 101),
        help="affichage des données météo génériques depuis [JOUR PASSE] (-10 pour J-10 à J-1, ...)",
    )         
    my_group.add_argument(
        "-g",
        "--gps",
        metavar=("LATITUDE", "LONGITUDE"),
        action="store",
        nargs=2,
        type=str,
        help="affichage des données météo par coordonnées GPS",
    )      
    my_parser.add_argument(
        "--nocolor",
        action="store_true",
        help="désactiver couleur et emojis en sortie -à utiliser en cas de problème d'affichage-",
    )
    my_parser.add_argument(
        "-c",
        "--condensate",
        action="store_true",
        help="condenser la sortie",
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
