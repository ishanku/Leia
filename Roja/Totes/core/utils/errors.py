from Roja.Totes.core.utils.logger import *
import sys

def HandleError():
    print("I am in Error Handler ~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    error=bool(True)
    serviceName = called_by()
    errorMessage=None
    errorMessage = str(sys.exc_info()[1]) + "\n" + "###########\n" + str(sys.exc_info())
    print("Error Occured in "+ called_by() + " " + errorMessage)
    print("++++++++++++++++++++++++++++++++")

    result = { error : error,
               serviceName :serviceName,
               errorMessage :errorMessage
             }
    return result, error