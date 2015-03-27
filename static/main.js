function createPlayFunc(cellTag, i, j) {
    return function(e) {
	$.get('/play', {'i': i, 'j': j}, function(data) {
		// do nothing if game over or space occupied
		if ($('#winner').html() !== "" ||
		    cellTag.html() === 'O' || cellTag.html() === 'X') {
		    return;
		}

		// play X
		cellTag.html('X');
		// play O
		if ('x' in data) {
		    var aiPlayTag = $('#cell' + data['x'] + data['y']);
		    aiPlayTag.html('O');
		}

		// update game status
		var status = data['status'];
		if (status !== null) {
		    var message = "Well, the game is over..." + status;
		    if (status !== 'tie') {
			message = message + " wins!";
		    }
		    $('#winner').html(message);
		}
	    });
    };
}

$(function() {
	for (var i in [0,1,2]) {
	    for (var j in [0,1,2]) {
		var cellName = '#cell' + i + j;
		var cellTag = $(cellName);
		var x = i;
		var y = j;

		// attach the play function to each cell
		$(document).on('click', cellName, createPlayFunc(cellTag, i, j));
	    }
	}
    });