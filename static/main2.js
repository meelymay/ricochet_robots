var sqrSize = 30;
var backgroundColor = '#DDD';
var currentRobot;

function selectRobot() {
    console.log('old robot: ' + currentRobot);
    if (currentRobot) {
	currentRobot
	    .style('stroke-width', '1')
	    .style('stroke', 'black');
    }
    currentRobot = d3.select(this)
	.style('stroke-width', '3')
	.style('stroke', 'white');
}

function moveRobot() {
    console.log('current robot: ' + currentRobot);
    var params = {
	robot: currentRobot,
	x: d3.select(this).data().x,
	y: d3.select(this).data().y
    };
    $.get('/move', params, function(data) {
	    console.log('update robot position');
	    console.log(data);
	    console.log(currentrobot);
	    var newPosition = data.data;
	    currentRobot
		.attr("cx", (newPosition.x+.5)*sqrSize)
		.attr("cy", (newPosition.y+.5)*sqrSize);
	});
}

function paintRobots(robots) {
    var svg = d3.select('svg');
    
    var robots = svg.selectAll(".robot")
      .data(robots)
      .enter().append("svg:circle")
      .attr("class", "robot")
      .attr("cx", function(d) {
	      return (d.x+.5)*sqrSize;
	  })
      .attr("cy", function(d) {
	      return (d.y+.5)*sqrSize;
	  })
      .attr("r", function(d) {
	      if (d.robot) {
		  return sqrSize/2-5;
	      } else {
		  return 0;
	      }
	  })
      .style('fill', function(d) {
	      return d.robot;
	  })
      .style("stroke", 'black')
      .on('click', selectRobot);
}

function main() {
    $.get('/board', {}, function(data) {
  var board = data.data;
  var h = board.length*50 + 25;
  var w = h;

  var grid = d3.select("body")
      .append("svg")
      .attr("width", w)
      .attr("height", h);

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
      .style('fill', backgroundColor);

  squares
      .on('mouseover', function() {
	      d3.select(this)
	      .style('fill', '#0F0');
	  })
      .on('mouseout', function() {
	      d3.select(this)
	      .style('fill', backgroundColor);
	  })
      .on('click', moveRobot)
      .style("stroke", '#555');

  var horWalls = grid.selectAll(".horwall")
      .data(board)
      .enter().append("svg:rect")
      .attr("class", "horwall")
      .attr("y", function(d) {
	      if (d.hor > 0) {
		  return d.y*sqrSize;
	      } else if (d.hor < 0) {
		  return (d.y-1)*sqrSize;
	      } else {
		  return 0;
	      }
	  })
      .attr("x", function(d) {
	      return sqrSize*d.x;
	  })
      .attr("width", 2)
      .attr("height", function(d) {
	      if (d.hor != 0) {
		  return sqrSize;
	      } else {
		  return 0;
	      }
	  })
      .style('fill', '#555')
      .style("stroke", '#555');

  var verWalls = grid.selectAll(".verwall")
      .data(board)
      .enter().append("svg:rect")
      .attr("class", "verwall")
      .attr("x", function(d) {
	      if (d.vert > 0) {
		  return d.x*sqrSize;
	      } else if (d.vert < 0) {
		  return (d.x-1)*sqrSize;
	      } else {
		  return 0;
	      }
	  })
      .attr("y", function(d) {
	      return sqrSize*d.y;
	  })
      .attr("width", function(d) {
	      if (d.vert != 0) {
		  return sqrSize;
	      } else {
		  return 0;
	      }
	  })
      .attr("height", 2)
      .style('fill', '#555')
      .style("stroke", '#555');

  paintRobots(board);
	});
}