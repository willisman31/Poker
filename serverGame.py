import sys, pygame, mygui, serverThread, serverGame, time, json
from pygame.locals import *
from constants import *
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
numberOfPlayers = 0

def init(clientSockets):
    numberOfPlayers = len(clientSockets) + 1
    #Initializing cards and players
    i = 0
    for cSock in clientSockets:
        cards[cSock] = (deck.pop(),deck.pop())
        cards[i]=cards[cSock]
        #players[cSock] = Player(i)
        players[i]=Player(i)
        i += 1

    serverTurn = numberOfPlayers - 1
    players[start]. bet(smallBlind)
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
        broadcast()
        if turn == serverTurn:
            server_move()
        else:
            wait_for_client_move()

        update_game()
        turn = (turn+1)%numberOfPlayers
        if turn == lastRaisedPlayer:
            break
    broadcast()


def init_broadcast(clientSockets):
    for cSock in clientSockets:
        msgPlayerCards = json.dumps(cards[cSock])
        cSock.send(msgPlayerCards)
    broadcast(clientSockets)

def broadcast(clientSockets):

    for cSock in clientSockets:
        msgPlayers = json.dumps(players, default=lambda o: o.__dict__)
        msgTableCards = json.dumps(tableCards)
        msgTurn = str(turn)
        msgNumPlayers = str(numberOfPlayers)
        msgPot = str(pot)
        cSock.send(msgPlayers)
        cSock.send(msgTableCards)
        cSock.send(msgTurn+" "+msgNumPlayers+" "+msgPot)

def start_game():
    init_broadcast() #players, client's cards, tablecards, turn

    one_round()
    tableCards.append(deck.pop())
    tableCards.append(deck.pop())
    tableCards.append(deck.pop())
    one_round()
    tableCards.append(deck.pop())
    one_round()
    tableCards.append(deck.pop())

    result()
    broadcast_result()

def unpause_clients(clientSockets):
    for obj in clientSockets:
        obj.send("begin")


def main(screen, clientSockets):
    #clients = [1,2,3]

    unpause_clients(clientSockets)
    print "Inside serverGame file : Method main()"
    screen.fill(BACK_SCREEN)
    pygame.display.update()
    init(clientSockets)
    time.sleep(5)
    pygame.quit()
    sys.exit()

    #init(clientSockets)
    start_game()


if __name__ == '__main__':
    main()
