// @TODO: YOUR CODE 
//let url = "/budget/" + wine_price
price_range = [100, 150, 200, 250, 300, 500]

let priceDropdown = d3.select("#priceRanges").selectAll()
price_range.forEach((price) => {
  let selection = d3.select("#priceRanges");
  let option = selection.append("option");
  option.text(price)
});

function optionChanged(selected_budget){
  var url = `/price/${selected_budget}`;

  d3.json(url, function(error, response){
    buildScatter(response)
  })
}

function makeResponsive() {
  const svgArea = d3.select("body").select("svg");
  if (!svgArea.empty()) {
    svgArea.remove();
  }
}




function buildScatter(hairData){

  const svgWidth = 750;
  const svgHeight = 500;

  const margin = {
    top: 20,
    right: 40,
    bottom: 60,
    left: 100
    };

  const height = svgHeight - margin.top - margin.bottom;
  const width = svgWidth - margin.left - margin.right;


  // Create an SVG wrapper, append an SVG group that will hold our chart, and shift the latter by left and top margins.
  const svg = d3.select("#scatter")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);
  const chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);
  

  // Import Data
    // Step 2: Create scale functions
  // ==============================
  let xScale = d3.scaleLinear()
  .domain([d3.min(hairData, d=> d.review) -5, d3.max(hairData, d => d.review)])
  .range([0, width]);
  const yScale = d3.scaleLinear()
  .domain([d3.min(hairData, d => d.price), d3.max(hairData, d => d.price)])
  .range([height, 0]);
  // Step 3: Create axis functions
  // ==============================
  const bottomAxis = d3.axisBottom(xScale);
  const leftAxis = d3.axisLeft(yScale);


  // Step 4: Append Axes to the chart
  // ==============================
  chartGroup.append("g")
  .attr("transform", `translate(0, ${height})`)
  .call(bottomAxis);
  chartGroup.append("g")
  .call(leftAxis);

  // Apped Axis Label
  chartGroup.append("text")
  .attr("transform", "rotate(-90)")
  .attr("y", 0 - margin.left + 40)
  .attr("x", 0 - (height / 2))
  .attr("dy", "1em")
  .text("Price of the Wine");
  chartGroup.append("text")
  .attr("transform", `translate(${width / 2}, ${height + margin.top + 30})`)
  .attr("class", "axisText")
  .text("Professional Review Score");
  // Step 5: Create Circles
  // ==============================
  hairData.forEach(function(data){
    data.price = +data.price;
    data.review = +data.review;
  })
    
  let circlesGroup = chartGroup.selectAll("circle")
    .data(hairData)
    .enter()
    .append("circle")
    .attr("cx", d => xScale(d.review))
    .attr("cy", d => yScale(d.price))
    .attr("r", "5")
    .attr("fill", "purple")
    .attr("opacity", "0.5");
    // Step 6: Initialize tool tip
    // ==============================
    let toolTip = d3.tip()
    .offset([80, -60])
    .html(function(data) {
    return `${data.wine_name}<br />
    Wine Price: ${data.price}<br /> 
    Wine Review: ${data.review}`;
    });
    // Step 7: Create tooltip in the chart
    // ==============================
    chartGroup.call(toolTip);
    // Step 8: Create event listeners to display and hide the tooltip
    // ==============================
    circlesGroup.on("click", function(data) {
    toolTip.show(data, this);
    })
    .on("mouseout", function(data) {
    toolTip.hide(data);
    });
    // Create axes labels

}
