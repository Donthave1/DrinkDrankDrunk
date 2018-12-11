//add Javascript in this file
console.log('taste.js file connected')


function optionChanged(selected_taste){

    console.log("Taste choice", selected_taste);

    if (selected_taste) {

        var url = `/taste/${selected_taste}`;
        console.log("Taste endpoint", url);

        d3.json(url, function(error, response){
            buildTable(response)    
      })
    }
  };

function buildTable(response){
    //get rid of the old table
    var table = d3.select("#taste-table");
          
    // Use `.html("") to clear any existing metadata
    table.html("");
          
    var sortAscending = false;
    var table = d3.select('#taste-table').append('table');
    var titles = d3.keys(response[0]);
    var headers = table.append('thead').append('tr')
                        .selectAll('th')
                        .data(titles).enter()
                        .append('th')
                        .text(function (d) {
                              return d;
                        })
                        .on('click', function (d) {
                            headers.attr('class', 'header');

                            if (sortAscending) {
                                rows.sort(function(a, b) {return d3.ascending(b[d], a[d]); });
                                sortAscending = true;
                                this.className = 'des';
                            } else {
                                rows.sort(function(a, b) {return d3.descending(b[d], a[d]); });
                                sortAscending = false;
                                this.className = 'aes';
                              }
                        });   

    var rows = table.append('tbody').selectAll('tr')
                    .data(response).enter()
                    .append('tr');
    rows.selectAll('td')
        .data(function (d) {
                 return titles.map(function (k) {
                     return { 'value': d[k], 'name': k};
                 });
              }).enter()
                .append('td')
                .attr('data-th', function (d) {
                 return d.name;
                })
                .text(function (d) {
                    return d.value;
                })
                .exit()
                .remove();                        
};  

