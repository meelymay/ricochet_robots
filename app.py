from flask import Flask, jsonify, render_template, request, session
from board import *
import random
app = Flask(__name__)

BOARD_SIZE = 16
@app.route('/board')
def draw():
    board = GAMES[session['uid']]
    return jsonify(data=board.board_view())

@app.route('/robots')
def get_robots():
    board = GAMES[session['uid']]
    return jsonify(data=board.board_view(filter='robots'))

@app.route('/target')
def get_target():
    board = GAMES[session['uid']]
    return jsonify(data=board.board_view(filter='target'))

@app.route('/move')
def move():
    board = GAMES[session['uid']]

    color = request.args.get('robot')
    click_x = int(request.args.get('x'))
    click_y = int(request.args.get('y'))
    old_x = int(request.args.get('oldX'))
    old_y = int(request.args.get('oldY'))

    y_diff = old_x - click_x
    x_diff = old_y - click_y
    hor = -x_diff/abs(x_diff) if x_diff != 0 else 0
    ver = -y_diff/abs(y_diff) if y_diff != 0 else 0

    new_square = board.move_robot(LETTERS[color].upper(), hor, ver)
    if not new_square:
        return jsonify(data=[])
    x = new_square.x
    y = new_square.y

    print 'Moving %s, currently at (%s, %s), in the direction of (%s, %s)' % (color,old_x, old_y, click_x, click_y)
    print 'New location (%s, %s)' % (x,y)

    target = board.get_target()

    print 'A target...',target

    return jsonify(data={'x': x, 'y': y, 'target': target.target})


@app.route('/')
def index():
    session['uid'] = int(random.random()*100000)
    GAMES[session['uid']] = Board(BOARD_SIZE)
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'computer cat'

    app.run(debug=True)
