import game

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *


class player(QMainWindow):
    '''
    hovedklassen
    '''
    def __init__(self):
        super().__init__()
        pass
    
    def closeEvent(self, a0=0):
        
        self.close()