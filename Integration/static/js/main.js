//let dateFormatter = d3.timeFormat("%Y-%m-%d");
//let dateParser = d3.timeParse("%Y-%m-%d");

let SelectedBarValue,SelectedBarTitle;
let parseDate = d3.timeParse("%Y-%m-%d");
let promises
let barData,rBarData,rTableData,detailedData;;

let dashboard='Performance Score'

what(dashboard)

function what(dashboard='Performance Score'){

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
// else if (dashboard==='Client Name'){
//
//    // d3.text('')
//
 }
//
Promise.all(promises)
     .then(function (data) {

        let Done, Rework, Pending, Assigned, Unassigned;


         Done = data[0]
         Rework = data[1]
         Pending = data[2]
         Assigned = data[3]
         Unassigned = data[4]

        singles(Done, Rework, Pending, Assigned, Unassigned);


          // let tData=data[5]
          // console.log("Logging Fine Data !")
          // console.log(tData);
          // let detailedData=data[6]

        //barData = new Wrangle(tData,"score","name")

        SelectedBarValue="score";
        SelectedBarTitle="Performance Score";

        //barchart=new BarVis("bar-chart",barData,"Performance Score","score")

        tableData = new Wrangle(tData,"score","date","name",["team"])
       //console.log(tableData);

        reloadBarChart(tableData);
        reloadTable(tableData);

        getHeaders(tableData[0]);
        buildTableStart(tableData[0],tableData,detailedData)
        buildTable(tableData,detailedData)

     })
     .catch(function (err) {
         console.log("Error Occurred :  " + err)
     });


function singlesHeader(){

    let sdiv=d3.selectAll("#singles-header")
    sdiv.append('div').attr("class","singles-header").html("Done")
    sdiv.append('div').attr("class","singles-header").html("Rework Done")
    sdiv.append('div').attr("class","singles-header").html("Pending")
    sdiv.append('div').attr("class","singles-header").html("Assigned")
    sdiv.append('div').attr("class","singles-header").html("UnAssigned")

}
function singles(totalDone,totalReworkDone,totalPending,totalAssigned,totalUnAssigned){

singlesHeader()
let sdiv=d3.selectAll("#singles")
sdiv.append('div').attr("class","singles").html(totalDone)
sdiv.append('div').attr("class","singles").html(totalReworkDone)
sdiv.append('div').attr("class","singles").html(totalPending)
sdiv.append('div').attr("class","singles").html(totalAssigned)
sdiv.append('div').attr("class","singles").html(totalUnAssigned)

    }