import sys, pygame, mygui, serverThread, serverGame, time, json, copy
from pygame.locals import *
from constants import *
from deck import *
from player import *

class ServerGame:
    def __init__(self,clientSockets):
        self.clientSockets = clientSockets

    #what happens if player folds?
    #suggestions:maintain new numberOfPlayers, players, turns etc for each round
    #one match = several games, one game = 4 rounds
    def update_game(self):
        if recievedFoldValue == True:
            self.numberOfUnfoldedPlayers -= 1
            self.players[self.turn].do_fold()
            self.players[self.turn].pot = 0
        else:
            self.players[self.turn].bet(recievedBetValue)
            self.pot += recievedBetValue
            if self.players[self.turn].currentRoundBet > self.currentRoundBet:
                 self.currentRoundBet = self.players[self.turn].currentRoundBet
                 self.lastRaisedPlayer = self.turn


    def init_one_round(self):
        for i in range(0, self.numberOfPlayers):
            self.players[i].currentRoundBet = 0

        if not self.tableCards:
            self.players[self.start].currentRoundBet = self.smallBlind
            self.players[(self.start + 1)%self.numberOfPlayers].currentRoundBet = self.bigBlind
            self.currentRoundBet = self.bigBlind
        else:
            self.currentRoundBet = 0


    def one_round(self):
        self.init_one_round()
        while True:
            if not self.players[self.turn].fold and self.players[self.turn].money != 0:
                self.broadcast()
                if self.turn == self.serverTurn:
                    server_move()
                else:
                    wait_for_client_move()
                self.update_game()
            self.turn = (self.turn+1)%self.numberOfPlayers
            if self.turn == self.lastRaisedPlayer or self.numberOfUnfoldedPlayers <= 1:
                break
        self.broadcast()

    def init_one_game(self):
        self.deck = Deck()
        self.cards = {0:[]}
        self.players = {0:[]}
        self.tableCards = []
        self.smallBlind = 10
        self.bigBlind = self.smallBlind * 2
        self.start = 0

        self.numberOfPlayers = len(self.clientSockets) + 1
        self.numberOfUnfoldedPlayers = self.numberOfPlayers
        #Initializing cards and players
        i = 0
        for cSock in self.clientSockets:
            self.cards[cSock] = (self.deck.pop(),self.deck.pop())
            self.cards[i] = self.cards[cSock]
            #players[cSock] = Player(i)
            self.players[i] = Player(i)
            i += 1

        self.serverTurn = self.numberOfPlayers - 1
        self.players[self.serverTurn] = Player(self.serverTurn,"Server")
        self.cards[self.serverTurn] = (self.deck.pop(),self.deck.pop()) #Server Cards
        #self.serverPlayer = Player(serverTurn)


        self.players[self.start].bet(self.smallBlind)

        self.players[((self.start)+1)%(self.numberOfPlayers)].bet(self.bigBlind)
        self.turn = (self.start + 2)%self.numberOfPlayers
        self.pot = self.smallBlind + self.bigBlind
        self.lastRaisedPlayer = self.turn


    def one_game(self):
        self.init_one_game()
        self.init_broadcast()

        time.sleep(5)
        #
        # self.one_round()
        # self.tableCards.append(deck.pop())
        # self.tableCards.append(deck.pop())
        # self.tableCards.append(deck.pop())
        # self.one_round()
        # self.tableCards.append(deck.pop())
        # self.one_round()
        # self.tableCards.append(deck.pop())

        # result()
        # broadcast_result()

    def start_game(self):
        self.one_game()

    def init_broadcast(self):   #players, client's cards, tablecards, turn, numberOfPlayers, pot, toCallAmount
        i=0
        for cSock in self.clientSockets:
            msgPlayerCards = json.dumps(self.cards[cSock])
            msgPlayers = json.dumps(self.players, default=lambda o: o.__dict__)
            msgTableCards = json.dumps(self.tableCards)
            things = (self.turn, self.numberOfPlayers, self.pot)
            msgThings = json.dumps(things)

            completeMessage = msgPlayerCards+"::"+str(i)+"::"+msgPlayers+"::"+msgTableCards+"::"+msgThings
            i+=1

            cSock.send(completeMessage)
            print "Size of message sent : "+ str(sys.getsizeof(completeMessage)) +" bytes!"

        #self.broadcast()

    #GUI should be updated at the time broadcast
    def broadcast(self):    #players, tablecards, turn, numberOfPlayers, pot, toCallAmount = currentRoundBet - currentRoundPlayerBet

        for cSock in self.clientSockets:
            msgPlayers = json.dumps(self.players, default=lambda o: o.__dict__)
            msgTableCards = json.dumps(self.tableCards)
            things = (self.turn, self.numberOfPlayers, self.pot)
            msgThings = json.dumps(things)

            completeMessage = msgPlayerCards+"::"+str(i)+"::"+msgPlayers+"::"+msgTableCards+"::"+msgThings
            cSock.send(completeMessage)
            print sys.getsizeof(completeMessage)
            # cSock.send(msgPlayers)
            # cSock.send(msgTableCards)
            # cSock.send(msgThings)

def unpause_clients(clientSockets):
    for obj in clientSockets:
        obj.send("begin")


def main(screen, clientSockets):
    #clients = [1,2,3]

    unpause_clients(clientSockets)
    print "Inside serverGame file : Method main()"
    screen.fill(BACK_SCREEN)
    pygame.display.update()

    game = ServerGame(clientSockets)
    game.start_game()

    time.sleep(5)
    pygame.quit()
    sys.exit()

    #init(clientSockets)
    start_game()


if __name__ == '__main__':
    main()
