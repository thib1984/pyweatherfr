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
        metavar="town",
        type=str,
        nargs="?",
        help="town",
    )
    my_parser.add_argument(
        "-d",
        "--day",
        metavar="[day]",
        action="store",
        type=int,
        default=-1,
        choices=range(0, 5),
        help="set the day to see (min=0, max=5, 0 for actual day)",
    ) 
    my_parser.add_argument(
        "-n",
        "--nocolor",
        action="store_true",
        help="disable colors in sysout",
    )
    my_parser.add_argument(
        "-c",
        "--condensate",
        action="store_true",
        help="condensate sysout",
    )
    my_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="debug mode",
    )              
    my_group.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="update pyweatherfr",
    )


    args = my_parser.parse_args()
    return args
