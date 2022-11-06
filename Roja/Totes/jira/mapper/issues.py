import sys
from Roja.Totes.core.utils.logger import *
from Roja.Totes.core.utils.date import getCurrentDateISO, getDate7Days, getDateLastMonth
import pandas as pd
import json


def rawArray(dataArray):
    rawData=[]
    for d in dataArray:
        for r in d:
            rawData.append(r)
    return rawData

## Filters the JSON for required Fields and returns as JSON Array
def arrayBuilder(data):
    log("Starting Function " + whoami())
    print("Length of the Array " + str(len(data)))
    error = bool(False)
    errorMessage=None
    returnData=[]
    baseReturn=[]
    iteration=0
    claimCount=None
    errorCount=None
    otherCount=None
    weight=None
    issueURL=None
    timespent=None
    
    try:
        dataLength=str(len(data))
        log("Array Builder Received Data Length " + dataLength)
        for issueArray in data:
            if iteration==0:
                log("No of Issues in the First Level " + str(len(issueArray)))
                for issue in issueArray:
                    try:
                        print("#################################################  " + str(iteration) + "^^^^^^")
                        
                        issueKey=issue['key']
                        issueId=issueKey.split("-")[1]
                        fieldData=issue['fields']
                        assignee=fieldData['assignee']
                        if assignee is not None:
                            accountId=assignee['accountId']
                            displayName=assignee['displayName']
                            updatedDate=fieldData['updated']
                            updatedDate=updatedDate.split("T")[0]
                            completedDate=fieldData['customfield_10030']
                            issueDate=completedDate
                            createdDate=fieldData['created']
                            createdDate=createdDate.split("T")[0]
                            score=fieldData['customfield_10060']
                            teamName=fieldData['customfield_10089']
                            if checkKey(fieldData,'timespent'):
                                timespent=fieldData['timespent']
                            print("Extracted Phase 1 ~~~~~~~~~~~~~~~~~~~~")
                            #################################################
                            if checkKey(fieldData,"parent"):
                                parent=fieldData['parent']
                            else:
                                parent=None
                            print("Extracted Phase 2 Parent Main ~~~~~~~~~~~~~~~~~~~~")
                            if parent is not None:
                                parentKey=parent['key']     
                                parentFields=parent['fields']
                                if parentFields is not None:
                                    parentSummary=parentFields['summary']
                                    parentStatus=parentFields['status']
                                    if parentStatus is not None:
                                        parentStatus=parentStatus['name']
                                        parentDescription=parentFields['status']['description']
                                    parentpriority=parentFields['priority']['name']
                                    parentissueID=parentFields['issuetype']['id']
                                    parentissueType=parentFields['issuetype']['name']
                                print("Extracted Phase 2 ~~~~~~~~~~~~~~~~~~~~")

                            clientName=fieldData['customfield_10038']
                            if clientName is not None:
                                clientName=clientName['value']
                            if checkKey(fieldData,"customfield_10031"):
                                pageCount=fieldData['customfield_10031']
                            if checkKey(fieldData,"customfield_10032"):
                                claimCount=fieldData['customfield_10032']
                            if checkKey(fieldData,"customfield_10051"):
                                errorCount=fieldData['customfield_10051']
                            if checkKey(fieldData,"customfield_10042"): 
                                otherCount=fieldData['customfield_10042']
                            if checkKey(fieldData,"customfield_10068"):
                                weight=fieldData['customfield_10068']
                                if weight is not None:
                                    weight=weight['value']

                            subTaskType=fieldData['customfield_10067']
                            if subTaskType is not None:
                                subTaskType=subTaskType['value']
                            claimType=fieldData['customfield_10100']
                            if claimType is not None:
                                claimType=claimType['value']
                            issueType=fieldData['issuetype']
                            
                            if issueType is not None:
                                issueType=issueType['name']
                                print(issueType)
                                issueURL=fieldData['issuetype']['iconUrl']
                            print("Extracted Phase 2 TaskTypes ~~~~~~~~~~~~~~~~~~~~") 
                            creator=fieldData['creator']
                            if creator is not None:
                                creator=creator['displayName']
                            reporter=fieldData['reporter']
                            if reporter is not None:
                                reporter=reporter['displayName']
                            logStatus=fieldData['customfield_10058']
                            if logStatus is not None:
                                logStatus=logStatus['value']
                            projectName=fieldData['project']['name']
                            projectKey=fieldData['project']['key']
                            #description=fieldData['description']['content']
                            #description=description['content']['text']
                            description=None
                            priority=fieldData['priority']['name']
                            status=fieldData['status']['name']
                            statusCategory=fieldData['status']['statusCategory']['key']
                            print("Extracted Phase 2 Status ~~~~~~~~~~~~~~~~~~~~")              
                            resolution=fieldData['resolution']
                            if resolution is not None:
                                resolution=resolution['description']
                                resolutionStatus=fieldData['resolution']['name']
                            else:
                                resolutionStatus=None
                            print("Extracted Phase 2 Resolution ~~~~~~~~~~~~~~~~~~~~") 
                            print("Extracted Phase 3 ~~~~~~~~~~~~~~~~~~~~")
                            if teamName is not None:
                                teamName=teamName['value']    
                                if issueDate is not None:
                                    if score is not None:
                                        name=displayName
                                        activityDate=issueDate
                                        performanceScores=score
                                        team=teamName
                                        print("#########@@@@@@@@@@@@@@################")
                                        baseBuild={  "name": name, "date" : activityDate,"score": performanceScores, "team" : team}
                                        build={
                                            "accountId" : accountId, "name": name, "date" : activityDate,"score": performanceScores, "team" : team, 
                                                "completed" : completedDate,
                                                "updated" : updatedDate,
                                                "created" : createdDate,
                                                "clientName" : clientName,
                                                "issueKey" : issueKey,
                                                "issueId":issueId,
                                                "issueType": issueType,
                                                "issueUrl":issueURL,
                                                "claimType": claimType,
                                                "subTaskType": subTaskType,
                                                "claimCount": claimCount,
                                                "errorCount": errorCount,
                                                "otherCount": otherCount,
                                                "pageCount" : pageCount,
                                                "timespent" : timespent,
                                                "weight" : weight,
                                                "priority":priority,
                                                "status":status,
                                                "statusCategory":statusCategory,
                                                "creator": creator,
                                                "reporter":reporter,
                                                "logStatus" : logStatus,
                                                "description" : description,
                                                "project" : {
                                                "name" : projectName,
                                                "key" : projectKey 
                                                }, 
                                                "resolution":{
                                                    "status":resolutionStatus,
                                                "description": resolution
                                                },
                                                    "parent": {
                                                            "key": parentKey,    
                                                            "summary": parentSummary,
                                                            "status" : parentStatus,
                                                            "description": parentDescription,
                                                            "priority" : parentpriority,
                                                            "issuetype": parentissueType,
                                                            "issueId" : parentissueID
                                                    }
                                            }
                                        baseReturn.append(baseBuild)
                                        returnData.append(build)
                                        iteration=iteration+1
                    except KeyError: 
                        print(str(sys.exc_info()[1]))
                        continue
        # df=pd.json_normalize(returnData)
        # df=df.sort_values(['name','date'])
        # df['score']=pd.to_numeric(df['score'])
        # df=df.groupby(['name','date'])['score'].sum()
        # returnData=df.to_json()
        print("Total Given Length ----: " + dataLength)
    except:
        errorMessage = str(sys.exc_info()[1]) + "\n" + "###########\n" + str(sys.exc_info())
        error = bool(True) 
        print("Error Occured in Array Builder" + errorMessage)
        print("++++++++++++++++++++++++++++++++")
    return returnData, baseReturn, errorMessage, error


