"""
pyweather init
"""


from pyweather.args import compute_args
from pyweather.pyweather import find
from pyweather.update import update

def pyweather():
    """
    pyweather entry point
    """
    args = compute_args()


    if args.update:
        update()
    if args.town:
        find(args.town)
