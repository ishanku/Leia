console.log("Welcome to Totesoft Dashboard")

what(dashboard)

function what(dashboard='Performance Score'){

    console.log("starting the function for : " , dashboard)

    if (dashboard==='Performance Score')
        {
            promises = [

                 d3.text(totalDone),              //0
                 d3.text(totalReworkDone),        //1
                 d3.text(totalPending),           //2
                 d3.text(totalAssigned),          //3
                 d3.text(totalUnAssigned),        //4
                 d3.json(wakeData),                  //5
                 d3.json(wakeDataExtract)            //6
            ];
        }
}

function reloadBarChart(){
        createVis(rBarData)
}

//
Promise.all(promises)
    .then(function (data) {
        initMainPage(data)
    })
    .catch(function (err) {
        console.log(err)
    });

function initMainPage(data) {

    // log data
    //console.log('check out the data', data[5]);

    // Init Single Box
    Done = data[0]
    Rework = data[1]
    Pending = data[2]
    Assigned = data[3]
    Unassigned = data[4]

    //-----------------------------------------------------------------------------------------------Init Singles   ---- 1

    singles(Done, Rework, Pending, Assigned, Unassigned);                                            //firstRow.js

    //-----------------------------------------------------------------------------------------------Init Table Data
    let tData=data[5]
    detailedData=data[6]

    //----------------------------------------------------------------------------------------------- Data Wrangling For Barchart
    console.log('Starting wrangle for bardata');

    barData = new Wrangle(tData,"score","name")

   //----------------------------------------------------------------------------------------------- Data Wrangling For Table (js/util/wrangler.js)
    console.log('Starting wrangle for name wise');
    let getTHeader, getTRows,nameWise = new Wrangle(tData, "score","name", "date",["team"],true)

    //console.log(nameWise)
    //Init table
    tableData = new Wrangle(tData,"score","date","name",["team"])
    //console.log(tableData);

    SelectedBarValue="score";
    SelectedBarTitle="Performance Score";

    barData.forEach(function(bData) {

        bData.score += bData.score

    });
    //-----------------------------------------------------------------------------------------------Init Bar Chart   ---- 2
    barchart = new CircleVis("bar-chart",barData,SelectedBarTitle,SelectedBarValue)

    rTableData = tableData
    rBarData = tableData

   //-----------------------------------------------------------------------------------------------Init Table Load   ---- 3

    loadTable(tableData,detailedData)
    //scoreTable(detailedData,"score-table")
}
//Table in the Third Row
function loadTable(tableData,detailedData)
{
            // getHeaders(tableData[0]);
            StartBuildingTablePrerequisites(tableData[0],tableData,detailedData,"myDynamicFilterTable") //js/table/startBuild
            BuildTable(tableData,detailedData,"myDynamicTable")                   //js/table/startBuild

}