def SumRequired(data):
    errorMessage=None
    error=bool(False)
    givenData=data
    try:
        df=pd.json_normalize(data)
        result=pd.DataFrame()
        for d in df.date.unique():
            for n in df.name.unique():
                score=df.loc[(df.name==n) & (df.date==d)]['score'].sum()
                team=df.loc[(df.name==n) & (df.date==d)]['team'].unique()
                temp=pd.DataFrame({"date":d, "name": n, "score": score,"team":team})
                result=pd.concat([result,temp])
        data=result.reset_index(drop=True)
        data=json.loads(data.to_json(orient='records'))
    except:
        errorMessage = str(sys.exc_info()[1])
        error = bool(True) 
        print("Error Message From "+ whoami() + " ----- " + errorMessage)
    return data,errorMessage,error


def checkKey(data, search_value):
    for item in data:
        if search_value in item:
            return True
    return False

def buildTimeQuery(key='Created',value='thisweek'):
 
    query=""
    result=None
    if value=='thisweek':
        query="startOfWeek()"
    if value=='today':
        query='startOfDay()'
    if value=='fromyesterday':
        query='startOfDay(-1)'
    if value=='yesterday':
        query=['startOfDay(-1)','endOfDay(-1)']
    if value=="Last7Days":
        query="startOfDay(-7)"
    else:
        query="startOfWeek()"

    # if query.length==2:
    #     result="'" + key + "'" +  ">=" + query[0] + " and " + key + "<=" +query[1]
    # else:
    result="'" + str(key) + "'" + ">=" + query 
    return result

def queryBuilder(key="Completed Date",startAt=0,duration=None):
    log("Starting Function " + whoami())

    key="Completed Date"
    if duration is not None:
        timeQuery=buildTimeQuery(key,"thisweek")
    else:
        timeQuery=buildTimeQuery(key,"Last7Days")

    jql="jql="
    jql=jql + "('Performance Score'>0 or 'Performance Score'<0)"
    jql=jql + " and " + timeQuery
    jql=jql + "&maxResults=100&startAt=" + str(startAt)

    return jql
