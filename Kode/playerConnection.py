import socket as s
from threading import Thread

class connection():
    def __init__(self , TCPconnection, receiveFunction, closeFunction = False): #, closeFunction?
        self.connection = TCPconnection
        self.receiveFunction = receiveFunction
        self.closeFunction = closeFunction
        t = Thread(target=self.receiveRun)
        t.start()
    
    def receiveRun(self):
        self.keepAlive = True
        while self.keepAlive:
            try:
                receivedData = self.connection.recv(1024)
            except:
                receivedData = b''
                
            if receivedData == b'' or  "PLZ-LUK-FORBINDELSE" in receivedData.decode(): #connection closed from the other side
                self.connection.close()
                self.keepAlive = False
                if self.closeFunction:
                    self.closeFunction(self)
            else:
                self.receiveFunction(self, receivedData.decode())

    def send(self, data:str):
        try:
            self.connection.sendall(data.encode())
            print("sendte dette data: "+ data+" :")
        except:
            print("sendte IKKE dette data: "+ data+" :")
    
    def closeMe(self):
        if self.keepAlive:
            self.keepAlive = False
            self.send("PLZ-LUK-FORBINDELSE")
    