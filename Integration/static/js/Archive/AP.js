let data;
function sendAPRequest(apiUrl='/rest/api/3/search?jql=parent=null and Status="Done"')
{
    // alert("Calling send AP Request")
    // alert(apiUrl);
    AP.request({
            url: apiUrl,
            type: 'GET', dataType: 'json', contentType: 'application/json',
                success: (msg) => {
                //alert("msg " + msg)
                data =JSON.parse(msg)
                return data
                //statusValues.push((JSON.parse(msg)).total)
                },
                error: (msg) => {
                    //statusValues.push("error");console.log("error:\n" + JSON.stringify(msg));
                    return "error:\n" + JSON.stringify(msg)
                }
            });

}
// AP.user.getCurrentUser(function(user) {
//
//     let userAPIPath='/rest/api/3/user?accountId='
//     url = userAPIPath + user.atlassianAccountId
//     alert(url)
//     //alert(sendAPRequest(url))
//     welcome(user.atlassianAccountId);
//     console.log(welcome ,  user.atlassianAccountId);
// });

// function welcome(user){
//         d3.selectAll("#nav-welcome").html("Welcome " +  user + ",")
//     }