from flask import Flask, jsonify

import tasks

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return "Heloooo Worldus!!"


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks.tasks})


if __name__ == '__main__':
    app.run(debug=True)
