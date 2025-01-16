import connection, server
import socket as s


from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon
import os
from PyQt6.QtWidgets import *

class gameController(QWidget):
    '''
    overklassen der spørger om man vil være host eller "bare" player,
    og opretter evt. host og playerConnection
    '''
    newServerDataSignal = pyqtSignal(list)
    closePopUpSignal = pyqtSignal(str)
    joinPopUpSignal = pyqtSignal(str)
    def __init__(self, p):
        super().__init__()
        self.p=p
        self.localServerExists = False
        self.newServerDataSignal.connect(self.p.newDataFromServer)
        self.closePopUpSignal.connect(self.closePopUp)
        self.newGame()
    
    def receiveData(self, sender, receivedStr:str):
        self.lines = receivedStr.split("\n\r")
        #print("Modtaget"+receivedStr+"!")
        #print("har modtaget dette data", self.lines)
        for i in range (len(self.lines)):
            if "" == self.lines[0]:
                self.lines.pop(0)
            elif "YOU ARE" in self.lines[0]:
                self.p.playerIs = self.lines[0][8] #should be either "1" or "2"
                if self.popUpExists:
                    #print("forsøger at lukke popup")
                    self.closePopUpSignal.emit("")
                    print (f"you are {self.p.playerIs}\n{receivedStr}")
                    #print("har lukket popUp")
                self.lines.pop(0)
                
            elif "@" in self.lines[0]:
                self.lines.pop(0)
                #modtaget serverens velkommen besked med ip 
            else:
                self.newServerDataSignal.emit(self.lines)
                break
    
    def pConClosed(self, sender):
        self.receiveData(self, "NOBODY WINS\n\r"+"1"+"\n\r"+self.p.board+"\n\r-1")
            
    def newConnection(self, address:tuple|bool):
        if address:
            self.address = address
        try:
            socket = s.socket(s.AF_INET, s.SOCK_STREAM)
            socket.connect(self.address)
            self.setpCon(connection.connection(socket, self.receiveData, self.pConClosed))
            print("new connection from player to "+ str(self.address))
            return True
        except:
            self.setpCon("")
            return False
    
    
    
            
    def newGame(self, tryJoiningAddress = False):
        if tryJoiningAddress:
            self.popUp = startPopUp(self, self.address)
            if self.localServerExists:
                self.joinPopUpSignal.connect(self.popUp.hostHandler)
            else:
                self.joinPopUpSignal.connect(self.popUp.joinHandler)
        else:
            self.popUp = startPopUp(self)
        
        self.popUp.show()
        
        self.popUpExists = True
        self.pCon, self.lines = "", []
        
        if tryJoiningAddress:
            self.joinPopUpSignal.emit("")
        
    
    def closePopUp(self):
        if self.popUpExists:
            self.popUp.closeMe()       
        
    def closeMe(self):
        if self.pCon != "":
            self.pCon.closeMe()
        if self.localServerExists:
            self.server.closeMe()
        self.closePopUpSignal.emit("")
        super().close()
            
    def createServer(self):
        self.server = server.host()
        self.localServerExists = True
        
    def send(self, string:str):
        if self.pCon != "":
            self.pCon.send(string) 
    
    def setpCon(self, var):
        if self.pCon != "":
            self.pCon.closeMe()
        self.pCon = var

class startPopUp(QWidget):
    def __init__(self, p:gameController, address = False):
        self.p=p
        super().__init__()
        #central = QWidget(self)
        
        #self.setCentralWidget(central)
        self.setWindowTitle("Start-spil")
        self.setWindowIcon(QIcon(os.path.join(".","assets","Logo.png")))
        
        self.label=QLabel()
        self.label.setText("Select button")
        self.txtEditor = QTextEdit()
        if address:
            self.txtEditor.setText(str(address[0]))
        self.txtEditor.setFixedHeight(50)
        self.bHost, self.bJoin = QPushButton(), QPushButton()
        self.bHost.clicked.connect(self.hostHandler)
        self.bJoin.clicked.connect(self.joinHandler)
        self.bHost.setText("Host")
        self.bJoin.setText("Join")
        
        
        layout = QGridLayout()
        layout.addWidget(self.bHost, 0,0)
        layout.addWidget(self.bJoin, 1,0)
        layout.addWidget(self.label, 0,1)
        layout.addWidget(self.txtEditor, 1,1)
        #central.setLayout(layout)
        self.setLayout(layout)
        self.setBaseSize(QSize(800, 600))
    
    def hostHandler(self):
        if self.p.localServerExists:
            self.label.setText("Local server already exists, awaiting player 2")
            self.txtEditor.setText(self.p.server.myIP)
            
        else:
            try:
                self.p.createServer()
                self.txtEditor.setText(self.p.server.myIP)
                self.label.setText("Local server at the IP below, awaiting player 2")
            except:
                self.label.setText("Local server already exists in another window.")
                return None
            
        if self.p.pCon == "":
            self.p.newConnection(("127.0.0.1", 54321))
        else:
            if self.p.address != ("127.0.0.1", 54321):
                self.p.newConnection(("127.0.0.1", 54321))
            else:
                self.label.setText("Already connected to local server, awaiting player 2")
                


    def joinHandler(self, a0=0):
        if self.p.localServerExists:
            self.label.setText("Closing local server")
            self.p.server.closeMe()
            self.p.localServerExists = False
        
        chosenIP=self.txtEditor.toPlainText().strip()

        if chosenIP == "":
            chosenIP = "127.0.0.1"
            self.txtEditor.setText("127.0.0.1")
            
        if not self.p.newConnection((chosenIP, 54321)):
            self.label.setText("The server at the chosen IP dosen't exist")
        else:
            self.label.setText("Succesfully connected to the server")
            
            #print("dosent exist")  

    def closeEvent(self, a0 = 0):
        if self.p.popUpExists:
            self.p.p.closeEvent()
        
        
    def closeMe(self):
        self.p.popUpExists=False
        #self.close()
        super().close()
        