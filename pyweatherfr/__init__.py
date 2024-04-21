"""
pyweatherfr init
"""


from pyweatherfr.args import compute_args
from pyweatherfr.app import find
from pyweatherfr.update import update
import colorama


def pyweatherfr():
    """
    pyweatherfr entry point
    """
    
    colorama.init()

    args = compute_args()
    try:
        if args.update:
            update()
        else:
            find()
    except KeyboardInterrupt:
        exit(1)