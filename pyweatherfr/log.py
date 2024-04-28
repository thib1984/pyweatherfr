import pyweatherfr.args

import termcolor


def print_debug(message):
    if pyweatherfr.args.compute_args().verbose:
        print("debug : " + message)


def my_colored(message, color):
    if pyweatherfr.args.compute_args().nocolor:
        return message
    return termcolor.colored(message, color)
