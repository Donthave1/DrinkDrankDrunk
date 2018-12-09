//add Javascript in this file
console.log('JS file Connected')


function optionChanged(selected_food){
  console.log("Food choice", selected_food);
  if (selected_food) {
    var url = `/yummy/${selected_food}`;
    console.log("Food endpoint", url);
    d3.json(url).then(function(response, error){
      console.log(response)
      buildPieChart(response)    
    })
  }
}

function buildPieChart(response){

  // var pieURL = "/food/" + selected_food;
      var list = [];
  //d3.json(pieURL).then(function(response) {

    response.forEach(function(data) {
      list.push({
        wine_count: data.wine_count,
        grape_type: data.grape_type,
      })
    })

    console.log(list)


    let pieValues = [];
    let pieLabels = [];

    list.forEach(function(data){
      pieValues.push(data.wine_count)
      pieLabels.push(data.grape_type)
    });
    console.log(pieValues)
    console.log(pieLabels)
    
    var pieData = 
      {
        values: pieValues,
        labels: pieLabels,
        type: "pie"

      };

    let pieTrace = [pieData]
    
    console.log(pieTrace)

    var pieLayout = {
      title: 'Wine count by Grape Type',
      height: 600,
      width: 700,
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)'

    
      
    };

    Plotly.newPlot("pie", pieTrace, pieLayout);


  }
