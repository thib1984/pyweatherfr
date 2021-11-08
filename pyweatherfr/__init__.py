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
    
    colorama.init()

    args = compute_args()
    if args.update:
        update()
    else:
        find()
