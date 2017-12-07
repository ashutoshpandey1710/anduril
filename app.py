from flask import Flask, jsonify

import tasks
from api import get_all_player_data

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return "LoL Statistics App (BattleFy)!!"


@app.route('/lolapp/<summonerName>', methods=['GET'])
def get_data(summonerName):
    return jsonify(get_all_player_data(summonerName))


if __name__ == '__main__':
    app.run(debug=True)
