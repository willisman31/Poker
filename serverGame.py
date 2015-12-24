from deck import *
from player import *

deck = Deck()
cards = {0:[]}
players = {0:[]}
pot = 0
tableCards = []
turn = -1
smallBlind = 10
bigBlind = smallBlind * 2
start = 0
lastRaisedPlayer = -1
serverTurn = 0

def init(clients):
    numberOfPlayers = len(clients)
    #Initializing cards and players
    for i in range(0, numberOfPlayers):
        cards[i] = (deck.pop(),deck.pop())
        players[i] = Player(i)

    serverTurn = 0
    players.get(start).bet(smallBlind)
    players.get((start+1)%numberOfPlayers).bet(bigBlind)
    turn = (start + 2)%numberOfPlayers
    pot = smallBlind + bigBlind
    lastRaisedPlayer = turn
    #wake_clients(clients)

#what happens if player folds?
#suggestions:maintain new numberOfPlayers, players, turns etc for each round
#one match = several games, one game = 4 rounds
def one_round():
    while True:
        wait_for_client()
        update_game()

        turn = (turn+1)%numberOfPlayers
        if turn == lastRaisedPlayer:
            break

def start_game():
    init_broadcast()

    one_round()
    tableCards.append(deck.pop())
    tableCards.append(deck.pop())
    tableCards.append(deck.pop())
    one_round()
    tableCards.append(deck.pop())
    one_round()
    tableCards.append(deck.pop())

    result()

def main():#clients):
    clients = [1,2,3]
    init(clients)
    start_game()


if __name__ == '__main__':
    main()
