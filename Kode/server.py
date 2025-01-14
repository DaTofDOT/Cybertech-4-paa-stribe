from threading import Thread
import socket as s
import time
import calculateBoard

import connection

class host():
    def __init__(self, port = 54321):
        self.port = port
        self.listeningSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.listeningSocket.bind(("", self.port))
        self.listeningSocket.listen()
        
        #TODO find min IP
        #temp = s.socket(s.AF_INET, s.SOCK_DGRAM)
        #temp.connect(("8.8.8.8", 80))
        #self.myIP = str(temp.getsockname()[0])
        #temp.close()
        self.myIP =s.gethostbyname(s.gethostname())

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
            print("new connection To server")
            newTCPconn.sendall(("WELCOME TO 4-IN-A-ROW @ "+self.myIP).encode())
            self.currentConnections.append(newTCPconn)
            if len(self.currentConnections) >= 2:
                p1=self.currentConnections.pop(0)
                p2=self.currentConnections.pop(0)
                self.ongoingGames.append(serverGame(self, (p1, p2)))
    
    def closeMe(self):
        self.keepAlive = False
        tempSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
        tempSocket.connect(("127.0.0.1", self.port))
        tempSocket.close()
        self.listeningSocket.close()
        time.sleep(0.02)
        originalLen=(len(self.ongoingGames))
        for i in range(originalLen):
            self.ongoingGames[0].closeMe()
        originalLen=(len(self.currentConnections))
        for i in range(originalLen):
            self.currentConnections[i].close() #sockets
        
        

'''                
class serverMessage():
    def __init__(self, p:host, players:tuple|list):
        self.overServer = p
        
        p1 , p2 = players
        try:
            self.p1Con = playerConnection.connection(p1, self.receivedNewMessage)
            self.p1Con.send("YOU ARE 1")
        except:
            print("player1 virker ikke")
            
        try:
            self.p2Con = playerConnection.connection(p2, self.receivedNewMessage)
            self.p2Con.send("YOU ARE 2")
        except:
            print("player2 virker ikke")
            

        #self.board = "0"*42
        #self.currentTurn = random.randrange(1,3) # tilfældigt 1 eller 2
        #self.newestPieceIndex = -1

        #t = Thread(target=self.run) 
        #t.start()
    
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
        #message = "NOBODY WINS\n\r"+str(self.currentTurn)+"\n\r"+self.board+"\n\r"+str(self.newestPieceIndex)
        
        
        self.p1Con.closeMe() #not final !!!
        self.p2Con.closeMe() #not final !!!
        self.overServer.removeMeFromOngoingGames(self)
'''
        
class serverGame():
    def __init__(self, p:host, players:tuple|list):
        self.overServer = p
        self.keepAlive = False
        self.gameTracker = calculateBoard.calculateBoard()
        
        p1 , p2 = players


        self.p1Con = connection.connection(p1, self.receivedNewMessage, self.connectionCloseFunction)
        self.p2Con = connection.connection(p2, self.receivedNewMessage, self.connectionCloseFunction)
  
        self.p1Con.send("YOU ARE 1\n\r")  
        self.p2Con.send("YOU ARE 2\n\r")
        
        self.keepAlive = True

        initial=f"OK\n\r{self.gameTracker.player_num}\n\r{self.gameTracker.board_str}\n\r-1"
        self.p1Con.send(initial)
        self.p2Con.send(initial)
        
        
    
    def connectionCloseFunction(self, sender):
        if self.keepAlive:
            self.closeMe()
    
    def receivedNewMessage(self, sender:connection.connection, message:str):
        if ((sender == self.p1Con and self.gameTracker.player_num == 1) or 
            (sender == self.p2Con and self.gameTracker.player_num == 2 )):
            try:
                column = int(message.strip())
            except:
                print("recived message wasn't an int")
                return

            newMessage = "\n\r".join(str(x) for x in self.gameTracker.play_move(column))+"\n\r"
            self.p1Con.send(newMessage)
            self.p2Con.send(newMessage)
        
        
        
    def closeMe(self):
        self.keepAlive = False
        message = "NOBODY WINS\n\r"+str(self.gameTracker.player_num)+"\n\r"+self.gameTracker.board_str+"\n\r-1\n\r"
        self.p1Con.send(message)
        self.p2Con.send(message)
        
        self.p1Con.closeMe()
        self.p2Con.closeMe()
        self.overServer.removeMeFromOngoingGames(self)