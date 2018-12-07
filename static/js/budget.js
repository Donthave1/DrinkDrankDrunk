// @TODO: YOUR CODE 
//let url = "/budget/" + wine_price
price_range = [100, 150, 200, 250, 300, 500]

let priceDropdown = d3.select("#priceRanges").selectAll()
price_range.forEach((price) => {
  let selection = d3.select("#priceRanges");
  let option = selection.append("option");
  option.text(price)
});


// function init() {
//   // Use the list of sample names to populate the select options
//   priceDropdown.on("optionChanged", function(selected_budget){
//     d3.json("price/"+selected_budget).then(buildScatter(data))
//   })
// }

function optionChanged(selected_budget){
  var url = `/price/${selected_budget}`;

  d3.json(url, function(error, response){
    buildScatter(response)
  })
}




function buildScatter(rofl){
  xData = []
  yData = []

  rofl.forEach(function(data) {
    data.price = +data.price
    data.review = +data.review
    xData.push(data.price)
    yData.push(data.review)
    });

  console.log(xData)
  console.log(yData)

  const trace1 = {
    x:xData,
    y:yData,
    mode:"markers",
    type: "scatter",
    name: "Review vs Price",
  }

  const data = [trace1]
  const layout ={
    title: "Review vs Price",
    xaxis: {title: "Price"},
    yaxis: {title: "Review"}
  }
  Plotly.newPlot("scatter", data, layout)
}
