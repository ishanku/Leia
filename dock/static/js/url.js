console.log(window.location.href)
//let serverName=window.location.protocol + "//" + window.location.hostname + ":" + window.location.port
let serverName=window.location.href
let wakeData=serverName + "Jira/issues/fine"
let wakeDataExtract=serverName + "Jira/issues/extract"
let totalDone= serverName + "Jira/total/Done"
let totalReworkDone= serverName + "Jira/total/Rework Done"
let totalPending= serverName + "Jira/total/Pending"
let totalAssigned= serverName + "Jira/total/Assigned"
let totalUnAssigned= serverName + "Jira/total/Unassigned"


////////////////////// Jira Site Name Specific
let siteURL="https://applebillingcredentialing.atlassian.net/browse/"