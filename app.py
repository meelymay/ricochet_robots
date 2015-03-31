from flask import Flask, jsonify, render_template, request, session
from board import *
import random
app = Flask(__name__)


@app.route('/board')
def draw():
    n = 16
    return jsonify(data=Board(n).board_view())

@app.route('/move')
def move():
    return jsonify(data={'x':10, 'y':10})


@app.route('/')
def index():
    # initialize a new board
    # session['user'] = random.randint(1, 1000000)
    session['board'] = None
    session['status'] = None
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'computer cat'

    app.run(debug=True)
