
let jql ='parent=null and Status='

d3.select('#task-counter')
  .on('change', function() {
      let task_counter = d3.select(this).property('value')
      if (task_counter==='today') {
          date_query='"Completed Date">=startOfDay()'
      }
      jql='parent=null' + ' and ' + date_query  +' and Status='
      // alert(d3.select(this).property('value'))
      singles(jql)
  });