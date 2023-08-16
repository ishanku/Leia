from django.core.cache import cache
from django.core.cache import caches
from django.utils.connection import ConnectionProxy
from Roja.Totes.core.utils.file import *
import environ
from Config.basepath import *
import sys

def get_cache_name(alias):
  return ConnectionProxy(caches, alias)

env = environ.Env()

def setCache(CacheName, data, cache_timeout=100000, cache = "default"):
    park = bool(False)
    errorMessage = None
    try:
        logger.info("Setting " + CacheName + " Cache for " + cache)
        cache.set(CacheName, data)
        logger.info("^^^^^^^^ " + CacheName + " Cache Set in " + cache + "^^^^^^^")
    except:
        errorMessage = sys.exc_info()[1]
        logger.info("Error Message While setting Cache " +  str(cache))
        logger.info(str(errorMessage))
        park = bool(True)
    return park, errorMessage

def setRedisCache(CacheName, data, cache_timeout=100000):
    park = bool(False)
    errorMessage = None
    try:
        logger.info("Setting " + CacheName + " Cache")
        # cache = get_cache_name('FileCache')
        # cache.set(CacheName, data)
        #
        #  cache = get_cache_name('default')
        cache.set(CacheName, data)
        logger.info("^^^^^^^^ " + CacheName + " Cache Set in " + cache + "^^^^^^^")
    except:
        errorMessage = sys.exc_info()[1]
        logger.info("Error Message While setting Cache ")
        logger.info(errorMessage)
        park = bool(True)
    return park, errorMessage

# from django.views.decorators.cache import cache_page
# @cache_page(60 * 15, cache="FileCache")
# def setFileCache():


def getRedisCache(CacheName, dataIfNumber=0):
    logger.info("::::::::::::::::Redis URL " + env("REDIS_URL") + "***************")
    data = None
    park = bool(False)
    stepName = "Starting Get Cache For " + CacheName

    try:
        stepName = "Starting Get Cache For " + CacheName + "From File Cache"
        fileName =  CacheName + ".json"
        cache = get_cache_name('FileCache')
        data = cache.get(CacheName)
        if data is not None:
            stepName =  "::::::: Data Could not be extracted from File Cache ::::::::::"
        else:
            stepName = "::::::: Data Could not be extracted from File Cache ::::::::::"
            park = bool(True)
    except:
        stepName = "Error Occured in Reading File " + fileName
        print(stepName)


    logger.info(stepName)


    if park:
        park = False
        try:
            stepName = "Starting Get Cache For " + CacheName + "From Redis Cache"
            logger.info(stepName)
            cache = get_cache_name('default')
            data = cache.get(CacheName)

            if data is None:
                park = bool(True)
                dataIfNumber = dataIfNumber + 1
                stepName = "Raw data is null"
                logger.info(stepName + " Progressing to Next step <-> Call APIs")
            else:
                logger.info("^^^^^^^^ " + CacheName + " Cache Retrived ^^^^^^^with data length " + str(len(data)))

        except:
            errorMessage = sys.exc_info()[1]
            stepName = "Error Retriving the Cache  -> " + CacheName
            logger.info(stepName + " Data If : " + str(dataIfNumber))
            logger.info(str(errorMessage))
            logger.info("^^^^^~~~~~~~~~~~~~~~~~~~^^")
            park = bool(True)
    return data, park, dataIfNumber, stepName
