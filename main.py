from flask import Flask
from flask import jsonify
from flask_cors import CORS
from world import WorldOfMonopoly

app = Flask(__name__)
#api = Api(app)
CORS(app)

globalWorld = WorldOfMonopoly()

@app.route('/debug/printstate')
@app.route('/debug/printstate/<int:gameId>')
def debug_printstate(gameId=None):
    if gameId is not None:
        return jsonify(globalWorld.debugGetPlayersOfTheGame(gameId))

    r = {
      "amount_of_games": globalWorld.debugAmountOfGames(),
      "list_of_games": globalWorld.debugListOfGames()
    }

    return jsonify(r)

@app.route('/creategame')
def create_game():
    gameId = globalWorld.createNewGame()
    playerId = globalWorld.games[gameId].addPlayer()
    return jsonify({'gameId' : gameId, 'playerId': playerId})

@app.route('/game/join/<int:gameId>')
def game_join(gameId):
    p = globalWorld.games[gameId].addPlayer()
    print(globalWorld)
    return jsonify({'playerId': p})

@app.route('/game/leave/<int:gameId>/<string:who>')
def game_leave(gameId, who):
    globalWorld.games[gameId].leaveTheGame(who)
    return jsonify({'status': 'ok'})

@app.route('/game/balance/<int:gameId>/<string:who>')
def get_balance(gameId, who):
    b = globalWorld.games[gameId].players[who].balance
    return jsonify({'balance': b})

@app.route('/game/send/<int:gameId>/<string:from_player>/<string:to_player>/<int:amount>')
def game_send(gameId, from_player, to_player, amount):
    globalWorld.games[gameId].send(from_player, to_player, amount)
    return jsonify({'status': 'ok'})
