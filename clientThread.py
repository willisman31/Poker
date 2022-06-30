#!/usr/bin/env python3

from socket import *
from threading import *
import time, ClientSide

class ClientThread(object):

    def __init__(self,host,port, screen):

        self.sock = socket()

        try:
            #Connecting to socket
            self.sock.connect((host, port)) #Connect takes tuple of host and port
        except Exception as msg:
            print("Could not connect to server.\nError msg : ", msg)
            ClientSide.PokerClient(screen)

        #start_new_thread(self.client_thread,(self.sock,))

    def client_thread(self,sock):
        #Infinite loop to keep client running.
        while True:
            #data = sock.recv(1024)
            #print data
            text = raw_input("Enter Text : ")
            sock.send(text)

        sock.close()

def main():
    host = socket.gethostname()
    port = 1234

    obj = ClientThread(host,port)
    time.sleep(60)

if __name__ == '__main__':
    main()
