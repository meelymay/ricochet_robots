var sqrSize = 30;
var backgroundColor = '#DDD';
var currentRobot;
var currentTarget;

function selectRobot() {
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
    var square = d3.select(this).data()[0];
    var params = {
	robot: currentRobot.data()[0].robot,
	x: square.x,
	y: square.y,
	oldX: currentRobot.data()[0].x,
	oldY: currentRobot.data()[0].y
    };
    $.get('/move', params, function(data) {
	    var newPosition = data.data;
	    if (newPosition.length == 0) {
		return;
	    }
	    currentRobot.data()[0].x = newPosition.x;
	    currentRobot.data()[0].y = newPosition.y;

	    currentRobot
		.attr("cx", (newPosition.x+.5)*sqrSize)
		.attr("cy", (newPosition.y+.5)*sqrSize);

	    $.get('/target', {}, function(data) {
		    var targets = data.data;
		    paintTarget(targets);
		});
	});
}

function paintTarget(targets) {
    var svg = d3.select('svg');

    if (currentTarget) {
	currentTarget.attr('points', '0,0');
    }

    var d = targets[0];
    a = '' + (d.x*sqrSize + 3) + ',' + (d.y*sqrSize + 3);
    b = '' + ((d.x + 1)*sqrSize - 3) + ',' + (d.y*sqrSize + 3);
    c = '' + ((d.x+.5)*sqrSize) + ',' + ((d.y+1)*sqrSize - 3);
    var points = a + ' ' + b + ' ' + c;

    currentTarget = svg.append('svg:polygon')
	.attr('class', 'target')
	.attr('points', points)
	.attr('fill', d.target);
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
		  return (d.y + 1)*sqrSize;
	      } else if (d.hor < 0) {
		  return d.y*sqrSize;
	      } else {
		  return 0;
	      }
	  })
      .attr("x", function(d) {
	      return sqrSize*d.x
	  })
      .attr("height", 2)
      .attr("width", function(d) {
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
		  return (d.x + 1)*sqrSize;
	      } else if (d.vert < 0) {
		  return d.x*sqrSize;
	      } else {
		  return 0;
	      }
	  })
      .attr("y", function(d) {
	      return sqrSize*d.y;
	  })
      .attr("height", function(d) {
	      if (d.vert != 0) {
		  return sqrSize;
	      } else {
		  return 0;
	      }
	  })
      .attr("width", 2)
      .style('fill', '#555')
      .style("stroke", '#555');

  paintRobots(board.filter(function(sq) {
	      return Boolean(sq.robot);
	  }));

  paintTarget(board.filter(function(sq) {
	      return Boolean(sq.target);
	  }));
	});
}