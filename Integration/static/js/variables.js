// ------------- Atlassian API URL --------------------------------------------------------------
let apiPath ='/rest/api/3/search'
let jql ='parent=null and Status='
let baseUrl = apiPath + '?jql=' + jql
// ------------- Set Status --------------------------------------------------------------
let status = ['Done','Rework Done','Pending','Assigned','Unassigned']
let statusValues = []

// ------------- Set Table and Chart Variables --------------------------------------------------------------
let tableData;
let thead = d3.select("thead");
let tbody = d3.select("tbody");
let odd= new Boolean(true);
let divrow=""
let divcols=""
let loggerKey=true

let functionText=[]
let headerarray=[]
let filtervalarray=[]
let filteredOutput = []


let SelectedBarValue,SelectedBarTitle;
let parseDate = d3.timeParse("%Y-%m-%d");
let promises
let barData,rBarData,rTableData,detailedData;;
let dashboard='Performance Score'
