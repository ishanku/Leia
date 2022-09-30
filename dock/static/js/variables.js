// ------------- Atlassian API URL --------------------------------------------------------------
let apiPath ='/rest/api/3/search'
let jql ='parent=null and Status='
let baseUrl = apiPath + '?jql=' + jql
// ------------- Set Status --------------------------------------------------------------
let status = ['Done','Rework Done','Pending','Assigned','Unassigned']
let statusValues = []