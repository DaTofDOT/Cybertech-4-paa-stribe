from threading import Thread
import socket as s
import time
import calculateBoard

import connection

class host():
    def __init__(self, port = 54321):
        """
        Initializes the host class, which handles all connections to the server, and the games running on the server.

        Parameters:
        - port: The port to listen on. Defaults to 54321 if not specified.

        Creates a socket and binds it to the specified port. Then starts a new thread that calls the run method of this class.
        """
        self.port = port
        self.listeningSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.listeningSocket.bind(("", self.port))
        self.listeningSocket.listen()
        

        self.myIP =s.gethostbyname(s.gethostname())

        t = Thread(target=self.run)
        t.start()
                
    def removeMeFromOngoingGames(self, klasse):
        try:
            self.ongoingGames.remove(klasse)
        except:
            pass
                
    def run(self):
        """
        Main loop of the server. Listens for new connections, and pairs up connected clients into games when possible.

        When a new connection is established, it is added to the list of current connections. If there are at least 2 connections, the first two are paired up and a new game is started with them as the players.

        The loop continues until the server is closed, at which point it stops listening for new connections and all existing games are closed.
        """
        self.keepAlive =True
        self.currentConnections = []
        self.ongoingGames = []
        
        while self.keepAlive:
            try:
                newTCPconn, addr = self.listeningSocket.accept()#blokere indtil ny forbindelse
                print("new connection To server")
                newTCPconn.sendall(("WELCOME TO 4-IN-A-ROW @ "+self.myIP+"\n\r").encode())
                self.currentConnections.append(newTCPconn)
                if len(self.currentConnections) >= 2:
                    p1=self.currentConnections.pop(0)
                    p2=self.currentConnections.pop(0)
                    self.ongoingGames.append(serverGame(self, (p1, p2)))
            except:
                pass


    def closeMe(self):
        """
        Closes the server and all ongoing games and connections.

        This function sets the server's keep-alive status to False, closes the listening socket, and terminates all ongoing games and connections. It first iterates over the list of ongoing games, closing each one, and then iterates over the list of current connections, closing each socket.
        """
        self.keepAlive = False
        self.listeningSocket.close()
        time.sleep(0.02)
        originalLen=(len(self.ongoingGames))
        for i in range(originalLen):
            self.ongoingGames[0].closeMe()
        originalLen=(len(self.currentConnections))
        for i in range(originalLen):
            self.currentConnections[i].close() #sockets
        
        
class serverGame():
    def __init__(self, p:host, players:tuple|list):
        """
        Constructor for a new serverGame object.

        Parameters:
        - p: a host object, the server that this game is a part of.
        - players: a tuple or list of two sockets, the connections to the two players in this game.

        This constructor sets up the game tracker and player connections. It sends a welcome message to each player, and sends the initial game state to each player. It then starts the game loop, which continues until the game is finished or a player disconnects.
        """
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
        '''
        If an connection is closed from the other side call this
        '''
        if self.keepAlive:
            self.closeMe()
    
    def receivedNewMessage(self, sender:connection.connection, message:str):
        """
        Called when a new message is received from one of the two players in this game.

        Parameters:
        - sender: the connection object that sent the message.
        - message: the received message, as a string.

        If the message is an integer and the sender is the current player, the message is interpreted as a move.
        It is then played on the game board, and the updated game state is sent to both players.
        If the message is not an integer, it is ignored.
        """
        if ((sender == self.p1Con and self.gameTracker.player_num == 1) or 
            (sender == self.p2Con and self.gameTracker.player_num == 2 )):
            try:
                column = int(message.strip())
            except:
                print("recived message wasn't an int")
                return

            newMessage = "\n\r".join(str(x) for x in self.gameTracker.play_move(column))
            self.p1Con.send(newMessage)
            self.p2Con.send(newMessage)
        
        
        
    def closeMe(self):
        """
        Closes this game server and its associated connections.

        It sends a final message to both players indicating the outcome of the game, and then closes the connections.
        Finally, it removes itself from the list of ongoing games in the overarching server object.
        """
        self.keepAlive = False
        time.sleep(0.02) #vent på at alle forbindelser lukker
        if self.p1Con.keepAlive == True and self.p2Con == True:
            
            message = "NOBODY WINS\n\r"+str(self.gameTracker.player_num)+"\n\r"+self.gameTracker.board_str+"\n\r-1"

        elif self.p1Con.keepAlive == True:
            message = "1 WINS\n\r"+str(self.gameTracker.player_num)+"\n\r"+self.gameTracker.board_str+"\n\r-1"

        elif self.p2Con.keepAlive == True: 
            message = "2 WINS\n\r"+str(self.gameTracker.player_num)+"\n\r"+self.gameTracker.board_str+"\n\r-1"
        else: #begge forbindelser er lukkede
            message = ""

        self.p1Con.send(message)
        self.p2Con.send(message)
        
        self.p1Con.closeMe()
        self.p2Con.closeMe()
        
        self.overServer.removeMeFromOngoingGames(self)