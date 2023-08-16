from Roja.Totes.core.utils.logger import *
import sys

def HandleError():
    logger.error("I am in Error Handler ~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    error = bool(True)
    serviceName = called_by()
    errorMessage = str(sys.exc_info()[1]) + "\n" + "###########\n" + str(sys.exc_info())
    logger.error("Error Occured in "+ called_by() + " " + errorMessage)
    logger.error("++++++++++++++++++++++++++++++++")

    result = {
               'error': error,
               'serviceName': serviceName,
               'errorMessage': errorMessage
             }
    return result, error