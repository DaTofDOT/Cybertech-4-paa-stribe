from threading import Thread
import socket as s
import random, time

import playerConnection

class host():
    def __init__(self, port = 54321):
        self.port = port
        self.listeningSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.listeningSocket.bind(("", self.port))
        self.listeningSocket.listen()
        
        #TODO find min IP
        self.myIP = "127.0.0.1"
        
        t = Thread(target=self.run)
        t.start()
                
    def removeMeFromOngoingGames(self, klasse):
        self.ongoingGames.remove(klasse)
                
    def run(self):
        self.keepAlive =True
        self.currentConnections = []
        self.ongoingGames = []
        
        
        while self.keepAlive:
            newTCPconn, addr = self.listeningSocket.accept()#blokere indtil ny forbindelse
            newTCPconn.sendall(("WELCOME TO 4-IN-A-ROW @ "+self.myIP).encode())
            self.currentConnections.append(newTCPconn)
            if len(self.currentConnections) >= 2:
                p1=self.currentConnections.pop(0)
                p2=self.currentConnections.pop(0)
                self.ongoingGames.append(serverGame(self, (p1, p2)))
    
    def closeMe(self):
        self.keepAlive = False
        tempSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
        tempSocket.bind(("127.0.0.1", self.port))
        tempSocket.close()
        self.listeningSocket.close()
        time.sleep(0.02)
        originalLen=(len(self.ongoingGames))
        for i in originalLen:
            self.ongoingGames[0].closeMe()
        originalLen=(len(self.currentConnections))
        for i in originalLen:
            self.currentConnections[i].close()
        
        

                
class serverGame():
    def __init__(self, p, players:tuple|list):
        self.overServer = p
        
        p1 , p2 = players
        self.p1Con = playerConnection.connection(p1, self.receivedNewMessage)
        self.p2Con = playerConnection.connection(p2, self.receivedNewMessage)
        self.p1Con.send("YOU ARE 1")
        self.p2Con.send("YOU ARE 2")
        self.board = "."*42
        self.currentTurn = random.randrange(1,3) # tilfældigt 1 eller 2
        self.newestPieceIndex = -1
        '''
        t = Thread(target=self.run) 
        t.start()
        '''
    
    def updateTurnVar(self):
        if self.currentTurn == 1:
            self.currentTurn = 2
        else:
            self.currentTurn = 1
        return self.currentTurn
    
    
    def receivedNewMessage(self, sender, message):
        if sender == self.p1Con:
            self.p2Con.send(message)
        else: # sender == self.p2Con
            self.p1Con.send(message)
        
    
    def run(self):
        self.keepAlive = True
        while self.keepAlive:
            pass
        
    def closeMe(self):
        self.keepAlive = False
        self.p1Con.closeMe() #not final !!!
        self.p2Con.closeMe() # not final !!!
        self.overServer.removeMeFromOngoingGames(self)