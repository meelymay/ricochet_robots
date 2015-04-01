from flask import Flask, jsonify, render_template, request, session
from board import *
import random
app = Flask(__name__)

BOARD_SIZE = 16
GAME = Board(BOARD_SIZE)

@app.route('/board')
def draw():
    return jsonify(data=GAME.board_view())

@app.route('/move')
def move():
    board = GAME

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
    return jsonify(data={'x': x, 'y': y})


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'computer cat'

    app.run(debug=True)
