"""
pyweatherfr init
"""


import pyweatherfr.args
import pyweatherfr.pyweatherfr
import pyweatherfr.update

import colorama


def pyweatherfr():
    """
    pyweatherfr entry point
    """
    
    colorama.init()

    try:
        if pyweatherfr.args.compute_args().update:
            pyweatherfr.update.update()
        else:
            pyweatherfr.pyweatherfr.find()
    except KeyboardInterrupt:
        exit(1)