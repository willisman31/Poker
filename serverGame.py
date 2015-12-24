from deck import *

deck = Deck()

def init(clients):
    numberOfPlayers = len(clients)
    #Initializing cards
    for i in range(0, numberOfPlayers):
        cards[i]=(deck.pop(),deck.pop())



def main(clients):
    init(clients)
