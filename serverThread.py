#!/usr/bin/env python3

from socket import *
from threading import *
import time, main

class ServerThread(object):

    def __init__(self):

        self.num_of_clients = 0
        self.clients = []

        # Defining server address and port

        self.host = socket.gethostname()
        self.host = self.get_ip()
        self.port = 1234 #Use port > 1024, below it all are reserved

        #Creating socket object
        sock = socket()

        #Binding socket to a address. bind() takes tuple of host and port.
        try : sock.bind((self.host, self.port))
        except Exception as msg:
            print("Could not start server.\n",msg)
            print("Restarting the game.")
            main.Begin()
            sys.exit()

        #Listening at the address
        sock.listen(5) #5 denotes the number of clients can queue

        start_new_thread(self.server_thread,(sock,))


    def server_thread(self,sock):

        while True:
            #Accepting incoming connections
            conn, addr = sock.accept()

            self.clients.append(conn)
            self.num_of_clients = self.num_of_clients + 1
            #Creating new thread. Calling clientthread function for this function and passing conn as argument.
            #start_new_thread(self.client_thread,(conn,addr)) #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.

        sock.close()

    def get_ip(self):
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        return s.getsockname()[0]

    def get_port(self):
        return self.port

    def get_num_of_clients(self):
        return self.num_of_clients

    def client_thread(self,conn,addr):
        #infinite loop so that function do not terminate and thread do not end.
        while True:
            #Sending message to connected client
            #conn.send('Hi! I am server\n') #send only takes string
            #Receiving from client
            data = conn.recv(1024) # 1024 stands for bytes of data to be received
            if not data:
                self.num_of_clients -= 1
                break
            print(str(addr) + ' : ' +data)
        conn.close()

if __name__ == '__main__':
    obj = ServerThread()
    print(obj.get_ip())
    time.sleep(60)

