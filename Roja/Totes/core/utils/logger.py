from datetime import datetime
import logging
import sys

# Create a logger for this file
logger = logging.getLogger(__file__)


def log(message, key='info', console=True, app_name=None):
    decorator = "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    if app_name is None:
        app_name = "Leia"

    if console:
        print(decorator)
        today = datetime.today().isoformat()
        print(today)
        print("App Name : " + app_name)
        print("Called By : " + called_by())
        print("Log Message : " + message)
        print(decorator)
    if key == "info":
        logger.info("App Name: " + app_name + "::::: Function Name: " + called_by() + ":::::  message: " + message)
    if key == "error":
        logger.error("App Name: " + app_name + "::::: Function Name: " + called_by() + ":::::  message: " + message)
    if key == 'debug':
        logger.debug("App Name: " + app_name + "::::: Function Name: " + called_by() + ":::::  message: " + message)


# noinspection PyProtectedMember
def whoami():
    return sys._getframe(1).f_code.co_name


# noinspection PyProtectedMember
def called_by():
    return sys._getframe(2).f_code.co_name
