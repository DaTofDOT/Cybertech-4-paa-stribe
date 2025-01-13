import playerConnection, server
import socket as s

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *

class gameController():
    '''
    overklassen der spørger om man vil være host eller "bare" player,
    og opretter evt. host og playerConnection
    '''
    def __init__(self):
        self.localServerExists = False
        self.popUp = startPopUp(self)
        self.popUp.show()
        self.popUpExists = True
        self.setpCon("")
    
    def receiveData(self, sender, receivedStr:str):
        print("Modtaget"+receivedStr+"!")
        
    def closeMe(self):
        if self.pCon != "":
            self.pCon.closeMe()
        if self.localServerExists:
            self.server.closeMe()
        if self.popUpExists:
            self.popUp.closeMe()
            
    def createServer(self):
        self.server = server.host()
        self.localServerExists = True
        
    def send(self, string:str):
        if self.pCon != "":
            self.pCon.send(string) 
    
    def setpCon(self, var):
        self.pCon = var

class startPopUp(QMainWindow):
    def __init__(self, p:gameController):
        self.p=p
        super().__init__()
        central = QWidget(self)
        self.setCentralWidget(central)
        self.setWindowTitle("Start-spil")
        
        self.label=QLabel()
        self.label.setText("Select button")
        self.txtEditor = QTextEdit()
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
        central.setLayout(layout)
        self.setBaseSize(QSize(800, 600))
    
    def hostHandler(self):
        if self.p.localServerExists:
            pass
        else:
            self.p.createServer()
        
        self.txtEditor.setText(self.p.server.myIP)
        
        socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        socket.connect(("127.0.0.1", 54321))
        self.p.setpCon(playerConnection.connection(socket, self.p.receiveData)) 

    def joinHandler(self):
        if self.p.localServerExists:
            self.p.server.closeMe()
            self.p.localServerExists = False
        
        #hæntIP fra UI
        
        chosenIP=self.txtEditor.toPlainText()
        if chosenIP == "":
            chosenIP = "127.0.0.1"
        
        try:
            socket = s.socket(s.AF_INET, s.SOCK_STREAM)
            socket.connect((chosenIP, 54321))
            self.p.setpCon(playerConnection.connection(socket, self.p.receiveData))
        except:
            print("dosent exist")  
    
    def closeMe(self):
        self.p.popUpExists=False
        super().close()
        