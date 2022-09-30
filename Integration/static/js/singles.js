//alert("Loading Singles")
// ---------------------------------------------------------------------------
// ---------------------------------------------------------------------------
// ---------------------------------------------------------------------------
singles()
// ---------------------------------------------------------------------------
// ---------------------------------------------------------------------------
function singles(jql='parent=null and Status=',statusValues = [])
    {

    let sdiv=d3.selectAll("#singles")
    let hdiv=d3.selectAll("#singles-header")

    d3.selectAll(".singles-header").remove()
    d3.selectAll(".singles").remove()


    for (let i = 0; i < status.length; i++) {
        hdiv.append('div').attr("class","singles-header").html(status[i]);
        url= baseUrl + '"' + status[i] + '"'

       let APResponse=sendAPRequest(url)

       // alert("APResponse " + APResponse)
        statusValue=(APResponse).total

        statusValues.push(statusValue)
        sdiv.append('div').attr("class","singles").html(statusValue);

        // AP.request(
        //     {
        //     url: url + '"' + status[i] + '"',
        //     url: url,
        //     type: 'GET', dataType: 'json', contentType: 'application/json',
        //         success: (msg) => {
        //             sdiv.append('div').attr("class","singles").html((JSON.parse(msg)).total);
        //             statusValues.push((JSON.parse(msg)).total)
        //         },
        //         error: (msg) => {
        //
        //             statusValues.push("error");console.log("error:\n" + JSON.stringify(msg));
        //         }
        //     });

        }
}
// ---------------------------------------------------------------------------