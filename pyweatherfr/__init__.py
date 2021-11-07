"""
pyweatherfr init
"""


from pyweatherfr.args import compute_args
from pyweatherfr.pyweatherfr import find
from pyweatherfr.update import update
import colorama

def pyweatherfr():
    """
    pyweatherfr entry point
    """
    args = compute_args()
    colorama.init()
    if args.day and (args.town is None):
        print("--day requires --town")
        exit(1)
    if args.update:
        update()
    if args.town:
        find(args.town)
