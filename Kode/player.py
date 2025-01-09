import game

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *


class player(QMainWindow):
    '''
    hovedklassen
    '''
    def __init__(self):
        super().__init__()
        self.controller = game.gameController()
        
        pass
    
    def closeEvent(self, a0=0):
        
        self.close()