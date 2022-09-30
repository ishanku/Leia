from Roja.Totes.core.utils.logger import *
import sys


def check_key(data, search_value):
    for item in data:
        if search_value in item:
            return True
    return False


# Filters the JSON for required Fields and returns as JSON Array
# noinspection PyBroadException,SpellCheckingInspection
def process_issues(data):
    log("Starting Function " + whoami())
    print("Length of the Array " + str(len(data)))
    status = bool(True)

    message = None
    return_data = []
    base_return = []
    iteration = 0
    page_count = None
    claim_count = None
    error_count = None
    other_count = None
    weight = None
    issue_url = None
    time_spent = None
    task_name = None
    parent_key = None
    parent_summary = None
    parent_status = None
    parent_description = None
    parent_priority = None
    parent_issue_type = None
    parent_issue_id = None
    position = "Starting issue Processor"

    try:
        data_length = str(len(data))
        log("Array Builder Received Data Length " + data_length)
        for issueArray in data:
            if iteration < len(data):
                log("No of Issues in the First Level " + str(len(issueArray)))
                for issue in issueArray:
                    try:
                        print("#################################################  " + str(iteration) + "^^^^^^")

                        issue_key = issue['key']
                        issue_id = issue_key.split("-")[1]
                        field_data = issue['fields']
                        assignee = field_data['assignee']
                        if assignee is not None:
                            account_id = assignee['accountId']
                            display_name = assignee['displayName']
                            updated_date = field_data['updated']
                            updated_date = updated_date.split("T")[0]
                            completed_date = field_data['customfield_10030']
                            issue_date = completed_date
                            created_date = field_data['created']
                            created_date = created_date.split("T")[0]
                            score = field_data['customfield_10060']
                            team_name = field_data['customfield_10089']
                            if check_key(field_data, 'time_spent'):
                                time_spent = field_data['time_spent']
                            print("Extracted Phase 1 ~~~~~~~~~~~~~~~~~~~~")
                            #################################################
                            if check_key(field_data, "parent"):
                                parent = field_data['parent']
                            else:
                                parent = None
                            print("Extracted Phase 2 Parent Main ~~~~~~~~~~~~~~~~~~~~")
                            if parent is not None:
                                parent_key = parent['key']
                                parent_fields = parent['fields']
                                if parent_fields is not None:
                                    parent_summary = parent_fields['summary']
                                    parent_status = parent_fields['status']
                                    if parent_status is not None:
                                        parent_status = parent_status['name']
                                        parent_description = parent_fields['status']['description']
                                    parent_priority = parent_fields['priority']['name']
                                    parent_issue_id = parent_fields['issuetype']['id']
                                    parent_issue_type = parent_fields['issuetype']['name']
                                print("Extracted Phase 2 ~~~~~~~~~~~~~~~~~~~~")

                            client_name = field_data['customfield_10038']
                            if client_name is not None:
                                client_name = client_name['value']
                            if check_key(field_data, "customfield_10035"):
                                task_name = field_data["customfield_10035"]
                            if check_key(field_data, "customfield_10031"):
                                page_count = field_data['customfield_10031']
                            if check_key(field_data, "customfield_10032"):
                                claim_count = field_data['customfield_10032']
                            if check_key(field_data, "customfield_10051"):
                                error_count = field_data['customfield_10051']
                            if check_key(field_data, "customfield_10042"):
                                other_count = field_data['customfield_10042']
                            if check_key(field_data, "customfield_10068"):
                                weight = field_data['customfield_10068']
                                if weight is not None:
                                    weight = weight['value']

                            sub_task_type = field_data['customfield_10067']
                            if sub_task_type is not None:
                                sub_task_type = sub_task_type['value']
                            claim_type = field_data['customfield_10100']
                            if claim_type is not None:
                                claim_type = claim_type['value']
                            issue_type = field_data['issuetype']

                            if issue_type is not None:
                                issue_type = issue_type['name']
                                issue_url = field_data['issuetype']['iconUrl']
                            print("Extracted Phase 2 TaskTypes ~~~~~~~~~~~~~~~~~~~~")
                            creator = field_data['creator']
                            if creator is not None:
                                creator = creator['displayName']
                            reporter = field_data['reporter']
                            if reporter is not None:
                                reporter = reporter['displayName']
                            log_status = field_data['customfield_10058']
                            if log_status is not None:
                                log_status = log_status['value']
                            project_name = field_data['project']['name']
                            project_key = field_data['project']['key']
                            # description=field_data['description']['content']
                            # description=description['content']['text']
                            description = None
                            priority = field_data['priority']['name']
                            status = field_data['status']['name']
                            status_category = field_data['status']['statusCategory']['key']
                            print("Extracted Phase 2 Status ~~~~~~~~~~~~~~~~~~~~")
                            resolution = field_data['resolution']
                            if resolution is not None:
                                resolution = resolution['description']
                                resolution_status = field_data['resolution']['name']
                            else:
                                resolution_status = None
                            print("Extracted Phase 2 Resolution ~~~~~~~~~~~~~~~~~~~~")
                            print("Extracted Phase 3 ~~~~~~~~~~~~~~~~~~~~")
                            if team_name is not None:
                                team_name = team_name['value']
                                if issue_date is not None:
                                    if score is not None:
                                        name = display_name
                                        activity_date = issue_date
                                        performance_scores = score
                                        team = team_name
                                        print("#########@@@@@@@@@@@@@@################")
                                        base_build = {"name": name, "date": activity_date, "score": performance_scores,
                                                      "team": team}
                                        build = {
                                            "accountId": account_id, "name": name, "date": activity_date,
                                            "score": performance_scores, "team": team,
                                            "completed": completed_date,
                                            "updated": updated_date,
                                            "created": created_date,
                                            "clientName": client_name,
                                            "issueKey": issue_key,
                                            "issueId": issue_id,
                                            "issueType": issue_type,
                                            "issue_url": issue_url,
                                            "task_name": task_name,
                                            "claimType": claim_type,
                                            "subTaskType": sub_task_type,
                                            "claim_count": claim_count,
                                            "error_count": error_count,
                                            "other_count": other_count,
                                            "page_count": page_count,
                                            "time_spent": time_spent,
                                            "weight": weight,
                                            "priority": priority,
                                            "status": status,
                                            "statusCategory": status_category,
                                            "creator": creator,
                                            "reporter": reporter,
                                            "logStatus": log_status,
                                            "description": description,
                                            "project": {
                                                "name": project_name,
                                                "key": project_key
                                            },
                                            "resolution": {
                                                "status": resolution_status,
                                                "description": resolution
                                            },
                                            "parent": {
                                                "key": parent_key,
                                                "summary": parent_summary,
                                                "status": parent_status,
                                                "description": parent_description,
                                                "priority": parent_priority,
                                                "issue_type": parent_issue_type,
                                                "issueId": parent_issue_id
                                            }
                                        }
                                        base_return.append(base_build)
                                        return_data.append(build)
                                        iteration = iteration + 1
                    except KeyError:
                        print(str(sys.exc_info()[1]))
                        continue
        # df=pd.json_normalize(return_data)
        # df=df.sort_values(['name','date'])
        # df['score']=pd.to_numeric(df['score'])
        # df=df.groupby(['name','date'])['score'].sum()
        # return_data=df.to_json()
        print("Total Given Length ----: " + data_length)
    except:
        message = str(sys.exc_info()[1]) + "\n" + "###########\n" + str(sys.exc_info())
        status = bool(False)
        print("Error Occured in Issue Processor " + message)
        print("++++++++++++++++++++++++++++++++")
    return return_data, base_return, status, message
