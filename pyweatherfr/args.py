"""
pygitscrum argparse gestion
"""

import argparse
import sys


def compute_args():
    """
    check args and return them
    """
    my_parser = argparse.ArgumentParser(
        description="pyweatherfr displays meteo for your town in France given in parameter",
        epilog="""
        Full documentation at: <https://github.com/thib1984/pyweatherfr>.
        Report bugs to <https://github.com/thib1984/pyweatherfr/issues>.
        MIT Licence.
        Copyright (c) 2021 thib1984.
        This is free software: you are free to change and redistribute it.
        There is NO WARRANTY, to the extent permitted by law.
        Written by thib1984.""",
    )
    my_group = my_parser.add_mutually_exclusive_group()
    my_group.add_argument(
        "town",
        metavar="VILLE",
        type=str,
        nargs="?",
        help="",
    )
    my_group.add_argument(
        "-p",
        "--post",
        action="store",
        metavar="CODE_POSTAL",
        type=str,
        help="",
    )  
    my_group.add_argument(
        "-s",
        "--search",
        action="store",
        metavar="RECHERCHE",
        type=str,
        help="ville ou code postal à rechercher",
    )        
    my_group.add_argument(
        "-g",
        "--gps",
        metavar=("LATITUDE", "LONGITUDE"),
        action="store",
        nargs=2,
        type=str,
        help="coordonnées GPS",
    )
    my_parser.add_argument(
        "-d",
        "--day",
        metavar="JOUR",
        action="store",
        type=int,
        default=-1,
        choices=range(0, 5),
        help="JOUR des prévision (0 pour le jour actuel, 1 pour le J+1, ...)",
    ) 
    my_parser.add_argument(
        "-n",
        "--nocolor",
        action="store_true",
        help="désactiver couleur en sortie",
    )
    my_parser.add_argument(
        "-c",
        "--condensate",
        action="store_true",
        help="condenser la sortie",
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
        help="update pyweatherfr",
    )


    args = my_parser.parse_args()
    return args
