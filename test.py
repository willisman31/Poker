import json, player, deck
from constants import *

players = {0:[]}
players[0] = player.Player("100","safal","True")
players[0].money = 1250
players[1] = player.Player(101)

tableCards = []
deck1 = deck.Deck()
tableCards.append(deck1.pop())
tableCards.append(deck1.pop())
tableCards.append(deck1.pop())

turn = -1

#message = '{"action": "safal", "obj": {"roll_number": "1", "name": "Mat"}, "data": "wow", "method": "pandita"}'
msgPlayers = json.dumps(players, default=lambda o: o.__dict__)
msgTableCards = json.dumps(tableCards)
msgTurn = str(turn)
print msgPlayers + '\n' + msgTableCards + '\n' + msgTurn

# payload = Payload(message)
# print payload.obj['name']

recvPlayers = json.loads(msgPlayers)
recvPlayersObj = {0:[]}

for key in recvPlayers:
    obj = player.Player(recvPlayers[key]['id'], recvPlayers[key]['name'])
    obj.fold = recvPlayers[key]['fold']
    obj.pot = recvPlayers[key]['pot']
    obj.money = recvPlayers[key]['money']
    print type(obj.fold)
    print type(obj.pot)
    print type(obj.money)
    print type(obj.id)

    recvPlayersObj[key] = obj

# print type(recvPlayersObj['0'].money)
# recvPlayersObj['0'].bet(500)
# print type(recvPlayersObj['0'].money)
