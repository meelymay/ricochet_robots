function main() {
    $.get('/board', {}, function(data) {
	    var board = data.data;
  var h = board.length*50 + 25;
  var w = h;

  var grid = d3.select("body")
      .append("svg")
      .attr("width", w)
      .attr("height", h);

  var sqrSize = 30;
  var squares = grid.selectAll(".cell")
      .data(board)
      .enter().append("svg:rect")
      .attr("class", "cell")
      .attr("x", function(d) {
	      return sqrSize*d.x;
	  })
      .attr("y", function(d) {
	      return sqrSize*d.y;
	  })
      .attr("width", sqrSize)
      .attr("height", sqrSize)
      .style('fill', function(d) {
	      if (d.robot) {
		  return '#0F0';
	      } else {
		  return '#FFF';
	      }
	  });

  squares
      .on('mouseover', function() {
	      d3.select(this)
	      .style('fill', '#0F0');
	  })
      .on('mouseout', function() {
	      d3.select(this)
	      .style('fill', '#FFF');
	  })
      .on('click', function() {
	      console.log(d3.select(this));
	  })
      .style("stroke", '#555');

  var horWalls = grid.selectAll(".horwall")
      .data(board)
      .enter().append("svg:rect")
      .attr("class", "horwall")
      .attr("x", function(d) {
	      if (d.hor > 0) {
		  return d.x*sqrSize;
	      } else if (d.hor < 0) {
		  return (d.x-1)*sqrSize;
	      } else {
		  return 0;
	      }
	  })
      .attr("y", function(d) {
	      return sqrSize*d.y;
	  })
      .attr("width", sqrSize)
      .attr("height", 2)
      .style('fill', '#555')
      .style("stroke", '#555');
      });


//   var col = row.selectAll(".cell")
//       .data(function (d) { return d; })
//       .enter().append("svg:rect")
//       .attr("class", "cell")
//       .attr("x", function(d, i) {
// 	      console.log(d);
// 	      return 10*i;
// 	  })
//       .attr("y", 5)
//       .attr("width", 10)
//       .attr("height", 10)
//       .on('mouseover', function() {
// 	      d3.select(this)
// 	      .style('fill', '#0F0');
// 	  })
//       .on('mouseout', function() {
// 	      d3.select(this)
// 	      .style('fill', '#FFF');
// 	  })
//       .on('click', function() {
// 	      console.log(d3.select(this));
// 	  })
//       .style("fill", '#FFF')
//       .style("stroke", '#555');
// 	});
}