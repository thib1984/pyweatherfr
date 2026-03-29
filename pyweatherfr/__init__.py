"""
pyweatherfr init
"""


from pyweatherfr.args import compute_args
from pyweatherfr.app import app
import pyweatherfr.log
import colorama


def pyweatherfr():
    """
    pyweatherfr entry point
    """
    
    colorama.init()

    try:
        app()
    except KeyboardInterrupt:
        pyweatherfr.log.my_colored(
                "erreur : traitement stoppé par le user", "red"
            )
        exit(1)