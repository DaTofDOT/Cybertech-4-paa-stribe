import socket as s
from threading import Thread

class connection():
    def __init__(self , TCPconnection, receiveFunction, closeFunction = False):
        """
        Constructor for a new connection object.

        Parameters:
        - TCPconnection: socket object, the underlying connection.
        - receiveFunction: function, called when new data is received from the connection.
        - closeFunction: function, called when the connection is closed. Defaults to False if not specified.

        This constructor sets up the connection and starts a new thread that calls the receiveRun method of this class.
        """
        self.connection = TCPconnection
        self.receiveFunction = receiveFunction
        self.closeFunction = closeFunction
        t = Thread(target=self.receiveRun)
        t.start()
    
    def receiveRun(self):
        """
        Continuously receives data from the connection and processes it.

        This method runs in a loop as long as the connection is alive. It attempts to receive data from the 
        socket. If data is received, the receiveFunction is called with the decoded data. If the connection 
        is closed from the other side or a termination message is received, it closes the connection, calls 
        the closeFunction if specified, and stops the loop.
        """
        self.keepAlive = True
        while self.keepAlive:
            try:
                receivedData = self.connection.recv(1024)
            except:
                receivedData = b''
                
            if receivedData == b'' or  "PLZ-LUK-FORBINDELSE" in receivedData.decode(): #connection closed from the other side
                self.connection.close()
                if self.closeFunction and self.keepAlive: #only call closing function if closed from other side
                    self.closeFunction(self)
                self.keepAlive = False

            else:
                self.receiveFunction(self, receivedData.decode())

    def send(self, data:str):
        try:
            self.connection.sendall(data.encode())
        except:
            pass
    
    def closeMe(self):
        if self.keepAlive:
            self.keepAlive = False
            self.send("PLZ-LUK-FORBINDELSE")