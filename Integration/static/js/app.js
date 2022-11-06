// from data.js
let tableData;
let thead = d3.select("thead");
let tbody = d3.select("tbody");
let odd=new Boolean(true);
let divrow=""
let divcols=""
let loggerKey=true

let functionText=[]
let headerarray=[]
let filtervalarray=[]
let filteredOutput = []


function getHeaders(tData){
  headerarray=[]
  Object.keys(tData).forEach((key) => {
  headerarray.push(key);
  });
}

function buildTableStart(tDataHead,tData,dData){
tableData=tData
detailedData=dData

  d3.select("#filterdrop").remove();

  //Building the Filters 
  var divselect = d3.select('#myDynamicFilterTable').append('div')
                      .attr("id", "filterdrop")
                      .attr("class","form-group col-xs-1");

  thead = d3.select("thead");
  let row = thead.append("tr");

  //==========================For Every Column Loop=============================
  //Object A------------------
  Object.keys(tDataHead).forEach((key) => 
  {

    let cell = row.append("th").attr("class","thlabel");
    let fkey=key;
    let optionvalue= []
    let optionflag=new Boolean(false);

    let optionhtml = '<option value="'+ key  +'">  --' +  key + '--  </option>'
    let selecthtml='<select class="form-control form-control-sm" d="select-key-'+ key +'" name="select-'+ key +'">'+ optionhtml +'</select>'

    if (odd == Boolean(true))
    {
 
      divrow = divselect.append('div').attr("class","row presence-row");
      divcols = divrow.append('div').attr("class","presence-cols")
      
      functionText.push("d3.select('#select-"+ key+ "').on('change', function() {\nconsole.clear();\nfiltervalarray=[];\nfilterKey = '"+ key+ "';\nfilterData = d3.select(this).property('value');\n//alert(filterData);\nvar i;\nfor (i=0 ;i < headerarray.length ; i ++){ var fvalue=d3.select("+"'"+"#select-"+"'"+"+headerarray[i]).property('value');\nif (!!fvalue){filtervalarray.push(headerarray[i]+' : '+fvalue);}\n };\nfilteredOutput = [];\nhandleBuild();\n//tableData.filter(tableFilter);\n//buildTable(filteredOutput,detailedData);\n});\n")
      odd=false
    }
    else
    {

      divcols = divrow.append('div').attr("class","presence-cols")
      
      functionText.push("d3.select('#select-"+ key+ "').on('change', function() {\nconsole.clear();\nfiltervalarray=[];\nfilterKey = '"+ key+ "';\nfilterData = d3.select(this).property('value');\n//alert(filterData);\nvar i;\nfor(i=0 ; i < headerarray.length ; i ++){ var fvalue=d3.select("+"'"+"#select-"+"'"+"+headerarray[i]).property('value');\nif (!!fvalue){filtervalarray.push(headerarray[i]+' : '+fvalue);}\n  };\nfilteredOutput = [];\nhandleBuild();\n//tableData.filter(tableFilter);\n//buildTable(filteredOutput,detailedData);\n});\n")
      odd=true
    }

    var label = divcols.append("label").attr("id","label-" + key).attr("for","select-key" + key).attr("class","presence-select-label").text(key);
    var selectoption = divcols.append('select').attr("class","presence-select").attr("id","select-"+key);
    var	optionlist = selectoption.append('option').attr("value","").text("--" + key + "--");

    //Object B------------------Fill the Values for Column
    Object.entries(tData).forEach(([key, value]) => {
     //Object C------------------
      Object.keys(value).forEach(key => {
       
              if (fkey===key)
              {
                Object.entries(value).forEach(([key, value]) => {
                    //console.log(value);

                    if (fkey==key){
                    
                      var optionflag=Boolean(false);

                      for (i=0; i<optionvalue.length; i ++)
                      {
                          if (optionvalue[i] == value)
                          {
                            optionflag=Boolean(true)
                          }
                      }
                        if (optionflag != Boolean(true))
                        {

                        optionvalue.push(value);
                        optionhtml = optionhtml + '<option value="' + value +'">'+ value + '</option>'
                        selecthtml='<select class="form-control form-control-sm" id="select-key-'+ key +'" name="select-key">' + optionhtml + '</select>'
                        
                        let htext= key+ '<br>' + selecthtml
                        cell.html(htext);

                        let	optionlist = selectoption.append('option').attr("value",value).text(value);

                        // Reset the Option Flag
                        optionflag=Boolean(false);
                        }
                    }
                  });
              }
    //Object C------------------  
            });
    //Object B------------------
    });
    //Object A------------------
  });
  smartScript(functionText)
}

    
  function handleBuild()
  {
        inputData = tableData;
        for (i=0;i<filtervalarray.length;i++){

          filterKey=filtervalarray[i].split(" : ")[0]
          filterData=filtervalarray[i].split(" : ")[1]


          inputData.filter(tableFilter);
          inputData=filteredOutput;
          filteredOutput=[];
        }

      buildTable(inputData,detailedData);
  }

  function buildTable(fData,dData){

      detailedData=dData;
      d3.selectAll("#myTable").remove();

      var table = d3.select('#myDynamicTable').append('table').attr("id", "myTable").attr("class","table table-striped");

      var thead = table.append('thead')
      var hrow = thead.append('tr')

      for (i=0;i<headerarray.length;i++){
        var hcell = hrow.append("th");
        hcell.text(headerarray[i]);

      }


      var	tbody = table.append('tbody');


      var rowcount=0;
      fData.forEach((ufoReport) => {
        rowcount ++
        let accountId;
        var row = tbody.append("tr");
        Object.entries(ufoReport).forEach(([key, value]) => {
          //console.log(ufoReport)
          let cell = row.append("td");
          if (key=="name"){
            detailedData.forEach((d)=>{

              if (d.name==value){
                  accountId=d.accountId;
                  //console.log(accountId)
              }
               
          })
            chtml= "<a href='javascript:getDetails(`"+ accountId +"`)'>"+value+"</a>"
          // chtml= "<a href='javascript:getDetails(accountId,detailedData)'>"+value+"</a>"
         
            cell.html(chtml)
          }
          else{
          cell.text(value);
          }

        });
      });

      d3.select(".rowcountdiv").html("Total Rows: " + rowcount )
      //d3.select(".rowcountdiv").text("Total Rows: " + rowcount)
  }

