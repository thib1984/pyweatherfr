"""
pyweatherfr init
"""


from pyweatherfr.args import compute_args
from pyweatherfr.app import app
from pyweatherfr.update import update
import pyweatherfr.log
import colorama


def pyweatherfr():
    """
    pyweatherfr entry point
    """
    
    colorama.init()

    try:
        if compute_args().update:
            update()
        else:
            app()
    except KeyboardInterrupt:
        pyweatherfr.log.my_colored(
                "erreur : traitement stoppé par le user", "red"
            )
        exit(1)