import json, player, deck
from constants import *
from operator import sub

# players = {0:[]}
# players[0] = player.Player("100","safal")
# players[0].money = 1250
# players[1] = player.Player(101)

# tableCards = []
# deck1 = deck.Deck()
# tableCards.append(deck1.pop())
# tableCards.append(deck1.pop())
# tableCards.append(deck1.pop())
#
# print tableCards[0]
turn = -1

#msgPlayers = json.dumps(players, default=lambda o: o.__dict__)
#msgTableCards = json.dumps(tableCards)
#msgTurn = str(turn)
#print msgPlayers + '\n' + msgTableCards + '\n' + msgTurn
#print msgTableCards

#recvTblCards = json.loads(msgTableCards)
#print recvTblCards[2]

# recvPlayers = json.loads(msgPlayers)
# recvPlayersObj = {0:[]}
#
# for key in recvPlayers:
#     obj = player.Player(recvPlayers[key]['id'], recvPlayers[key]['name'])
#     obj.fold = recvPlayers[key]['fold']
#     obj.pot = recvPlayers[key]['pot']
#     obj.money = recvPlayers[key]['money']
#     print type(obj.fold)
#     print type(obj.pot)
#     print type(obj.money)
#     print type(obj.id)
#
#     recvPlayersObj[key] = obj

# cards = (('C',4),('H',5))
# jsC = json.dumps(cards)
# print jsC
#
# recvCards = json.loads(jsC)
# print recvCards

a=(1,2)
b=(3,4)
c=(5,6)

print map(sum, zip(a, b))
print map(sub, a, b)
