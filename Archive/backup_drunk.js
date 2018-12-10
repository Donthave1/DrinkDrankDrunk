// @TODO: YOUR CODE 
//let url = "/budget/" + wine_price
content_range = [0,5, 10, 14, 20]

let priceDropdown = d3.select("#contentRanges").selectAll()
content_range.forEach((percent) => {
  let selection = d3.select("#contentRanges");
  let option = selection.append("option");
  option.text(percent)
});

function optionChanged(selected_percent){
  var url = `/alcohol/${selected_percent}`;

  d3.json(url, function(error, response){
    buildScatter(response)
  })
}



function buildScatter(rofl){
  xData = []
  yData = []
  priceData=[]
  rofl.forEach(function(data) {
    data.alcohol = +data.alcohol
    data.price = +data.price
    xData.push(data.wine_name)
    yData.push(data.alcohol)
    priceData.push(data.price)
    });

  console.log(xData)
  console.log(yData)

  const trace1 = {
    x:xData,
    y:yData,
    type: "bar",
    name: "Alcohol vs Brand",
    text: priceData
  }

  const data = [trace1]
  const layout ={
    title: "Alcohol Content for top reviews",
    xaxis: {title: "Brands"},
    yaxis: {title: "Alcohol Content"},
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)'
    
  }
  Plotly.newPlot("bar", data, layout)
}