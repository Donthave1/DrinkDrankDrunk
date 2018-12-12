// @TODO: YOUR CODE 
price_range = [ {"text":"Dirt Cheap",
                "value":50}, 
                {"text":"Meh College Kid",
                "value":100}, 
                {"text":"Normal Human Being",
                "value":150}, 
                {"text":"Going Ham",
                "value":200}, 
                {"text":"Like a Boss",
                "value":99999}]

let priceDropdown = d3.select("#priceRanges").selectAll()
price_range.forEach((price) => {
  let selection = d3.select("#priceRanges");
  let option = selection.append("option");
  option.text(price["text"]).attr("value",(price["value"]));
});

function optionChanged(selected_budget){
  var url = `/price/${selected_budget}`;

  d3.json(url, function(error, response){
    buildScatter(response)
  })
}
function defineColor(data){
  if (data.wine_type == "Red"){
    wineData.push("rgb(153,0,76");
  }
  else if (data.wine_type == "White"){
    wineData.push("rgb(255,255,224)");
  }
  else if (data.wine_type == "Rose"){
    wineData.push("rgb(255,192,203)");
  }
  else if (data.wine_type == "Sparkling"){
    wineData.push("rgb(255,215,0)");
  }
  else {
    wineData.push("rgb(128,0,0)");
  }
}

function buildScatter(rofl){
  xData = []
  yData = []
  textData = []
  sizeData = []
  wineData = []
  typeData=[]
  normData=[]

  rofl.forEach(function(data) {
    data.price = +data.price
    data.review = +data.review
    xData.push(data.review)
    yData.push(data.price)
    normData.push(data.price)
    textData.push(`Brand: ${data.wine_name} <br> Wine Type: ${data.wine_type} <br> Price: $${data.price} <br> Score: ${data.review}`)
    //sizeData.push(data.price/data.review)
    defineColor(data)
    typeData.push(data.wine_type)
    });

  ratio = Math.max.apply(Math, normData) / 100,
  l = normData.length
  for (i = 0; i < l; i++) {
    normData[i] =Math.round(normData[i]/ratio);
  }
  
  for (i=0; i<l; i++) {
    ratioData = Math.round(xData[i]/normData[i])
    sizeData.push(ratioData*1.5+10)
  }
  console.log(sizeData)
  console.log(normData)
  console.log(yData)

  const trace1 = {
    x:xData,
    y:yData,
    mode:"markers",
    type: "scatter",
    name: "Review vs Price",
    text:textData,
    marker:{
      color:wineData,
      size:sizeData,
      opacity: 0.75
    }
  };

  let priceData = [trace1];

  let priceLayout = {
    title: "Cost Performance (Review/Price)",
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    "xaxis": {"title": "Professional Review Rating Scores"},
    "yaxis": {"title": "Price"},
    hovermode:"closest"
  };


  Plotly.newPlot("scatter", priceData, priceLayout, {responsive: true})

};

