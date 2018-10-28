from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from world import WorldOfMonopoly

app = Flask(__name__)
api = Api(app)
CORS(app)

globalWorld = WorldOfMonopoly()

class DebugMode(Resource):
    def get(self, gameId=None):
        if gameId is not None:
            return globalWorld.debugGetPlayersOfTheGame(gameId)

        r = {
          "amount_of_games": globalWorld.debugAmountOfGames(),
          "list_of_games": globalWorld.debugListOfGames()
        }

        return r

class AiraMonopoly(Resource):
    def get(self):
        return {'id' : globalWorld.createNewGame()}

class JoinMonopoly(Resource):
    def get(self, gameId):
        p = globalWorld.games[gameId].addPlayer()
        print(globalWorld)
        return p

class LeaveMonopoly(Resource):
    def get(self, gameId, who):
        globalWorld.games[gameId].leaveTheGame(who)
        return {'status': 'ok'}

class SendMoney(Resource):
    def get(self, gameId, from_player, to_player, amount):
        globalWorld.games[gameId].send(from_player, to_player, amount)
        return {'status': 'ok'}

api.add_resource(DebugMode, '/debug/printstate', '/debug/printstate/<int:gameId>', endpoint=None)
api.add_resource(AiraMonopoly, '/creategame')
api.add_resource(JoinMonopoly, '/game/join/<int:gameId>')
api.add_resource(LeaveMonopoly, '/game/leave/<int:gameId>/<int:who>')
api.add_resource(SendMoney, '/game/send/<int:gameId>/<int:from>/<int:to>/<int:amount>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
