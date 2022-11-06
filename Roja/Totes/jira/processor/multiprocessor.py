
#from ..api.jira import GetJiraResponse
from Roja.Totes.core.utils.logger import *

def CalculateSubProcess(ProcessCount,LoopCount):
    log("Starting Function " + whoami())
    error=bool(False)
    errorMessage=None
    try:
        SubProcessCount = int(LoopCount)//int(ProcessCount)
        print("Quotient")
        print(SubProcessCount)
        SubProcessCount=SubProcessCount*ProcessCount
        SubProcessCount=LoopCount-SubProcessCount
    except:
        errorMessage = str(sys.exc_info()[1])
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print(whoami())
        print("Error Message: " + errorMessage)
        error = bool(True)  
    return SubProcessCount

# def MultiPoolCalls(queryArray,ProcessCount,BatchNumber):

#     print("I am in Call Jira as CJ")
#     pool = Pool(processes=ProcessCount)
#     start_time = millis()
#     response = pool.map(GetJiraResponse, queryArray)

#     print("\nTotal took " + str(millis() - start_time) + " ms\n")
#     print(response)
#     return response