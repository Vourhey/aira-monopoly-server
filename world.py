import os
from game import Game

class WorldOfMonopoly:
    games = {}
    def createNewGame(self):
        g = Game()
        self.games[g.gameId] = g
        print(self.games)
        return g.gameId

    def debugAmountOfGames(self):
        return len(self.games)

    def debugListOfGames(self):
        rlist = []
        for key, value in self.games.items():
            rlist.append(key)

        return rlist

    def debugGetPlayersOfTheGame(self, gameId):
        g = self.games[gameId]
        ret = []
        for i in g.players:
            ret.append(i)
        return ret

    def __str__(self):
        return '\n'.join("{!s}: {!r}".format(key,val) for (key,val) in self.games.items())

    def __repr__(self):
        return '\n'.join("{!s}: {!r}".format(key,val) for (key,val) in self.games.items())
