// from app.js
function smartScript(functionText){
  
var script = d3.select('body').append('script').attr("type","text/javascript");
var functionsappend=""

var i;
//BUILDS AND APPENDS DYANAMIC JAVA SCRIPT EVENTS

for (i = 0; i < functionText.length; i++) {
  functionsappend = functionsappend + "\n" + functionText[i];
}
script.html(functionsappend);
}
