from django.core.cache import cache
import sys
from Roja.Totes.core.utils.logger import log

def setRedisCache(CacheName,data,cache_timeout=9000):
    error=bool(False)
    errorMessage=None
    try:
        #print(rawData)
        print("Setting "+ CacheName +" Cache")          
        #cache.set(RawCacheName,rawData, timeout=cache_ttl)
        cache.set(CacheName,data)
        print("^^^^^^^^ " + CacheName +  " Cache Set ^^^^^^^")
    except:
        errorMessage = sys.exc_info()[1]
        log("Error Message While setting Cache " + errorMessage)
        error=bool(True)
    return error,errorMessage

def getRedisCache(CacheName):
    data = None
    error = bool(False)
    errorMessage = None
    try:
       print("Getting "+ CacheName +" Cache")
       data = cache.get(CacheName)
       print("^^^^^^^^ " + CacheName +  " Cache Retrived ^^^^^^^")
    except:
        errorMessage = sys.exc_info()[1]
        log("Error Message While getting Cache ")
        log(str(errorMessage))
        log("^^^^^~~~~~~~~~~~~~~~~~~~^^")
        error = bool(True)
    return data,error,errorMessage