function getDetails(accountId){

 // console.log(detailedData)
  let odd=true;
  let getKeys=['created', 'clientName','score','weight','claimCount','errorCount','otherCount','status','claimType','subTaskType']
  let rowdiv;
  let prHTML="";
  let pc=0;
  d3.selectAll("#popup-row-master").remove();
  pdiv=d3.selectAll("#popDiv").append("div").attr("id","popup-row-master").attr("class","popupChild")
  

  detailedData.forEach((d) => {
  
    if(d.accountId==accountId){
   
    prdiv=pdiv.append("div").attr("class","popup-record")

    Object.entries(d).forEach(([key,value])=>{

      if  ((key=='issueType') || (key=='issueId') || key=='issueUrl'){
        if (key=='issueUrl'){
          prHTML="<div class='issueHead'><img width='14' height='14' src='"+ value + "'> " + prHTML
          pc=pc+1
        }
        if (key=='issueType'){
          prHTML= prHTML + " - " + value + "</div>"
          pc=pc+1
        }
        if (key=='issueId'){
          prHTML=" " + value + " " + prHTML
          pc=pc+1
        }
      }
      if (key=='resolution'){
        prHTML = prHTML + "<div class='issueHead'></div>" + value.description + "</div>"
        pc=pc+1
      }
      if(key=='parent'){
        prHTML = prHTML + "<div class='issueHeadBold'></div>" + value.key + "</div>"
        pc=pc+1
      }

      if (pc==5){
        prdiv.append("div").attr("class", "popup-row-head").attr("id","popup-row-head").html(prHTML)
        prHTML=""
        pc=0 //reset pc
      }
    
    })

    // for(i=0;i<d.length;i++){

    // }
    Object.entries(d).forEach(([key,value])=>
    {
    
      if (getKeys.includes(key)){
        if (odd==true) {

            odd=false;

            rowdiv=prdiv.append("div").attr("class", "popup-row").attr("id","popup-row")
            ckdiv=rowdiv.append("div").attr("class","popup-cols popup-cols-label")
            ckdiv.html(key)
            cvdiv=rowdiv.append("div").attr("class","popup-cols")
            cvdiv.html(value) 
            
        }
        else{    
            odd=true

            ckdiv=rowdiv.append("div").attr("class","popup-cols popup-cols-label")
            ckdiv.html(key)
            cvdiv=rowdiv.append("div").attr("class","popup-cols")
            cvdiv.html(value) 
            
        }
      }
    })
    // cellHTML = cellHTML + "<br>" + d.created + " " + d.clientName + " " + d.issueType + d.score
  }
  })

  //pdiv.html(cellHTML);
  }


function tableFilter(tdata) {

        //let output=null
        let fvalue=filterData
        fkey=filterKey

        Object.entries(tdata).forEach(([key, value]) => {

          if (key==fkey) {
            if (value == fvalue){
                filteredOutput.push(tdata)
          }}
          });
  }

  function toDisplayCase(s) {
    
    capNext = true;
    charArray=s.split('');
    let displayText;

    for (c in charArray) {

        if (c==" "){
          capNext =true
        }
        else{
        c = (capNext)
                ? c.toUpperCase()
                : c.toLowerCase();
        capNext=false
        }
        displayText=displayText + c
      
    }
    return displayText;
}