#!/usr/bin/python

# Import all from module socket
from socket import *
#Importing all from thread
from thread import *

import time

num_of_clients = 0

# Defining server address and port
host = '127.0.0.1'  #'localhost' or '127.0.0.1' or '' are all same
port = 52001 #Use port > 1024, below it all are reserved

class ServerThread(object):

    def __init__(self):

        #Creating socket object
        sock = socket()
        #Binding socket to a address. bind() takes tuple of host and port.
        sock.bind((host, port))

        #print self.get_ip()
        #print self.get_port()
        #print self.get_num_of_clients()
        #print([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

        #Listening at the address
        sock.listen(5) #5 denotes the number of clients can queue

        #t1 = Thread(target=self.serverthread, args=(scriptA + argumentsA))

        start_new_thread(self.server_thread,(sock,))


    def server_thread(self,sock):

        while True:
        #Accepting incoming connections
            conn, addr = sock.accept()
        #Creating new thread. Calling clientthread function for this function and passing conn as argument.
            global num_of_clients
            num_of_clients = num_of_clients + 1
            start_new_thread(self.client_thread,(conn,addr)) #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.

        conn.close()
        sock.close()
    def get_ip(self):
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        return s.getsockname()[0]

    def get_port(self):
        global port
        return port

    def get_num_of_clients(self):
        global num_of_clients
        return num_of_clients


    def client_thread(self,conn,addr):
    #infinite loop so that function do not terminate and thread do not end.
         while True:

    #Sending message to connected client
             #conn.send('Hi! I am server\n') #send only takes string
    #Receiving from client
             data = conn.recv(1024) # 1024 stands for bytes of data to be received
             if not data:
                 global num_of_clients
                 num_of_clients -= 1
                 break
             print str(addr) + ' : ' +data


if __name__ == '__main__':
    obj = ServerThread()
    print obj.get_ip()
    time.sleep(60)
