import playerConnection, server
import socket as s


from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtWidgets import *

class gameController(QWidget):
    '''
    overklassen der spørger om man vil være host eller "bare" player,
    og opretter evt. host og playerConnection
    '''
    newServerDataSignal = pyqtSignal(list)
    def __init__(self, p):
        super().__init__()
        self.p=p
        self.localServerExists = False
        self.popUp = startPopUp(self)
        self.popUp.show()
        self.popUpExists = True
        self.pCon, self.lines = "", []
        self.newServerDataSignal.connect(self.p.newDataFromServer)
    
    def receiveData(self, sender, receivedStr:str):
        print("Modtaget"+receivedStr+"!")
        if "YOU ARE" in receivedStr:
            self.p.playerIs = receivedStr[8] #should be either "1" or "2"
        elif "@" in receivedStr:
            pass
            #modtaget serverrens velkommen besked med ip 
        else:
            self.lines = receivedStr.split()
            self.newServerDataSignal.emit(self.lines)
        

            
        
    def closeMe(self):
        if self.pCon != "":
            self.pCon.closeMe()
        if self.localServerExists:
            self.server.closeMe()
        if self.popUpExists:
            self.popUp.closeMe()
        super().close()
            
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
            self.label.setText("Local server already exists, awaiting player 2")
            
        else:
            self.p.createServer()
            socket = s.socket(s.AF_INET, s.SOCK_STREAM)
            socket.connect(("127.0.0.1", 54321))
            self.p.setpCon(playerConnection.connection(socket, self.p.receiveData)) 
            self.label.setText("Local server created, awaiting player 2")
        
        self.txtEditor.setText(self.p.server.myIP)
        


    def joinHandler(self):
        if self.p.localServerExists:
            self.label.setText("Closing local server")
            self.p.server.closeMe()
            self.p.localServerExists = False
        
        chosenIP=self.txtEditor.toPlainText()
        if chosenIP == "":
            chosenIP = "127.0.0.1"
            self.txtEditor.setText("127.0.0.1")
        
        try:
            socket = s.socket(s.AF_INET, s.SOCK_STREAM)
            socket.connect((chosenIP, 54321))
            self.p.setpCon(playerConnection.connection(socket, self.p.receiveData))
        except:
            self.label.setText("The server at the chosen IP dosen't exist")
            print("dosent exist")  
            self.p.setpCon("")
    
    def closeMe(self):
        self.p.popUpExists=False
        super().close()
        