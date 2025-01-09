import playerConnection, server

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *

class gameController():
    '''
    overklassen der spørger om man vil være host eller "bare" player,
    og opretter evt. host og playerConnection
    '''
    def __init__(self):
        self.popUp = startPopUp(self)
        self.popUp.show()
        

class startPopUp(QMainWindow):
    def __init__(self, p):
        self.parent=p
        
        super().__init__()
        central = QWidget(self)
        self.setCentralWidget(central)
        self.setWindowTitle("Start-spil")
        
        self.label=QLabel()
        self.label.setText("Select button")
        self.txtEditor = QTextEdit()
        self.bHost, self.bJoin = QPushButton(), QPushButton()
        
        layout = QGridLayout()
        layout.addWidget(self.bHost, 0,0)
        layout.addWidget(self.bJoin, 1,0)
        layout.addWidget(self.label, 0,1)
        layout.addWidget(self.txtEditor, 1,1)
        central.setLayout(layout)
        self.setBaseSize(QSize(800, 600))
    
    def hostHandler(self):
        pass
        
    def joinHandler(self):
        pass
        