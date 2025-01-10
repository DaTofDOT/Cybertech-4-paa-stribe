import socket as s
from threading import Thread

class connection():
    def __init__(self , TCPconnection, receiveFunction):
        self.connection = TCPconnection
        self.receiveFunction = receiveFunction
        
        t = Thread(target=self.receiveRun)
        t.start()
    
    def receiveRun(self):
        self.keepAlive = True
        while self.keepAlive:
            receivedData = self.connection.recv(1024)
            if receivedData == b'': #connection closed from the other side
                self.connection.close()
                self.keepAlive = False
            self.receiveFunction(self, receivedData.decode())
    
    def send(self, data:str):
        self.connection.sendall(data.encode())
    
    def closeMe(self):
        self.keepAlive = False
        self.connection.close() # may course crash
    